# CBDModel Protocol (Detailed)

The CBDModel protocol defines the minimal interface required for objects to be evaluated by the `detect_bias` function.

## Requirements

### Required Methods
- **`predict(X) -> y_pred`**: Must return predictions (numpy array-like)

### Optional Methods
- **`predict_proba(X) -> probs`**: For probabilistic metrics (e.g., log loss, ROC AUC)

## Usage Patterns

### Direct Usage
Directly pass objects that implement `predict`:

```python
class MyCustomModel:
    def predict(self, X):
        # Your prediction logic
        return predictions

model = MyCustomModel()
result = detect_bias(model, X_test, y_test, metric=accuracy_score)
```

### Scikit-learn Wrapper
Wrap scikit-learn estimators with `SklearnCBDModel` for convenience:

```python
from cbd.adapters.sklearn_adapter import SklearnCBDModel
from sklearn.linear_model import LogisticRegression

est = LogisticRegression().fit(X_train, y_train)
model = SklearnCBDModel(est)
res = detect_bias(model, X_test, y_test, metric=accuracy_score)
```

## Example Implementation

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class CBDModel(Protocol):
    """Protocol for models usable by detect_bias."""
    
    def predict(self, X):
        """
        Generate predictions for input data.
        
        Parameters
        ----------
        X : array-like
            Input features
            
        Returns
        -------
        y_pred : array-like
            Predicted labels or values
        """
        ...
    
    def predict_proba(self, X):
        """
        Generate probability predictions (optional).
        
        Parameters
        ----------
        X : array-like
            Input features
            
        Returns
        -------
        probs : array-like
            Predicted probabilities
        """
        ...
```

## Integration with Other Frameworks

### PyTorch Models
```python
class TorchCBDModel:
    def __init__(self, torch_model, device='cpu'):
        self.model = torch_model
        self.device = device
        
    def predict(self, X):
        import torch
        self.model.eval()
        with torch.no_grad():
            X_tensor = torch.tensor(X, dtype=torch.float32).to(self.device)
            outputs = self.model(X_tensor)
            return outputs.cpu().numpy()
```

### TensorFlow/Keras Models
```python
class KerasCBDModel:
    def __init__(self, keras_model):
        self.model = keras_model
        
    def predict(self, X):
        return self.model.predict(X)
    
    def predict_proba(self, X):
        return self.model.predict(X)
```

## Best Practices

1. **Stateless Predictions**: The `predict` method should be stateless and deterministic for the same input
2. **Array Compatibility**: Return numpy arrays or array-like objects
3. **Shape Consistency**: Output shape should match the expected format for your metric
4. **Error Handling**: Raise clear exceptions for invalid inputs

## See Also

- [detect_bias API documentation](detect_bias.md)
- [Sklearn adapter source](../cbd/adapters/sklearn_adapter.py)
- [Examples](../examples/)
