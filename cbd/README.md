# circular-bias-detection (CBD Package)

A lightweight Python toolkit to detect circular reasoning / data-leakage style bias in model evaluation. Provides a simple API (`CBDModel` protocol and `detect_bias`) and examples showing how to integrate with scikit-learn models and MLOps tooling.

[![CI](https://github.com/hongping-zh/circular-bias-detection/actions/workflows/cbd-ci.yml/badge.svg)](https://github.com/hongping-zh/circular-bias-detection/actions)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Quick Links
- **Repository**: https://github.com/hongping-zh/circular-bias-detection
- **Documentation**: [docs/](../docs/)
- **Examples**: [examples/quickstart.py](../examples/quickstart.py)
- **Web App**: https://is.gd/check_sleuth

## Overview

Circular reasoning bias arises when evaluation protocols inadvertently leak information from training or from the evaluation process back into the model, producing overly optimistic results. This package offers a reproducible statistical test (permutation-based) to flag suspiciously-high evaluation metrics that may indicate potential circular bias.

## Installation

### From Source (Editable)
```bash
git clone https://github.com/hongping-zh/circular-bias-detection.git
cd circular-bias-detection
pip install -e .
```

### Install with Examples Dependencies
```bash
pip install -e ".[dev]"
```

## Minimal Quickstart (Copy-Paste)

```python
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from cbd.api import detect_bias
from cbd.adapters.sklearn_adapter import SklearnCBDModel
from sklearn.metrics import accuracy_score

# Generate data
X, y = make_classification(n_samples=500, n_features=10, random_state=0)

# Train a model
clf = LogisticRegression(max_iter=1000).fit(X, y)

# Wrap into CBDModel
model = SklearnCBDModel(clf)

# Run bias detection (permutation test on accuracy)
result = detect_bias(
    model, X, y, 
    metric=lambda y_true, y_pred: accuracy_score(y_true, y_pred),
    n_permutations=500, 
    random_state=0
)

print("Observed metric:", result["observed_metric"])
print("p-value:", result["p_value"])
print("Conclusion:", result["conclusion"])
```

### Example Output
```
Observed metric: 0.86
p-value: 0.02
Conclusion: Suspicious: p <= 0.05 — potential circular bias detected
```

## API: CBDModel Protocol

See [docs/CBDModel.md](../docs/CBDModel.md) for full protocol documentation.

**Short summary**:
- A `CBDModel` is any object exposing:
  - `predict(X) -> y_pred` (required)
  - Optionally `predict_proba(X) -> probs` for probabilistic metrics
- `detect_bias(model, X, y, metric, ...)` accepts either such a model or a scikit-learn estimator wrapped with `SklearnCBDModel`

## detect_bias (High-Level API)

### Signature
```python
detect_bias(
    model: CBDModel,
    X,
    y,
    metric: Callable[[Any, Any], float],
    n_permutations: int = 1000,
    random_state: Optional[int] = None,
    return_permutations: bool = False
) -> Dict[str, Any]
```

### Returns
A dictionary with at least the following keys:
- `observed_metric`: float — metric evaluated on (X, y)
- `p_value`: float — permutation p-value
- `n_permutations`: int
- `permuted_metrics`: list[float] — (optional, if `return_permutations=True`)
- `conclusion`: str — human readable conclusion

### Parameters
- **model**: Object implementing `predict(X)` method
- **X**: Feature matrix (array-like)
- **y**: Target labels (array-like)
- **metric**: Callable that takes (y_true, y_pred) and returns a float
- **n_permutations**: Number of label permutations for null distribution (default: 1000)
- **random_state**: Random seed for reproducibility
- **return_permutations**: If True, include all permuted metrics in result

## Design Notes & Limitations

- **Permutation Testing**: Uses non-parametric permutation testing to estimate the null distribution of the metric when labels are independent of features. This is a general-purpose approach but may be expensive when `n_permutations` is large.

- **Interpretation**: A small p-value suggests the observed metric is unlikely under the null (labels independent), which could reflect strong signal **or** circular bias. Combine with reproducibility checks and dataset provenance audit.

- **Metric Flexibility**: Works for classification/regression metrics. The metric must accept `(y_true, y_pred)` and return a scalar.

- **Computational Cost**: O(n_permutations × prediction_time). For large datasets or expensive models, consider reducing `n_permutations` or using sampling.

## Examples

### Basic Classification
```python
from cbd import detect_bias, SklearnCBDModel
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score

clf = RandomForestClassifier().fit(X_train, y_train)
model = SklearnCBDModel(clf)

result = detect_bias(
    model, X_test, y_test,
    metric=lambda yt, yp: f1_score(yt, yp, average='weighted'),
    n_permutations=1000
)
```

### Regression
```python
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import r2_score

reg = GradientBoostingRegressor().fit(X_train, y_train)
model = SklearnCBDModel(reg)

result = detect_bias(
    model, X_test, y_test,
    metric=r2_score,
    n_permutations=500
)
```

### Custom Metric
```python
def custom_metric(y_true, y_pred):
    # Your custom metric logic
    return some_score

result = detect_bias(model, X, y, metric=custom_metric)
```

## Integration with MLOps

### MLflow
```python
import mlflow

with mlflow.start_run():
    # Train model
    clf = train_model(X_train, y_train)
    model = SklearnCBDModel(clf)
    
    # Detect bias
    result = detect_bias(model, X_test, y_test, metric=accuracy_score)
    
    # Log results
    mlflow.log_metric("bias_p_value", result["p_value"])
    mlflow.log_param("bias_conclusion", result["conclusion"])
```

### Weights & Biases
```python
import wandb

wandb.init(project="my-project")

result = detect_bias(model, X, y, metric=accuracy_score)
wandb.log({
    "bias/p_value": result["p_value"],
    "bias/observed_metric": result["observed_metric"]
})
```

## Testing

Run the test suite:
```bash
pytest tests/test_api.py -v
```

Run with coverage:
```bash
pytest tests/test_api.py --cov=cbd --cov-report=html
```

## Contributing

Please see [CONTRIBUTING.md](../CONTRIBUTING.md) for contribution guidelines.

Suggested areas:
- Additional adapters (PyTorch, TensorFlow, etc.)
- More sophisticated bias detection methods
- Performance optimizations
- Documentation improvements

## License

MIT License - see [LICENSE](../LICENSE) for details.

## Citation

If you use this package in your research, please cite:

```bibtex
@software{zhang2024cbd,
  author    = {Zhang, Hongping},
  title     = {Circular Bias Detection: A Statistical Framework for AI Evaluation},
  year      = {2024},
  publisher = {GitHub},
  url       = {https://github.com/hongping-zh/circular-bias-detection}
}
```

## Related Projects

- **Full Framework**: [circular-bias-detection](https://github.com/hongping-zh/circular-bias-detection) (includes CLI, web app, and advanced features)
- **Dataset**: [CBD Dataset v3/v3.1](https://doi.org/10.5281/zenodo.17637303)
- **Web App**: [Sleuth - AI Bias Hunter](https://is.gd/check_sleuth)

## Support

- **Issues**: https://github.com/hongping-zh/circular-bias-detection/issues
- **Discussions**: https://github.com/hongping-zh/circular-bias-detection/discussions
- **Email**: yujjam@uest.edu.gr
