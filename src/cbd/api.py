"""Core API: CBDModel protocol and detect_bias implementation (permutation test).

Enhancements in this version:
- Input standardization and validation (numpy arrays, shape checks, single-class guard).
- Use numpy.random.Generator for reproducible random streams.
- Support stratified permutations (permute within groups supplied via `stratify` array).
- Optional retrain null_method placeholder (not implemented fully here; raises if requested).
- n_jobs parameter (uses ThreadPoolExecutor for parallel metric computation to avoid heavy pickling).
- Improved docstrings and type hints.
"""
from typing import Protocol, runtime_checkable, Optional, Callable, Any, Dict, List
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed

MetricFn = Callable[[Any, Any], float]

@runtime_checkable
class CBDModel(Protocol):
    """Protocol for models usable by detect_bias.
    - predict(X) -> y_pred required
    - optionally predict_proba(X)
    """
    def predict(self, X):
        ...
    def predict_proba(self, X):
        ...


def _ensure_predict(model: CBDModel):
    if not hasattr(model, "predict"):
        raise ValueError("Model must implement predict(X)")


def _to_numpy(a):
    import numpy as _np
    arr = _np.asarray(a)
    return arr


def _permute_labels_within_groups(y, rng: np.random.Generator, stratify: Optional[np.ndarray]):
    """Return a permuted copy of y. If stratify is provided (same length as y),
    labels are permuted only within each group defined by stratify.
    """
    y = np.asarray(y)
    perm = np.empty_like(y)
    if stratify is None:
        # global permutation
        idx = rng.permutation(len(y))
        perm = y[idx]
    else:
        stratify = np.asarray(stratify)
        if stratify.shape[0] != y.shape[0]:
            raise ValueError("stratify must be the same length as y")
        perm = np.empty_like(y)
        for grp in np.unique(stratify):
            indices = np.where(stratify == grp)[0]
            if len(indices) <= 1:
                perm[indices] = y[indices]
            else:
                idx = rng.permutation(len(indices))
                perm[indices] = y[indices[idx]]
    return perm


def detect_bias(model: CBDModel,
                X,
                y,
                metric: MetricFn,
                n_permutations: int = 1000,
                random_state: Optional[int] = None,
                return_permutations: bool = False,
                stratify: Optional[Any] = None,
                null_method: str = "labels",
                n_jobs: int = 1) -> Dict[str, Any]:
    """
    Perform a permutation test to detect unusually high metric values that could indicate circular bias.

    Parameters
    ----------
    model : CBDModel
        Object implementing predict(X). For probabilistic metrics, it may also implement predict_proba(X).
    X : array-like
        Features (will be converted to numpy array); only used for computing predictions.
    y : array-like
        True labels/targets (will be converted to 1D numpy array).
    metric : callable
        Function metric(y_true, y_pred) -> float
    n_permutations : int
        Number of permutations to perform for the null distribution.
    random_state : Optional[int]
        Seed for RNG to make permutation reproducible.
    return_permutations : bool
        If True, include the list of permuted metrics in the returned dict.
    stratify : Optional[array-like]
        If provided, must be same length as y. Permutations will be performed within each group defined
        by stratify (useful to preserve grouping structure).
    null_method : {"labels", "retrain"}
        Which null to simulate. "labels" keeps model fixed and permutes labels (fast).
        "retrain" would retrain the model on each permuted dataset (not implemented here; raises).
    n_jobs : int
        Number of parallel workers for computing permuted metrics. Uses threads to avoid pickle issues.

    Returns
    -------
    dict
        Keys: observed_metric, p_value, n_permutations, conclusion; optionally permuted_metrics
    """
    # Basic checks and normalization
    X_a = _to_numpy(X)
    y_a = _to_numpy(y)
    if y_a.ndim > 1:
        y_a = y_a.ravel()

    if X_a.shape[0] != y_a.shape[0]:
        raise ValueError("X and y must have the same number of samples")

    if y_a.shape[0] < 2:
        raise ValueError("Need at least 2 samples to perform permutation testing")

    # check single-class
    unique_labels = np.unique(y_a)
    if unique_labels.shape[0] <= 1:
        raise ValueError("y must contain more than one unique label/value")

    if null_method != "labels":
        # For now, only labels method is implemented in this function
        raise NotImplementedError("Only null_method='labels' is implemented in this version")

    _ensure_predict(model)

    # Predictions are computed once (label-shuffle test)
    y_pred = model.predict(X_a)

    try:
        observed = float(metric(y_a, y_pred))
    except Exception:
        observed = float(metric(np.asarray(y_a), np.asarray(y_pred)))

    rng = np.random.default_rng(random_state)

    permuted_metrics = []

    def _compute_one(_):
        y_perm = _permute_labels_within_groups(y_a, rng, stratify)
        try:
            return float(metric(y_perm, y_pred))
        except Exception:
            return float(metric(np.asarray(y_perm), np.asarray(y_pred)))

    if n_jobs == 1:
        for i in range(n_permutations):
            m = _compute_one(i)
            permuted_metrics.append(m)
    else:
        # Use ThreadPoolExecutor to avoid heavy pickling of model objects; metrics often release GIL
        with ThreadPoolExecutor(max_workers=n_jobs) as exc:
            futures = [exc.submit(_compute_one, i) for i in range(n_permutations)]
            for f in as_completed(futures):
                permuted_metrics.append(f.result())

    permuted_metrics = np.asarray(permuted_metrics)
    # p-value: fraction of permuted metrics >= observed (one-sided test)
    p_value = float((np.sum(permuted_metrics >= observed) + 1) / (n_permutations + 1))

    alpha = 0.05
    if p_value <= alpha:
        conclusion = f"Suspicious: p <= {alpha} — potential circular bias detected"
    else:
        conclusion = f"No strong evidence of circular bias (p = {p_value:.3f})"

    result = {
        "observed_metric": observed,
        "p_value": p_value,
        "n_permutations": n_permutations,
        "conclusion": conclusion,
    }
    if return_permutations:
        result["permuted_metrics"] = permuted_metrics.tolist()
    return result
