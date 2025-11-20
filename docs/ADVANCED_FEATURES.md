# Advanced Features Guide

This guide covers the advanced features added in v1.5.0+ for enhanced bias detection.

## Table of Contents

1. [Parallel Permutation Testing](#parallel-permutation-testing)
2. [Retrain-Null Testing](#retrain-null-testing)
3. [Probability-Based Metrics](#probability-based-metrics)
4. [Adaptive Permutation Testing](#adaptive-permutation-testing)
5. [Performance Optimization](#performance-optimization)
6. [Visualization and Model Cards](#visualization-and-model-cards)

---

## Parallel Permutation Testing

### Overview

The new permutation testing module supports parallel processing with configurable backends and proper random number generation for reproducibility.

### Features

- **Configurable backends**: Choose between `threads` (default) or `processes`
- **Reproducible RNG**: Pre-generated seeds ensure identical results across runs
- **Thread-safe**: No race conditions with shared random state
- **Efficient**: Scales well with multiple cores

### Basic Usage

```python
from circular_bias_detector.core.permutation import permutation_test
from circular_bias_detector.core.metrics import compute_psi
import numpy as np

# Your data
perf_matrix = np.random.rand(20, 5)
const_matrix = np.random.rand(20, 3)

# Run permutation test with parallelism
results = permutation_test(
    perf_matrix, const_matrix, compute_psi,
    n_permutations=1000,
    random_seed=42,        # For reproducibility
    n_jobs=-1,             # Use all CPU cores
    backend='threads'      # or 'processes'
)

print(f"p-value: {results['p_value']:.4f}")
print(f"95% CI: [{results['ci_lower']:.4f}, {results['ci_upper']:.4f}]")
```

### Backend Selection

#### Threads (Recommended)

```python
results = permutation_test(
    perf_matrix, const_matrix, metric_func,
    n_jobs=4,
    backend='threads'  # Default
)
```

**Pros:**
- Lower overhead
- Good for I/O-bound operations
- Works with most metric functions

**Cons:**
- Subject to Python GIL for pure Python code
- May not scale linearly for CPU-bound tasks

#### Processes

```python
results = permutation_test(
    perf_matrix, const_matrix, metric_func,
    n_jobs=4,
    backend='processes'
)
```

**Pros:**
- True parallelism (bypasses GIL)
- Better for CPU-intensive metrics

**Cons:**
- Higher overhead (process spawning)
- Requires picklable objects
- More memory usage

### Reproducibility

The implementation ensures reproducibility through pre-generated random seeds:

```python
# These will produce identical results
results1 = permutation_test(..., random_seed=42, n_jobs=1)
results2 = permutation_test(..., random_seed=42, n_jobs=4)

assert results1['p_value'] == results2['p_value']
```

---

## Retrain-Null Testing

### Overview

Retrain-null testing provides a more conservative permutation test by retraining the model on each permuted dataset. This is computationally expensive but more rigorous.

### When to Use

- **High-stakes decisions**: When you need maximum confidence
- **Small datasets**: Where overfitting is a concern
- **Model-dependent bias**: When bias might be in the model itself

### Usage

```python
from circular_bias_detector.core.permutation import retrain_null_test
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Define model factory (returns new untrained model)
def model_factory():
    return RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42
    )

# Run retrain-null test
results = retrain_null_test(
    X_train, y_train,
    X_test, y_test,
    model_factory=model_factory,
    metric_func=accuracy_score,
    n_permutations=100,      # Keep low (expensive!)
    random_seed=42,
    n_jobs=-1,               # Parallelism highly recommended
    backend='processes'      # Processes better for model training
)

print(f"Observed accuracy: {results['observed']:.4f}")
print(f"p-value: {results['p_value']:.4f}")
```

### Stratified Permutation

For imbalanced datasets, use stratified permutation:

```python
# Stratify by class labels
results = retrain_null_test(
    X_train, y_train, X_test, y_test,
    model_factory=model_factory,
    metric_func=accuracy_score,
    stratify_groups=y_train,  # Preserve class distribution
    n_permutations=100
)
```

### Cost Considerations

**Example timing:**
- Model training time: 1 second
- n_permutations: 100
- Sequential: ~100 seconds
- Parallel (8 cores): ~12-15 seconds

**Recommendations:**
- Start with `n_permutations=50-100`
- Use `n_jobs=-1` for parallelism
- Consider adaptive testing for large-scale experiments

---

## Probability-Based Metrics

### Overview

The new metrics utilities module provides automatic handling of probability-based metrics (AUC, log loss) vs prediction-based metrics (accuracy, F1).

### Automatic Detection

```python
from circular_bias_detector.metrics_utils import create_metric_wrapper
from sklearn.metrics import roc_auc_score, accuracy_score

# Automatically detects probability requirement
auc_wrapper = create_metric_wrapper(roc_auc_score)
print(auc_wrapper.requires_proba)  # True

acc_wrapper = create_metric_wrapper(accuracy_score)
print(acc_wrapper.requires_proba)  # False
```

### Using with Models

```python
from circular_bias_detector.metrics_utils import MetricWrapper
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Wrapper handles predict_proba automatically
wrapper = MetricWrapper(roc_auc_score, requires_proba=True)
score = wrapper(y_test, model, X_test)
```

### Compatibility Checking

```python
from circular_bias_detector.metrics_utils import validate_metric_compatibility
from sklearn.svm import SVC

# Check if model supports metric
model = SVC(kernel='linear')  # No predict_proba by default
compatible, msg = validate_metric_compatibility(model, 'auc')

if not compatible:
    print(f"Warning: {msg}")
    # Use model with probability=True
    model = SVC(kernel='linear', probability=True)
```

### Supported Metrics

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
- `mean_absolute_error` / `'mae'`
- `r2_score` / `'r2'`

### Fallback Behavior

When `predict_proba` is unavailable, the wrapper attempts to use `decision_function`:

```python
from sklearn.svm import SVC

model = SVC(kernel='linear')  # No predict_proba
model.fit(X_train, y_train)

# Will use decision_function with warning
wrapper = MetricWrapper(roc_auc_score, requires_proba=True)
score = wrapper(y_test, model, X_test)  # Works, with warning
```

---

## Adaptive Permutation Testing

### Overview

Adaptive permutation testing automatically stops when the p-value estimate has converged, saving computation time.

### Usage

```python
from circular_bias_detector.core.permutation import adaptive_permutation_test

results = adaptive_permutation_test(
    perf_matrix, const_matrix, compute_psi,
    max_permutations=10000,   # Maximum to run
    min_permutations=100,     # Minimum before checking convergence
    precision=0.01,           # Stop when SE(p-value) < 0.01
    random_seed=42,
    n_jobs=-1
)

print(f"Converged: {results['converged']}")
print(f"Permutations used: {results['n_permutations']} / {results['max_permutations']}")
print(f"p-value: {results['p_value']:.4f}")
```

### How It Works

1. Run `min_permutations` permutations
2. Compute standard error of p-value: SE = √(p(1-p)/n)
3. If SE < `precision`, stop (converged)
4. Otherwise, run more permutations in batches
5. Repeat until converged or `max_permutations` reached

### Benefits

- **Efficiency**: Stops early when estimate is stable
- **Accuracy**: Ensures sufficient precision
- **Adaptive**: Runs more permutations only when needed

### Example Savings

```python
# Standard test
standard_results = permutation_test(..., n_permutations=10000)
# Always runs 10,000 permutations

# Adaptive test
adaptive_results = adaptive_permutation_test(
    ..., max_permutations=10000, precision=0.01
)
# Might converge at 500 permutations → 20x speedup!
```

---

## Performance Optimization

### Subsampling for Large Datasets

For very large datasets, consider subsampling:

```python
import numpy as np

# Subsample data
n_samples = 1000
indices = np.random.choice(len(perf_matrix), size=n_samples, replace=False)
perf_subsample = perf_matrix[indices]
const_subsample = const_matrix[indices]

# Run test on subsample
results = permutation_test(
    perf_subsample, const_subsample, compute_psi,
    n_permutations=1000,
    n_jobs=-1
)
```

### Recommended Settings

| Dataset Size | n_permutations | n_jobs | backend | Expected Time |
|--------------|----------------|--------|---------|---------------|
| Small (<100) | 1000-5000 | 1-2 | threads | <1 min |
| Medium (100-1000) | 1000-2000 | 4-8 | threads | 1-5 min |
| Large (>1000) | 500-1000 | -1 | threads | 5-15 min |
| Very Large | Use adaptive | -1 | threads | Variable |

### Memory Considerations

```python
# For memory-constrained environments
results = permutation_test(
    perf_matrix, const_matrix, metric_func,
    n_permutations=500,  # Fewer permutations
    n_jobs=2,            # Fewer parallel jobs
    backend='threads'    # Lower memory overhead
)
```

---

## Visualization and Model Cards

### Permutation Distribution Plots

See the [permutation_visualization.ipynb](../examples/permutation_visualization.ipynb) notebook for interactive examples.

```python
import matplotlib.pyplot as plt

# Run test
results = permutation_test(perf_matrix, const_matrix, compute_psi, n_permutations=1000)

# Plot distribution
plt.hist(results['permuted_values'], bins=50, alpha=0.7, density=True)
plt.axvline(results['observed'], color='red', linestyle='--', label='Observed')
plt.axvline(results['ci_lower'], color='orange', linestyle=':', label='95% CI')
plt.axvline(results['ci_upper'], color='orange', linestyle=':')
plt.xlabel('PSI Score')
plt.ylabel('Density')
plt.legend()
plt.title(f"Permutation Test (p={results['p_value']:.4f})")
plt.show()
```

### Model Card Generation

Generate audit-ready model cards:

```python
def generate_model_card(results_dict):
    card = f"""
# Bias Detection Model Card

## Statistical Testing
- Method: Permutation Test
- Permutations: {results_dict['n_permutations']}
- p-value: {results_dict['p_value']:.4f}

## Results
- Observed: {results_dict['observed']:.4f}
- 95% CI: [{results_dict['ci_lower']:.4f}, {results_dict['ci_upper']:.4f}]
- Interpretation: {'Significant' if results_dict['p_value'] < 0.05 else 'Not significant'}

## Recommendations
{'⚠️ Review evaluation methodology' if results_dict['p_value'] < 0.05 else '✅ No action needed'}
"""
    return card

# Generate and save
card = generate_model_card(results)
with open('model_card.md', 'w') as f:
    f.write(card)
```

---

## Best Practices

### 1. Always Set Random Seed

```python
# For reproducibility
results = permutation_test(..., random_seed=42)
```

### 2. Start with Threads

```python
# Default to threads unless you have a specific reason
results = permutation_test(..., backend='threads')
```

### 3. Use Adaptive for Exploration

```python
# When you don't know how many permutations you need
results = adaptive_permutation_test(
    ..., max_permutations=10000, precision=0.01
)
```

### 4. Validate Metric Compatibility

```python
# Before running expensive tests
compatible, msg = validate_metric_compatibility(model, metric)
if not compatible:
    raise ValueError(msg)
```

### 5. Save Results

```python
import json

# Save for later analysis
with open('results.json', 'w') as f:
    json.dump({
        'observed': results['observed'],
        'p_value': results['p_value'],
        'ci_lower': results['ci_lower'],
        'ci_upper': results['ci_upper'],
        'n_permutations': results['n_permutations']
    }, f, indent=2)
```

---

## Troubleshooting

### Issue: Slow Performance

**Solution:**
1. Reduce `n_permutations`
2. Increase `n_jobs`
3. Use adaptive testing
4. Consider subsampling

### Issue: Pickle Errors with Processes

**Solution:**
```python
# Use threads instead
results = permutation_test(..., backend='threads')

# Or ensure metric_func is picklable
# (defined at module level, not as lambda)
```

### Issue: Inconsistent Results

**Solution:**
```python
# Always set random_seed
results = permutation_test(..., random_seed=42)
```

### Issue: Model Doesn't Support predict_proba

**Solution:**
```python
# Option 1: Enable probability estimates
model = SVC(probability=True)

# Option 2: Use prediction-based metric
wrapper = create_metric_wrapper(accuracy_score)  # Doesn't need proba

# Option 3: Accept decision_function fallback
# (will work but with warning)
```

---

## API Reference

See individual module documentation:
- [`circular_bias_detector.core.permutation`](../circular_bias_detector/core/permutation.py)
- [`circular_bias_detector.metrics_utils`](../circular_bias_detector/metrics_utils.py)

## Examples

- [Basic Permutation Testing](../examples/permutation_visualization.ipynb)
- [Retrain-Null Testing](../examples/retrain_null_example.py)
- [Metric Utilities](../examples/metrics_utils_example.py)

---

**Questions or Issues?**

- GitHub Issues: https://github.com/hongping-zh/circular-bias-detection/issues
- Documentation: https://github.com/hongping-zh/circular-bias-detection#readme
