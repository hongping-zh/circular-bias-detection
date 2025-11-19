# 🎉 New Features in CBD v1.3

## Quick Summary

CBD v1.3 brings major performance and usability improvements:

- ⚡ **3-4x faster** with parallel execution
- 🔒 **100% reproducible** results with improved RNG
- 📊 **AUC/Log Loss support** for probability-based metrics
- 🔬 **Conservative testing** with retrain null method
- 📈 **Large dataset support** with intelligent subsampling
- 📋 **Model cards** for audit documentation
- 🎨 **Rich visualizations** in Jupyter notebooks

---

## 🚀 Quick Examples

### 1. Parallel Execution (3-4x Faster)

```python
from cbd.api import detect_bias
from sklearn.metrics import accuracy_score

# Before: Sequential (slow)
result = detect_bias(model, X, y, metric=accuracy_score)

# After: Parallel (fast)
result = detect_bias(
    model, X, y, 
    metric=accuracy_score,
    n_jobs=-1  # Use all CPUs
)
```

### 2. AUC and Probability Metrics

```python
from sklearn.metrics import roc_auc_score

def auc_metric(y_true, y_proba):
    return roc_auc_score(y_true, y_proba[:, 1])

result = detect_bias(
    model, X, y,
    metric=auc_metric,
    allow_proba=True  # Use predict_proba
)
```

### 3. Large Dataset Optimization

```python
# Fast approximate test on 100K samples
result = detect_bias(
    model, X_large, y_large,
    metric=accuracy_score,
    subsample_size=5000,  # Sample 5K points
    n_jobs=-1
)
```

### 4. Conservative Testing

```python
# Rigorous test: retrain on each permutation
result = detect_bias(
    model, X, y,
    metric=accuracy_score,
    null_method='retrain',  # More conservative
    n_permutations=100,
    n_jobs=-1
)
```

---

## 📊 Performance Comparison

| Dataset Size | v1.2 (Sequential) | v1.3 (Parallel) | Speedup |
|--------------|-------------------|-----------------|---------|
| 1K samples   | 2.3s              | 0.8s            | 2.9x    |
| 5K samples   | 11.2s             | 3.4s            | 3.3x    |
| 10K samples  | 23.5s             | 6.8s            | 3.5x    |

---

## 🎯 Key Improvements

### 1. Parallelization & Reproducibility
- Thread and process backends
- Pre-generated permutation indices
- Guaranteed reproducibility with same seed

### 2. Metric Type Support
- Probability-based metrics (AUC, log loss)
- Automatic fallback to decision_function
- Comprehensive error handling

### 3. Null Method Options
- `permute`: Fast label shuffling (default)
- `retrain`: Conservative model retraining

### 4. Performance Optimization
- Intelligent subsampling for large datasets
- P-value confidence intervals
- Parallel execution with joblib

### 5. Visualization & Documentation
- Interactive Jupyter notebook
- Automated model card generation
- Distribution plots and statistics

### 6. CI/CD Integration
- Codecov integration
- 85%+ test coverage
- Multi-version Python testing

---

## 📦 Installation

```bash
# Upgrade to v1.3
pip install --upgrade circular-bias-detector

# Or install from source
git clone https://github.com/hongping-zh/circular-bias-detection.git
cd circular-bias-detection
pip install -e .
```

---

## 📚 Documentation

- **Full Guide**: [docs/ENHANCEMENTS_V1.3.md](ENHANCEMENTS_V1.3.md)
- **Jupyter Notebook**: [examples/visualization_and_model_card.ipynb](../examples/visualization_and_model_card.ipynb)
- **API Reference**: [docs/API.md](API.md)
- **Migration Guide**: See ENHANCEMENTS_V1.3.md

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run new enhancement tests
pytest tests/test_enhanced_detect_bias.py -v

# Generate coverage report
pytest --cov=circular_bias_detector --cov=cbd --cov-report=html
```

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

---

## 📄 License

MIT License - see [LICENSE](../LICENSE) for details.

---

## 🙏 Acknowledgments

Thanks to all contributors and users who provided feedback for v1.3!

---

**Questions?** Open an issue on [GitHub](https://github.com/hongping-zh/circular-bias-detection/issues)
