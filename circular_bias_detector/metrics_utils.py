"""
Utilities for handling different metric types and model prediction methods.

This module provides helpers for:
- Detecting metric requirements (probabilities vs predictions)
- Handling models with/without predict_proba
- Common metrics (AUC, logloss, accuracy, F1, etc.)
"""

import numpy as np
from typing import Callable, Optional, Union, Tuple, Any
import warnings


class MetricWrapper:
    """
    Wrapper for metrics that handles probability vs prediction requirements.
    
    Automatically detects if a metric requires probabilities and attempts to
    use predict_proba if available, falling back to predict or decision_function.
    """
    
    def __init__(
        self,
        metric_func: Callable,
        requires_proba: bool = False,
        name: Optional[str] = None
    ):
        """
        Initialize metric wrapper.
        
        Parameters
        ----------
        metric_func : callable
            Metric function with signature: func(y_true, y_pred) -> float
        requires_proba : bool, default=False
            Whether metric requires probability predictions
        name : str, optional
            Metric name for error messages
        """
        self.metric_func = metric_func
        self.requires_proba = requires_proba
        self.name = name or getattr(metric_func, '__name__', 'unknown_metric')
    
    def __call__(self, y_true: np.ndarray, model: Any, X: np.ndarray) -> float:
        """
        Compute metric using appropriate prediction method.
        
        Parameters
        ----------
        y_true : np.ndarray
            True labels
        model : object
            Trained model with predict/predict_proba/decision_function
        X : np.ndarray
            Input features
            
        Returns
        -------
        float
            Metric value
            
        Raises
        ------
        ValueError
            If metric requires probabilities but model doesn't support them
        """
        if self.requires_proba:
            y_pred = self._get_probabilities(model, X)
        else:
            y_pred = self._get_predictions(model, X)
        
        return self.metric_func(y_true, y_pred)
    
    def _get_probabilities(self, model: Any, X: np.ndarray) -> np.ndarray:
        """Get probability predictions from model."""
        if hasattr(model, 'predict_proba'):
            proba = model.predict_proba(X)
            # For binary classification, return positive class probability
            if proba.shape[1] == 2:
                return proba[:, 1]
            return proba
        elif hasattr(model, 'decision_function'):
            warnings.warn(
                f"Metric '{self.name}' requires probabilities but model has no "
                f"predict_proba. Using decision_function as fallback.",
                UserWarning
            )
            return model.decision_function(X)
        else:
            raise ValueError(
                f"Metric '{self.name}' requires probabilities but model has neither "
                f"predict_proba nor decision_function methods."
            )
    
    def _get_predictions(self, model: Any, X: np.ndarray) -> np.ndarray:
        """Get class predictions from model."""
        if hasattr(model, 'predict'):
            return model.predict(X)
        else:
            raise ValueError(f"Model has no predict method for metric '{self.name}'")


def detect_metric_type(metric_func: Callable) -> str:
    """
    Detect if a metric requires probabilities or predictions.
    
    Parameters
    ----------
    metric_func : callable
        Metric function
        
    Returns
    -------
    str
        'proba' if requires probabilities, 'pred' otherwise
    """
    metric_name = getattr(metric_func, '__name__', '').lower()
    
    # Known probability-based metrics
    proba_metrics = {
        'roc_auc', 'auc', 'log_loss', 'logloss', 'brier_score',
        'average_precision', 'roc_curve', 'pr_curve'
    }
    
    for pm in proba_metrics:
        if pm in metric_name:
            return 'proba'
    
    return 'pred'


def create_metric_wrapper(
    metric_func: Union[Callable, str],
    requires_proba: Optional[bool] = None
) -> MetricWrapper:
    """
    Create a MetricWrapper from a metric function or name.
    
    Parameters
    ----------
    metric_func : callable or str
        Metric function or name ('auc', 'accuracy', 'f1', etc.)
    requires_proba : bool, optional
        Override automatic detection of probability requirement
        
    Returns
    -------
    MetricWrapper
        Wrapped metric
        
    Examples
    --------
    >>> from sklearn.metrics import roc_auc_score
    >>> wrapper = create_metric_wrapper(roc_auc_score)
    >>> # wrapper.requires_proba is True (auto-detected)
    
    >>> wrapper = create_metric_wrapper('accuracy')
    >>> # wrapper.requires_proba is False
    """
    if isinstance(metric_func, str):
        metric_func = get_metric_by_name(metric_func)
    
    if requires_proba is None:
        requires_proba = detect_metric_type(metric_func) == 'proba'
    
    return MetricWrapper(metric_func, requires_proba)


def get_metric_by_name(name: str) -> Callable:
    """
    Get metric function by name.
    
    Parameters
    ----------
    name : str
        Metric name (e.g., 'accuracy', 'auc', 'f1', 'mse')
        
    Returns
    -------
    callable
        Metric function
        
    Raises
    ------
    ValueError
        If metric name is not recognized
    """
    try:
        from sklearn import metrics as sk_metrics
    except ImportError:
        raise ImportError("scikit-learn required for metric lookup")
    
    name_lower = name.lower().replace('-', '_').replace(' ', '_')
    
    # Mapping of common names to sklearn functions
    metric_map = {
        'accuracy': sk_metrics.accuracy_score,
        'acc': sk_metrics.accuracy_score,
        'auc': sk_metrics.roc_auc_score,
        'roc_auc': sk_metrics.roc_auc_score,
        'log_loss': sk_metrics.log_loss,
        'logloss': sk_metrics.log_loss,
        'f1': sk_metrics.f1_score,
        'f1_score': sk_metrics.f1_score,
        'precision': sk_metrics.precision_score,
        'recall': sk_metrics.recall_score,
        'mse': sk_metrics.mean_squared_error,
        'mae': sk_metrics.mean_absolute_error,
        'r2': sk_metrics.r2_score,
        'brier': sk_metrics.brier_score_loss,
        'brier_score': sk_metrics.brier_score_loss,
    }
    
    if name_lower in metric_map:
        return metric_map[name_lower]
    
    # Try to get from sklearn.metrics directly
    if hasattr(sk_metrics, name_lower):
        return getattr(sk_metrics, name_lower)
    
    raise ValueError(
        f"Unknown metric: {name}. Available: {', '.join(metric_map.keys())}"
    )


def validate_metric_compatibility(
    model: Any,
    metric: Union[Callable, str, MetricWrapper],
    raise_error: bool = False
) -> Tuple[bool, str]:
    """
    Check if a model is compatible with a metric.
    
    Parameters
    ----------
    model : object
        Model to check
    metric : callable, str, or MetricWrapper
        Metric to validate
    raise_error : bool, default=False
        If True, raise error on incompatibility
        
    Returns
    -------
    compatible : bool
        Whether model and metric are compatible
    message : str
        Compatibility message or error description
        
    Examples
    --------
    >>> from sklearn.svm import SVC
    >>> from sklearn.metrics import roc_auc_score
    >>> model = SVC(kernel='linear')  # No predict_proba by default
    >>> compatible, msg = validate_metric_compatibility(model, roc_auc_score)
    >>> print(msg)
    """
    if isinstance(metric, str):
        metric = create_metric_wrapper(metric)
    elif not isinstance(metric, MetricWrapper):
        metric = create_metric_wrapper(metric)
    
    # Check basic predict
    if not hasattr(model, 'predict'):
        msg = "Model has no predict method"
        if raise_error:
            raise ValueError(msg)
        return False, msg
    
    # Check probability requirements
    if metric.requires_proba:
        if hasattr(model, 'predict_proba'):
            return True, "Model supports predict_proba (required)"
        elif hasattr(model, 'decision_function'):
            msg = (
                f"Metric '{metric.name}' requires probabilities. "
                f"Model has decision_function but not predict_proba. "
                f"Will use decision_function as fallback."
            )
            if raise_error:
                warnings.warn(msg, UserWarning)
            return True, msg
        else:
            msg = (
                f"Metric '{metric.name}' requires probabilities but model has "
                f"neither predict_proba nor decision_function"
            )
            if raise_error:
                raise ValueError(msg)
            return False, msg
    
    return True, "Model compatible with metric"


def safe_metric_call(
    metric: Union[Callable, str, MetricWrapper],
    y_true: np.ndarray,
    y_pred: np.ndarray,
    default_value: float = 0.0,
    **metric_kwargs
) -> float:
    """
    Safely call a metric function with error handling.
    
    Parameters
    ----------
    metric : callable, str, or MetricWrapper
        Metric function
    y_true : np.ndarray
        True labels
    y_pred : np.ndarray
        Predicted labels or probabilities
    default_value : float, default=0.0
        Value to return on error
    **metric_kwargs
        Additional arguments for metric
        
    Returns
    -------
    float
        Metric value or default_value on error
    """
    if isinstance(metric, str):
        metric = get_metric_by_name(metric)
    
    try:
        return float(metric(y_true, y_pred, **metric_kwargs))
    except Exception as e:
        warnings.warn(f"Metric computation failed: {e}. Returning {default_value}")
        return default_value


# Common pre-configured metric wrappers
def get_common_metrics() -> dict:
    """
    Get dictionary of common pre-configured metrics.
    
    Returns
    -------
    dict
        Dictionary mapping metric names to MetricWrapper instances
    """
    try:
        from sklearn import metrics as sk_metrics
    except ImportError:
        warnings.warn("scikit-learn not available. Cannot load common metrics.")
        return {}
    
    return {
        'accuracy': MetricWrapper(sk_metrics.accuracy_score, requires_proba=False, name='accuracy'),
        'auc': MetricWrapper(sk_metrics.roc_auc_score, requires_proba=True, name='auc'),
        'log_loss': MetricWrapper(sk_metrics.log_loss, requires_proba=True, name='log_loss'),
        'f1': MetricWrapper(sk_metrics.f1_score, requires_proba=False, name='f1'),
        'precision': MetricWrapper(sk_metrics.precision_score, requires_proba=False, name='precision'),
        'recall': MetricWrapper(sk_metrics.recall_score, requires_proba=False, name='recall'),
        'mse': MetricWrapper(sk_metrics.mean_squared_error, requires_proba=False, name='mse'),
        'mae': MetricWrapper(sk_metrics.mean_absolute_error, requires_proba=False, name='mae'),
        'r2': MetricWrapper(sk_metrics.r2_score, requires_proba=False, name='r2'),
    }


def example_usage():
    """Example usage of metric utilities."""
    print("=== Metric Utilities Example ===\n")
    
    try:
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.svm import SVC
        from sklearn.metrics import roc_auc_score, accuracy_score
        from sklearn.datasets import make_classification
        
        # Create sample data
        X, y = make_classification(n_samples=100, n_features=10, random_state=42)
        
        # Models with different capabilities
        rf = RandomForestClassifier(n_estimators=10, random_state=42)
        svc_no_proba = SVC(kernel='linear', random_state=42)  # No predict_proba by default
        svc_with_proba = SVC(kernel='linear', probability=True, random_state=42)
        
        rf.fit(X, y)
        svc_no_proba.fit(X, y)
        svc_with_proba.fit(X, y)
        
        # Check compatibility
        print("1. Compatibility checks:")
        for model, name in [(rf, 'RandomForest'), (svc_no_proba, 'SVC_no_proba'), 
                            (svc_with_proba, 'SVC_with_proba')]:
            compatible, msg = validate_metric_compatibility(model, roc_auc_score)
            print(f"   {name} + AUC: {compatible} - {msg}")
        
        print("\n2. Using MetricWrapper:")
        auc_wrapper = create_metric_wrapper(roc_auc_score)
        print(f"   AUC requires proba: {auc_wrapper.requires_proba}")
        
        acc_wrapper = create_metric_wrapper(accuracy_score)
        print(f"   Accuracy requires proba: {acc_wrapper.requires_proba}")
        
        print("\n3. Common metrics:")
        common = get_common_metrics()
        print(f"   Available: {list(common.keys())}")
        
    except ImportError as e:
        print(f"Example requires scikit-learn: {e}")


if __name__ == '__main__':
    example_usage()
