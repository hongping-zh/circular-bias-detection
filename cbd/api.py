"""Core API: CBDModel protocol and detect_bias implementation (permutation test)."""
from typing import Protocol, runtime_checkable, Optional, Callable, Any, Dict, List
import numpy as np
from copy import deepcopy

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

def _ensure_predict(model):
    if not hasattr(model, "predict"):
        raise ValueError("Model must implement predict(X)")

def detect_bias(model: CBDModel,
                X,
                y,
                metric: MetricFn,
                n_permutations: int = 1000,
                random_state: Optional[int] = None,
                return_permutations: bool = False) -> Dict[str, Any]:
    """
    Perform a permutation test to detect unusually high metric values that could indicate circular bias.
    - model: object implementing predict(X)
    - X, y: numpy arrays or pandas-like
    - metric: callable(y_true, y_pred) -> float
    - n_permutations: number of label shuffles for null distribution
    - random_state: seed
    Returns a dict with observed metric, p-value, permuted metrics, and conclusion.
    """
    import numpy as _np
    from sklearn.utils import shuffle

    _ensure_predict(model)

    rng = _np.random.RandomState(random_state)

    # ensure arrays
    X_a = X
    y_a = y

    y_pred = model.predict(X_a)
    observed = float(metric(y_a, y_pred))

    permuted_metrics: List[float] = []
    for i in range(n_permutations):
        y_perm = shuffle(y_a, random_state=rng)
        try:
            # If model is stateful to training data, we keep it unchanged and just compute metric vs permuted labels.
            # This tests whether the model's predictions align with labels beyond chance.
            m = float(metric(y_perm, y_pred))
        except Exception:
            # fallback: if metric expects (y_true, y_pred) types, convert to numpy
            m = float(metric(_np.array(y_perm), _np.array(y_pred)))
        permuted_metrics.append(m)

    # p-value: fraction of permuted metrics >= observed (one-sided test)
    permuted_metrics = _np.array(permuted_metrics)
    p_value = float((_np.sum(permuted_metrics >= observed) + 1) / (n_permutations + 1))

    alpha = 0.05
    if p_value <= alpha:
        conclusion = f"Suspicious: p <= {alpha} — potential circular bias detected"
    else:
        conclusion = f"No strong evidence of circular bias (p = {p_value:.3f})"

    result = {
        "observed_metric": observed,
        "p_value": p_value,
        "n_permutations": n_permutations,
        "conclusion": conclusion
    }
    if return_permutations:
        result["permuted_metrics"] = permuted_metrics.tolist()
    return result
