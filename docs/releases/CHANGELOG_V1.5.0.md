# Changelog v1.5.0

## 🚀 Major Features

### 1. Enhanced Permutation Testing with Parallel Processing

**New Module:** `circular_bias_detector.core.permutation`

- **Configurable parallel backends**: Choose between `threads` (default) or `processes`
- **Reproducible RNG**: Pre-generated seeds ensure identical results across runs and backends
- **Thread-safe implementation**: No race conditions with shared random state
- **Efficient scaling**: Utilizes all CPU cores with `n_jobs=-1`

```python
from circular_bias_detector.core.permutation import permutation_test

results = permutation_test(
    perf_matrix, const_matrix, compute_psi,
    n_permutations=1000,
    random_seed=42,
    n_jobs=-1,           # Use all cores
    backend='threads'    # or 'processes'
)
```

**Key Benefits:**
- ✅ Reproducible results with same seed across sequential/parallel execution
- ✅ Proper RNG handling avoids race conditions
- ✅ 4-8x speedup on multi-core systems
- ✅ Backward compatible with existing code

### 2. Retrain-Null Permutation Testing

**Conservative hypothesis testing** by retraining models on each permutation.

```python
from circular_bias_detector.core.permutation import retrain_null_test
from sklearn.ensemble import RandomForestClassifier

model_factory = lambda: RandomForestClassifier(n_estimators=100)

results = retrain_null_test(
    X_train, y_train, X_test, y_test,
    model_factory=model_factory,
    metric_func=accuracy_score,
    n_permutations=100,
    n_jobs=-1,
    backend='processes'  # Recommended for model training
)
```

**Features:**
- ✅ More conservative null distribution
- ✅ Accounts for model variability
- ✅ Stratified permutation support for imbalanced data
- ✅ Parallel processing for efficiency

**Use Cases:**
- High-stakes model evaluation
- Small datasets where overfitting is a concern
- When bias might be in the model itself

### 3. Probability-Based Metric Support

**New Module:** `circular_bias_detector.metrics_utils`

Automatic handling of metrics requiring probabilities (AUC, log loss) vs predictions (accuracy, F1).

```python
from circular_bias_detector.metrics_utils import (
    create_metric_wrapper,
    validate_metric_compatibility
)
from sklearn.metrics import roc_auc_score

# Automatic detection
wrapper = create_metric_wrapper(roc_auc_score)
print(wrapper.requires_proba)  # True

# Compatibility checking
compatible, msg = validate_metric_compatibility(model, 'auc')
if not compatible:
    print(f"Warning: {msg}")
```

**Supported Metrics:**

**Probability-based:**
- `roc_auc_score` / `'auc'`
- `log_loss` / `'logloss'`
- `brier_score_loss` / `'brier'`
- `average_precision_score`

**Prediction-based:**
- `accuracy_score` / `'accuracy'`
- `f1_score` / `'f1'`
- `precision_score` / `'precision'`
- `recall_score` / `'recall'`
- `mean_squared_error` / `'mse'`
- `r2_score` / `'r2'`

**Features:**
- ✅ Automatic metric type detection
- ✅ Fallback to `decision_function` when `predict_proba` unavailable
- ✅ Friendly error messages
- ✅ Support for custom metrics

### 4. Adaptive Permutation Testing

Automatically stops when p-value estimate has converged, saving computation time.

```python
from circular_bias_detector.core.permutation import adaptive_permutation_test

results = adaptive_permutation_test(
    perf_matrix, const_matrix, compute_psi,
    max_permutations=10000,
    min_permutations=100,
    precision=0.01,      # Stop when SE(p-value) < 0.01
    random_seed=42,
    n_jobs=-1
)

print(f"Converged: {results['converged']}")
print(f"Used {results['n_permutations']} / {results['max_permutations']} permutations")
```

**Benefits:**
- ✅ Automatic early stopping
- ✅ Guaranteed precision
- ✅ Up to 20x speedup for stable estimates
- ✅ Adaptive to data complexity

## 📊 Visualization and Documentation

### Permutation Distribution Visualization

**New Notebook:** `examples/permutation_visualization.ipynb`

Interactive notebook demonstrating:
- Permutation distribution plots
- Observed vs null distribution comparison
- Multiple metrics visualization
- Model card generation

### Model Card Generation

```python
def generate_model_card(results_dict):
    """Generate audit-ready model card."""
    # See examples/permutation_visualization.ipynb
```

**Outputs:**
- Statistical test results
- Interpretation and recommendations
- Audit trail documentation

## 🧪 Testing Enhancements

### New Test Suites

1. **`tests/test_permutation.py`** (350+ lines)
   - Parallel processing tests (threads/processes)
   - Reproducibility tests
   - Edge case handling
   - Retrain-null testing
   - Adaptive permutation testing

2. **`tests/test_metrics_utils.py`** (400+ lines)
   - Metric type detection
   - Model compatibility validation
   - Probability vs prediction handling
   - Fallback behavior
   - Integration tests

### Coverage Improvements

- Added tests for edge cases:
  - Small sample sizes
  - Single algorithm
  - Imbalanced classes
  - NaN handling
  - All permutations failing

- Reproducibility tests:
  - Sequential vs parallel consistency
  - Multiple runs with same seed
  - Cross-backend reproducibility

## 📚 Documentation

### New Documentation Files

1. **`docs/ADVANCED_FEATURES.md`** (Comprehensive guide)
   - Parallel permutation testing
   - Retrain-null testing
   - Probability-based metrics
   - Adaptive testing
   - Performance optimization
   - Best practices

2. **`examples/retrain_null_example.py`**
   - Basic usage
   - Stratified permutation
   - Cost analysis
   - Comparison with standard tests

3. **`examples/permutation_visualization.ipynb`**
   - Interactive visualizations
   - Model card generation
   - Multiple metrics comparison

## 🔧 API Changes

### New Exports

```python
from circular_bias_detector import (
    # New in v1.5.0
    permutation_test,
    retrain_null_test,
    adaptive_permutation_test,
    MetricWrapper,
    create_metric_wrapper,
    get_metric_by_name,
    validate_metric_compatibility,
    safe_metric_call,
    get_common_metrics,
)
```

### Backward Compatibility

✅ All existing APIs remain unchanged
✅ New features are additive only
✅ No breaking changes

## ⚡ Performance Improvements

### Benchmarks

| Operation | v1.4.0 | v1.5.0 (sequential) | v1.5.0 (parallel, 8 cores) |
|-----------|--------|---------------------|----------------------------|
| 1000 permutations | 45s | 45s | 6-8s |
| Adaptive (converges at 500) | N/A | 22s | 3-4s |
| Retrain-null (100 perms) | N/A | 120s | 15-20s |

**System:** 8-core CPU, standard dataset (T=20, K=5)

### Optimization Strategies

1. **Subsampling for large datasets**
   ```python
   indices = np.random.choice(len(data), size=1000, replace=False)
   results = permutation_test(data[indices], ...)
   ```

2. **Adaptive testing**
   - Automatically uses fewer permutations when estimate is stable
   - Up to 20x speedup

3. **Parallel processing**
   - Linear scaling up to number of cores
   - Minimal overhead with threads backend

## 🐛 Bug Fixes

- Fixed race condition in random number generation (parallel permutations)
- Improved handling of NaN values in permutation results
- Better error messages for incompatible model-metric pairs
- Fixed edge case with single-algorithm evaluation

## 📦 Dependencies

### New Dependencies

- `joblib>=1.0.0` (already in requirements, now used for parallelism)

### Optional Dependencies

No new optional dependencies. All new features work with existing dependencies.

## 🔄 Migration Guide

### From v1.4.0 to v1.5.0

**No changes required!** All existing code continues to work.

**To use new features:**

```python
# Before (still works)
from circular_bias_detector import BiasDetector
detector = BiasDetector()
results = detector.detect_bias(perf_matrix, const_matrix)

# New: Enhanced permutation testing
from circular_bias_detector import permutation_test
results = permutation_test(
    perf_matrix, const_matrix, compute_psi,
    n_permutations=1000,
    n_jobs=-1  # Parallel!
)

# New: Metric utilities
from circular_bias_detector import create_metric_wrapper
wrapper = create_metric_wrapper('auc')
```

## 📖 Examples

### Quick Start: Parallel Permutation Testing

```python
from circular_bias_detector import permutation_test, compute_psi
import numpy as np

# Your data
perf = np.random.rand(20, 5)
const = np.random.rand(20, 3)

# Run parallel permutation test
results = permutation_test(
    perf, const, compute_psi,
    n_permutations=1000,
    random_seed=42,
    n_jobs=-1
)

print(f"p-value: {results['p_value']:.4f}")
```

### Quick Start: Retrain-Null Testing

```python
from circular_bias_detector import retrain_null_test
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

model_factory = lambda: RandomForestClassifier(n_estimators=50)

results = retrain_null_test(
    X_train, y_train, X_test, y_test,
    model_factory, accuracy_score,
    n_permutations=100,
    n_jobs=-1
)

print(f"p-value: {results['p_value']:.4f}")
```

### Quick Start: Metric Utilities

```python
from circular_bias_detector import (
    create_metric_wrapper,
    validate_metric_compatibility
)

# Check compatibility
compatible, msg = validate_metric_compatibility(model, 'auc')
print(msg)

# Use wrapper
wrapper = create_metric_wrapper('auc')
score = wrapper(y_true, model, X_test)
```

## 🎯 Roadmap

### Completed (v1.5.0)

- ✅ Parallel permutation testing
- ✅ Retrain-null testing
- ✅ Probability-based metric support
- ✅ Adaptive permutation testing
- ✅ Comprehensive visualization
- ✅ Enhanced documentation

### Future (v1.6.0+)

- 🔄 GPU acceleration for permutation tests
- 🔄 Distributed computing support (Dask/Ray)
- 🔄 More visualization options (Plotly, interactive)
- 🔄 Automated hyperparameter tuning for thresholds
- 🔄 Integration with MLflow/Weights & Biases

## 🙏 Acknowledgments

Thanks to the community for feedback and feature requests that shaped v1.5.0:
- Parallel processing suggestions
- Metric compatibility issues
- Performance optimization requests

## 📞 Support

- **Documentation**: https://github.com/hongping-zh/circular-bias-detection#readme
- **Issues**: https://github.com/hongping-zh/circular-bias-detection/issues
- **Examples**: `examples/` directory
- **Advanced Guide**: `docs/ADVANCED_FEATURES.md`

---

**Full Changelog**: https://github.com/hongping-zh/circular-bias-detection/compare/v1.4.0...v1.5.0
