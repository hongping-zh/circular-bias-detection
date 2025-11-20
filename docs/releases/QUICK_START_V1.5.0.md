# Quick Start Guide - CBD v1.5.0

**New to v1.5.0?** This guide gets you started with the enhanced features in 5 minutes.

## Installation

```bash
pip install circular-bias-detector
# or upgrade
pip install --upgrade circular-bias-detector
```

---

## 🚀 Feature 1: Parallel Permutation Testing

**Speed up your tests 4-8x with multi-core processing!**

### Before (v1.4.0)

```python
from circular_bias_detector import BiasDetector

detector = BiasDetector()
results = detector.detect_bias(perf_matrix, const_matrix)
# Sequential only, no parallelism
```

### After (v1.5.0)

```python
from circular_bias_detector import permutation_test, compute_psi

results = permutation_test(
    perf_matrix, const_matrix, compute_psi,
    n_permutations=1000,
    random_seed=42,      # Reproducible!
    n_jobs=-1,           # Use all CPU cores
    backend='threads'    # Fast and safe
)

print(f"p-value: {results['p_value']:.4f}")
print(f"95% CI: [{results['ci_lower']:.4f}, {results['ci_upper']:.4f}]")
```

**Key Benefits:**
- ⚡ 4-8x faster on multi-core systems
- 🔒 Reproducible results with same seed
- 🧵 Thread-safe, no race conditions

---

## 🔬 Feature 2: Retrain-Null Testing

**Conservative hypothesis testing for high-stakes decisions.**

### When to Use

- ✅ High-stakes model evaluation
- ✅ Small datasets (overfitting concerns)
- ✅ Need maximum confidence

### Example

```python
from circular_bias_detector import retrain_null_test
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Define how to create a fresh model
def model_factory():
    return RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42
    )

# Run conservative test
results = retrain_null_test(
    X_train, y_train,
    X_test, y_test,
    model_factory=model_factory,
    metric_func=accuracy_score,
    n_permutations=100,  # Keep low (expensive!)
    n_jobs=-1,           # Parallel highly recommended
    backend='processes'  # Better for model training
)

print(f"Observed: {results['observed']:.4f}")
print(f"p-value: {results['p_value']:.4f}")

if results['p_value'] < 0.05:
    print("✅ Model significantly better than random!")
else:
    print("⚠️  Model not significantly different from random")
```

**⏱️ Timing:** ~15-20 seconds for 100 permutations (8 cores)

---

## 📊 Feature 3: Probability-Based Metrics

**Automatic handling of AUC, log loss, and other probability metrics.**

### Problem (Before)

```python
# This would fail if model doesn't have predict_proba
from sklearn.metrics import roc_auc_score
score = roc_auc_score(y_true, model.predict(X))  # ❌ Wrong!
```

### Solution (v1.5.0)

```python
from circular_bias_detector import create_metric_wrapper

# Automatic detection
wrapper = create_metric_wrapper('auc')
print(wrapper.requires_proba)  # True

# Handles predict_proba automatically
score = wrapper(y_true, model, X_test)  # ✅ Works!
```

### Check Compatibility

```python
from circular_bias_detector import validate_metric_compatibility

compatible, msg = validate_metric_compatibility(model, 'auc')
if not compatible:
    print(f"⚠️  {msg}")
    # Fix: Use model with probability=True
```

### Supported Metrics

**Probability-based** (auto-detected):
- `'auc'` / `roc_auc_score`
- `'logloss'` / `log_loss`
- `'brier'` / `brier_score_loss`

**Prediction-based**:
- `'accuracy'` / `accuracy_score`
- `'f1'` / `f1_score`
- `'precision'` / `precision_score`
- `'mse'` / `mean_squared_error`

---

## ⚡ Feature 4: Adaptive Permutation Testing

**Automatically stops when p-value is stable. Up to 20x faster!**

### Example

```python
from circular_bias_detector import adaptive_permutation_test

results = adaptive_permutation_test(
    perf_matrix, const_matrix, compute_psi,
    max_permutations=10000,  # Maximum
    min_permutations=100,    # Minimum before checking
    precision=0.01,          # Stop when SE < 0.01
    random_seed=42,
    n_jobs=-1
)

print(f"Converged: {results['converged']}")
print(f"Used: {results['n_permutations']} / {results['max_permutations']}")
print(f"p-value: {results['p_value']:.4f}")
```

**Example Output:**
```
Converged: True
Used: 523 / 10000
p-value: 0.0234
```

**Savings:** 19x fewer permutations needed! ⚡

---

## 📈 Feature 5: Visualization

**Beautiful plots and model cards for your reports.**

### Permutation Distribution Plot

```python
import matplotlib.pyplot as plt

results = permutation_test(perf_matrix, const_matrix, compute_psi, n_permutations=1000)

# Plot
plt.hist(results['permuted_values'], bins=50, alpha=0.7, density=True)
plt.axvline(results['observed'], color='red', linestyle='--', label='Observed')
plt.axvline(results['ci_lower'], color='orange', linestyle=':')
plt.axvline(results['ci_upper'], color='orange', linestyle=':')
plt.xlabel('PSI Score')
plt.ylabel('Density')
plt.title(f"Permutation Test (p={results['p_value']:.4f})")
plt.legend()
plt.show()
```

### Model Card Generation

```python
card = f"""
# Bias Detection Report

## Results
- **Observed PSI:** {results['observed']:.4f}
- **95% CI:** [{results['ci_lower']:.4f}, {results['ci_upper']:.4f}]
- **p-value:** {results['p_value']:.4f}
- **Permutations:** {results['n_permutations']}

## Interpretation
{'⚠️ Bias detected' if results['p_value'] < 0.05 else '✅ No bias detected'}

## Recommendation
{'Review evaluation methodology' if results['p_value'] < 0.05 else 'Continue current practices'}
"""

print(card)
# Save to file
with open('bias_report.md', 'w') as f:
    f.write(card)
```

**See full notebook:** `examples/permutation_visualization.ipynb`

---

## 🎯 Common Use Cases

### Use Case 1: Fast Bias Detection

```python
from circular_bias_detector import permutation_test, compute_psi

# Quick test with parallelism
results = permutation_test(
    perf_matrix, const_matrix, compute_psi,
    n_permutations=500,
    n_jobs=-1
)
```

### Use Case 2: Conservative Model Evaluation

```python
from circular_bias_detector import retrain_null_test

# Conservative test for high-stakes decision
results = retrain_null_test(
    X_train, y_train, X_test, y_test,
    model_factory, metric_func,
    n_permutations=100,
    n_jobs=-1
)
```

### Use Case 3: Metric Compatibility Check

```python
from circular_bias_detector import validate_metric_compatibility

# Before running expensive tests
compatible, msg = validate_metric_compatibility(model, 'auc')
if not compatible:
    raise ValueError(msg)
```

### Use Case 4: Adaptive Testing for Unknown Complexity

```python
from circular_bias_detector import adaptive_permutation_test

# Let it figure out how many permutations needed
results = adaptive_permutation_test(
    perf_matrix, const_matrix, metric_func,
    max_permutations=10000,
    precision=0.01,
    n_jobs=-1
)
```

---

## 🔧 Configuration Tips

### Choosing Backend

```python
# Threads (default, recommended)
results = permutation_test(..., backend='threads')
# ✅ Lower overhead
# ✅ Works with most functions
# ⚠️  Subject to GIL for pure Python

# Processes
results = permutation_test(..., backend='processes')
# ✅ True parallelism (bypasses GIL)
# ✅ Better for CPU-intensive metrics
# ⚠️  Higher overhead
# ⚠️  Requires picklable objects
```

### Choosing n_permutations

| Dataset Size | Recommended | Time (8 cores) |
|--------------|-------------|----------------|
| Small (<100) | 1000-5000   | <1 min         |
| Medium (100-1000) | 500-1000 | 1-5 min       |
| Large (>1000) | 500 or adaptive | 5-15 min  |

### Choosing n_jobs

```python
n_jobs=1     # Sequential (no parallelism)
n_jobs=2     # Use 2 cores
n_jobs=4     # Use 4 cores
n_jobs=-1    # Use all available cores (recommended)
```

---

## 🐛 Troubleshooting

### Issue: Slow Performance

**Solution:**
```python
# Option 1: Use adaptive testing
results = adaptive_permutation_test(..., max_permutations=10000)

# Option 2: Reduce permutations
results = permutation_test(..., n_permutations=500)

# Option 3: Increase parallelism
results = permutation_test(..., n_jobs=-1)
```

### Issue: Pickle Errors with Processes

**Solution:**
```python
# Use threads instead
results = permutation_test(..., backend='threads')
```

### Issue: Model Doesn't Support predict_proba

**Solution:**
```python
# Option 1: Enable probabilities
from sklearn.svm import SVC
model = SVC(probability=True)  # Add probability=True

# Option 2: Use prediction-based metric
wrapper = create_metric_wrapper('accuracy')  # Doesn't need proba

# Option 3: Accept decision_function fallback
# (will work but with warning)
```

### Issue: Inconsistent Results

**Solution:**
```python
# Always set random_seed
results = permutation_test(..., random_seed=42)
```

---

## 📚 Learn More

- **Full Documentation:** `docs/ADVANCED_FEATURES.md`
- **Examples:** `examples/` directory
- **Changelog:** `CHANGELOG_V1.5.0.md`
- **GitHub:** https://github.com/hongping-zh/circular-bias-detection

---

## 🎓 Next Steps

1. **Try the examples:**
   ```bash
   python examples/retrain_null_example.py
   jupyter notebook examples/permutation_visualization.ipynb
   ```

2. **Read the advanced guide:**
   ```bash
   cat docs/ADVANCED_FEATURES.md
   ```

3. **Run the tests:**
   ```bash
   pytest tests/test_permutation.py -v
   pytest tests/test_metrics_utils.py -v
   ```

4. **Integrate into your project:**
   - Replace sequential tests with parallel
   - Add retrain-null for critical evaluations
   - Use metric wrappers for compatibility

---

**Questions?** Open an issue on GitHub!

**Happy bias detecting! 🔍**
