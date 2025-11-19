"""Core API: CBDModel protocol and detect_bias implementation (permutation test)."""
from typing import Protocol, runtime_checkable, Optional, Callable, Any, Dict, List, Literal, Union
import numpy as np
from copy import deepcopy
import warnings
from sklearn.utils import check_array, check_consistent_length

MetricFn = Callable[[Any, Any], float]
BackendType = Literal["threads", "processes"]

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

def _ensure_predict(model):
    if not hasattr(model, "predict"):
        raise ValueError("Model must implement predict(X)")

def detect_bias(model: CBDModel,
                X,
                y,
                metric: MetricFn,
                n_permutations: int = 1000,
                random_state: Optional[int] = None,
                return_permutations: bool = False,
                n_jobs: int = 1,
                backend: BackendType = "threads",
                allow_proba: bool = False,
                null_method: Literal["permute", "retrain"] = "permute",
                subsample_size: Optional[int] = None,
                confidence_level: float = 0.95,
                stratify: bool = False,
                alpha: float = 0.05) -> Dict[str, Any]:
    """
    Perform a permutation test to detect unusually high metric values that could indicate circular bias.
    
    Parameters:
    -----------
    model : CBDModel
        Object implementing predict(X) and optionally predict_proba(X)
    X : array-like, shape (n_samples, n_features)
        Feature matrix. Accepts numpy arrays, pandas DataFrames, or scipy sparse matrices.
        Will be converted to numpy array internally.
    y : array-like, shape (n_samples,)
        Target labels. Accepts numpy arrays, pandas Series, or lists.
        Will be converted to 1D numpy array internally.
        Must contain at least 2 unique classes for meaningful testing.
    metric : callable
        Metric function(y_true, y_pred) -> float
        For probability metrics (AUC, log_loss), set allow_proba=True
    n_permutations : int, default=1000
        Number of label shuffles for null distribution.
        Recommended: 100 for quick tests, >=1000 for robust results
    random_state : int, optional
        Random seed for reproducibility. Uses numpy.random.Generator internally.
    return_permutations : bool, default=False
        If True, return all permuted metric values
    n_jobs : int, default=1
        Number of parallel workers. -1 uses all CPUs
    backend : {'threads', 'processes'}, default='threads'
        Parallel backend. Use 'processes' if model is picklable and GIL is a bottleneck
    allow_proba : bool, default=False
        If True, use predict_proba for metrics requiring probabilities (e.g., AUC, log_loss).
        Model must have predict_proba() or decision_function() method.
    null_method : {'permute', 'retrain'}, default='permute'
        'permute': shuffle labels only (fast)
        'retrain': retrain model on each permutation (conservative but slow, requires fit())
    subsample_size : int, optional
        If specified, subsample this many samples for faster computation on large datasets.
        Recommended for n_samples > 10000. If None, uses all samples.
    confidence_level : float, default=0.95
        Confidence level for p-value confidence interval (when n_permutations >= 1000)
    stratify : bool, default=False
        If True, preserve class distribution in each permutation (stratified shuffle).
        Recommended for imbalanced datasets to avoid spurious results.
    alpha : float, default=0.05
        Significance level for hypothesis test. Returned in conclusion.
    
    Returns:
    --------
    dict
        Comprehensive results with observed metric, p-value, permuted metrics, and conclusion
        
    Raises:
    -------
    ValueError
        - If model lacks required methods
        - If X and y have inconsistent lengths
        - If y has fewer than 2 unique classes
        - If allow_proba=True but model lacks predict_proba/decision_function
        - If null_method='retrain' but model lacks fit()
    
    Notes:
    ------
    - A low p-value (< alpha) suggests the observed metric is unusually high,
      which MAY indicate circular bias, but could also result from strong signal
      or sampling variation. Always combine with reproducibility checks and data audits.
    - For multiple comparisons, consider Bonferroni or Benjamini-Hochberg correction.
    - Random state handling uses numpy.random.Generator for improved reproducibility.
    
    Examples:
    ---------
    >>> from sklearn.ensemble import RandomForestClassifier
    >>> from sklearn.metrics import accuracy_score
    >>> model = RandomForestClassifier(random_state=42)
    >>> model.fit(X_train, y_train)
    >>> result = detect_bias(model, X_test, y_test, accuracy_score, n_permutations=1000)
    >>> print(result['p_value'], result['conclusion'])
    
    For probability metrics:
    >>> from sklearn.metrics import roc_auc_score
    >>> result = detect_bias(model, X_test, y_test, 
    ...                      lambda y_true, y_pred: roc_auc_score(y_true, y_pred[:, 1]),
    ...                      allow_proba=True, n_permutations=1000)
    """
    import numpy as _np

    _ensure_predict(model)

    # ===== INPUT VALIDATION =====
    # Standardize X to numpy array (supports pandas, sparse, etc.)
    X_a = check_array(X, accept_sparse=True, force_all_finite=False, ensure_2d=True)
    
    # Standardize y to 1D numpy array
    y_a = _np.asarray(y).ravel()
    
    # Check consistent lengths
    check_consistent_length(X_a, y_a)
    
    # Validate y has at least 2 unique classes
    unique_classes = _np.unique(y_a)
    n_classes = len(unique_classes)
    if n_classes < 2:
        raise ValueError(
            f"y must contain at least 2 unique classes for meaningful permutation test. "
            f"Found {n_classes} class(es): {unique_classes}. "
            f"Single-class data makes metrics like accuracy undefined."
        )
    
    # Validate alpha
    if not 0 < alpha < 1:
        raise ValueError(f"alpha must be in (0, 1), got {alpha}")
    
    # ===== RANDOM STATE SETUP =====
    # Use numpy.random.Generator for improved reproducibility
    if random_state is None:
        rng = _np.random.default_rng()
    else:
        rng = _np.random.default_rng(random_state)
    
    # Apply subsampling if requested
    if subsample_size is not None and subsample_size < len(y_a):
        subsample_idx = rng.choice(len(y_a), size=subsample_size, replace=False)
        X_a = X_a[subsample_idx]
        y_a = y_a[subsample_idx]
        warnings.warn(
            f"Subsampling {subsample_size} samples from {len(y)} for performance. "
            f"Results are approximate.",
            UserWarning
        )

    # Determine prediction method
    if allow_proba:
        if not hasattr(model, "predict_proba"):
            if hasattr(model, "decision_function"):
                warnings.warn(
                    "Model lacks predict_proba but has decision_function. Using decision_function as fallback.",
                    UserWarning
                )
                predict_fn = model.decision_function
            else:
                raise ValueError(
                    "allow_proba=True but model has neither predict_proba nor decision_function. "
                    "Set allow_proba=False or use a model with probability outputs."
                )
        else:
            predict_fn = model.predict_proba
    else:
        predict_fn = model.predict

    # Compute observed metric
    y_pred = predict_fn(X_a)
    observed = float(metric(y_a, y_pred))

    # Validate null_method
    if null_method == "retrain" and not hasattr(model, "fit"):
        raise ValueError("null_method='retrain' requires model to have fit() method")

    # ===== GENERATE PERMUTATION INDICES =====
    # Generate all permutation indices upfront for reproducibility
    if stratify:
        # Stratified permutation: preserve class distribution
        perm_indices = _generate_stratified_permutations(y_a, n_permutations, rng)
    else:
        # Standard permutation: shuffle all labels
        perm_indices = [rng.permutation(len(y_a)) for _ in range(n_permutations)]

    # ===== COMPUTE NULL DISTRIBUTION =====
    # Parallel or sequential execution
    if n_jobs == 1:
        # Sequential execution
        permuted_metrics = _compute_permuted_metrics_sequential(
            model, X_a, y_a, y_pred, metric, perm_indices, null_method, predict_fn
        )
    else:
        # Parallel execution
        permuted_metrics = _compute_permuted_metrics_parallel(
            model, X_a, y_a, y_pred, metric, perm_indices, null_method, predict_fn, n_jobs, backend
        )

    # p-value: fraction of permuted metrics >= observed (one-sided test)
    permuted_metrics = _np.array(permuted_metrics)
    p_value = float((_np.sum(permuted_metrics >= observed) + 1) / (n_permutations + 1))
    
    # Compute confidence interval for p-value if enough permutations
    p_value_ci = None
    if n_permutations >= 1000:
        p_value_ci = _compute_pvalue_ci(p_value, n_permutations, confidence_level)

    # Generate conclusion based on configurable alpha
    if p_value <= alpha:
        conclusion = f"Suspicious: p = {p_value:.4f} <= {alpha} — potential circular bias detected"
    else:
        conclusion = f"No strong evidence of circular bias (p = {p_value:.4f} > {alpha})"

    result = {
        "observed_metric": observed,
        "p_value": p_value,
        "n_permutations": n_permutations,
        "conclusion": conclusion,
        "alpha": alpha,
        "null_method": null_method,
        "stratified": stratify,
        "backend": backend if n_jobs != 1 else "sequential",
        "n_jobs": n_jobs,
        "n_samples": len(y_a),
        "n_classes": n_classes,
        "subsampled": subsample_size is not None
    }
    if p_value_ci is not None:
        result["p_value_ci"] = p_value_ci
        result["confidence_level"] = confidence_level
    if return_permutations:
        result["permuted_metrics"] = permuted_metrics.tolist()
    return result


def _generate_stratified_permutations(y, n_permutations, rng):
    """Generate stratified permutation indices that preserve class distribution.
    
    Parameters:
    -----------
    y : array-like
        Target labels
    n_permutations : int
        Number of permutations to generate
    rng : numpy.random.Generator
        Random number generator
    
    Returns:
    --------
    list of arrays
        List of permutation indices
    """
    import numpy as _np
    
    # Get unique classes and their indices
    unique_classes = _np.unique(y)
    class_indices = {cls: _np.where(y == cls)[0] for cls in unique_classes}
    
    perm_indices = []
    for _ in range(n_permutations):
        # Shuffle within each class, then concatenate
        perm_idx = _np.empty(len(y), dtype=int)
        for cls, indices in class_indices.items():
            shuffled = rng.permutation(indices)
            perm_idx[indices] = shuffled
        perm_indices.append(perm_idx)
    
    return perm_indices


def _compute_permuted_metrics_sequential(
    model, X_a, y_a, y_pred, metric, perm_indices, null_method, predict_fn
) -> List[float]:
    """Compute permuted metrics sequentially."""
    import numpy as _np
    from copy import deepcopy
    
    permuted_metrics = []
    for perm_idx in perm_indices:
        y_perm = y_a[perm_idx]
        
        if null_method == "permute":
            # Fast: just evaluate metric with permuted labels
            try:
                m = float(metric(y_perm, y_pred))
            except Exception:
                m = float(metric(_np.array(y_perm), _np.array(y_pred)))
        else:  # retrain
            # Conservative: retrain model on permuted data
            model_copy = deepcopy(model)
            model_copy.fit(X_a, y_perm)
            y_pred_perm = predict_fn(X_a) if predict_fn == model.predict or predict_fn == model.predict_proba else model_copy.predict(X_a)
            m = float(metric(y_perm, y_pred_perm))
        
        permuted_metrics.append(m)
    
    return permuted_metrics


def _compute_permuted_metrics_parallel(
    model, X_a, y_a, y_pred, metric, perm_indices, null_method, predict_fn, n_jobs, backend
) -> List[float]:
    """Compute permuted metrics in parallel using joblib."""
    try:
        from joblib import Parallel, delayed
    except ImportError:
        warnings.warn(
            "joblib not available. Falling back to sequential execution. "
            "Install joblib for parallel processing: pip install joblib",
            UserWarning
        )
        return _compute_permuted_metrics_sequential(
            model, X_a, y_a, y_pred, metric, perm_indices, null_method, predict_fn
        )
    
    import numpy as _np
    from copy import deepcopy
    
    def _compute_single_permutation(perm_idx):
        """Compute metric for a single permutation."""
        y_perm = y_a[perm_idx]
        
        if null_method == "permute":
            try:
                return float(metric(y_perm, y_pred))
            except Exception:
                return float(metric(_np.array(y_perm), _np.array(y_pred)))
        else:  # retrain
            model_copy = deepcopy(model)
            model_copy.fit(X_a, y_perm)
            if predict_fn == model.predict:
                y_pred_perm = model_copy.predict(X_a)
            elif predict_fn == model.predict_proba:
                y_pred_perm = model_copy.predict_proba(X_a)
            else:
                y_pred_perm = model_copy.decision_function(X_a)
            return float(metric(y_perm, y_pred_perm))
    
    # Determine joblib backend
    if backend == "processes":
        joblib_backend = "loky"  # Better than multiprocessing for pickling
    else:
        joblib_backend = "threading"
    
    # Execute in parallel
    permuted_metrics = Parallel(n_jobs=n_jobs, backend=joblib_backend)(
        delayed(_compute_single_permutation)(perm_idx) for perm_idx in perm_indices
    )
    
    return permuted_metrics


def _compute_pvalue_ci(p_value: float, n_permutations: int, confidence_level: float) -> tuple:
    """Compute confidence interval for p-value using Wilson score interval.
    
    Parameters:
    -----------
    p_value : float
        Observed p-value
    n_permutations : int
        Number of permutations
    confidence_level : float
        Confidence level (e.g., 0.95)
    
    Returns:
    --------
    tuple
        (lower_bound, upper_bound) for p-value
    """
    from scipy import stats
    
    # Number of permuted metrics >= observed
    k = int(p_value * (n_permutations + 1)) - 1
    k = max(0, k)  # Ensure non-negative
    n = n_permutations
    
    # Wilson score interval for binomial proportion
    z = stats.norm.ppf((1 + confidence_level) / 2)
    
    denominator = 1 + z**2 / n
    center = (k + z**2 / 2) / (n + z**2)
    margin = z * np.sqrt((k * (n - k) / n + z**2 / 4) / (n + z**2))
    
    lower = max(0.0, (center - margin) / denominator)
    upper = min(1.0, (center + margin) / denominator)
    
    return (float(lower), float(upper))
