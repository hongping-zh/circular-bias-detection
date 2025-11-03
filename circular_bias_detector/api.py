from typing import Protocol, runtime_checkable, Optional, Union, Dict, Any
import numpy as np
import pandas as pd

@runtime_checkable
class ModelProtocol(Protocol):
    def predict(self, X: Union[np.ndarray, pd.DataFrame]) -> Union[np.ndarray, pd.Series, list]:
        ...
    def predict_proba(self, X: Union[np.ndarray, pd.DataFrame]) -> Any:
        ...

def _to_array(a: Union[np.ndarray, pd.DataFrame, pd.Series, list]) -> np.ndarray:
    if isinstance(a, pd.DataFrame) or isinstance(a, pd.Series):
        return a.to_numpy()
    return np.asarray(a)

def detect_bias(
    model: ModelProtocol,
    X: Union[np.ndarray, pd.DataFrame],
    y: Optional[Union[np.ndarray, pd.Series]] = None,
    metric: str = 'accuracy',
) -> Dict[str, Any]:
    X_arr = _to_array(X)
    y_pred = _to_array(model.predict(X_arr))
    result: Dict[str, Any] = {
        'predictions': y_pred.tolist() if isinstance(y_pred, np.ndarray) else list(y_pred),
        'metric': metric,
    }
    if hasattr(model, 'predict_proba'):
        try:
            proba = model.predict_proba(X_arr)
            proba_arr = _to_array(proba)
            result['probabilities'] = proba_arr.tolist()
        except Exception:
            pass
    if y is not None:
        y_true = _to_array(y)
        if metric == 'accuracy':
            score = float((y_pred == y_true).mean())
        else:
            raise ValueError(f"Unsupported metric: {metric}")
        result['score'] = score
    return result
