# Release Notes - v1.2.0

**Release Date**: 2025-11-18  
**Branch**: feat/zenodo-badges-citation → main  
**Commits**: f0ea19d, 3a692af, a9c3c32

---

## 🎉 What's New

### 1. CLI One-Line Command Support for CBD Dataset v3/v3.1

Now you can analyze the latest CBD dataset with a single command:

```bash
circular-bias detect zenodo://17637303
```

**Features**:
- 🎯 **Smart File Selection**: Automatically selects the largest CSV file
- 💾 **Intelligent Caching**: Downloads once, reuses forever
- 📚 **Complete Documentation**: Usage guides and quick reference
- ✅ **Fully Tested**: 3 new unit tests, all passing

**Example**:
```bash
$ circular-bias detect zenodo://17637303
Loading data from: zenodo://17637303
Loaded 4 records
Running DECISION algorithm...
✓ Analysis complete
```

---

### 2. Web App "Try with Latest Dataset" Feature

Visit https://is.gd/check_sleuth to see the new prominent banner!

**Features**:
- 🎨 **Eye-Catching Banner**: Gradient purple design on homepage
- 🔘 **One-Click Loading**: Instant dataset loading
- 🔗 **URL Parameters**: Share pre-loaded demos
- 📱 **Responsive Design**: Works on all devices

**Try It Now**:
- Manual: https://is.gd/check_sleuth
- Auto-load: https://is.gd/check_sleuth?dataset=latest

---

### 3. Lightweight CBD Python Package

A new standalone package for easy integration into your code:

```python
from cbd import detect_bias, SklearnCBDModel
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Train your model
clf = LogisticRegression().fit(X_train, y_train)

# Wrap and test for bias
model = SklearnCBDModel(clf)
result = detect_bias(model, X_test, y_test, metric=accuracy_score)

print(f"p-value: {result['p_value']}")
print(f"Conclusion: {result['conclusion']}")
```

**Features**:
- 🔌 **Protocol-Based**: Works with any model implementing `predict()`
- 🛡️ **Type-Safe**: Full type hints for IDE support
- 📦 **Framework-Agnostic**: Sklearn adapter included, more coming
- 🧪 **Well-Tested**: Unit tests and examples
- 🤖 **CI/CD Ready**: GitHub Actions workflow included

---

## 📊 Statistics

- **26 files changed**
- **2,669+ lines added**
- **9 lines deleted**
- **14 new documentation files**
- **4 new tests** (all passing)

---

## 🔧 Technical Details

### CLI Enhancements
- Modified `circular_bias_cli/utils/zenodo_loader.py` for smart file selection
- Updated `circular_bias_cli/main.py` with new examples
- Added comprehensive caching mechanism
- Created standalone test script

### Web App Updates
- Enhanced `web-app/src/App.jsx` with banner component
- Added URL parameter detection and auto-loading
- Updated footer with latest dataset links
- Included hover effects and animations

### CBD Package Structure
```
cbd/
├── __init__.py              # Package exports
├── api.py                   # Core API (CBDModel, detect_bias)
├── README.md                # Package documentation
└── adapters/
    ├── __init__.py
    └── sklearn_adapter.py   # Scikit-learn integration
```

---

## 📚 New Documentation

### User Guides
- **ZENODO_17637303_USAGE.md**: Detailed CLI usage for latest dataset
- **QUICK_REFERENCE.md**: Quick reference card for common commands
- **cbd/README.md**: Complete CBD package documentation
- **docs/CBDModel.md**: Protocol specification and examples

### Developer Guides
- **CONTRIBUTING.md**: Contribution guidelines and setup
- **CBD_PACKAGE_SUMMARY.md**: Implementation details
- **OPTIMIZATION_SUMMARY.md**: Technical optimization notes

### Marketing Materials
- **web-app/MARKETING_COPY.md**: Social media posts and templates
- **web-app/LATEST_DATASET_FEATURE.md**: Feature documentation

---

## 🧪 Testing

All tests passing:

### CLI Tests
```bash
✓ test_zenodo_loader_selects_largest_csv
✓ test_zenodo_cache_mechanism
✓ test_cli_detect_zenodo_17637303
```

### CBD Package Tests
```bash
✓ test_detect_bias_sanity
```

### Manual Verification
```bash
✓ python examples/quickstart.py
✓ circular-bias detect zenodo://17637303
✓ Web app banner displays correctly
✓ URL parameter ?dataset=latest works
```

---

## 🔄 Backward Compatibility

✅ **100% Backward Compatible**

- All existing CLI commands work unchanged
- Previous Zenodo records (`zenodo://17201032`) still supported
- Web app existing features preserved
- No breaking API changes

---

## 🚀 Migration Guide

### For CLI Users
No migration needed! Just update and use the new command:

```bash
git pull
pip install -e .
circular-bias detect zenodo://17637303
```

### For Web App Users
No action required. Visit the site to see the new banner.

### For Python Package Users
Install the package and start using:

```bash
pip install -e .
```

Then in your code:
```python
from cbd import detect_bias, SklearnCBDModel
```

---

## 🔗 Links

### Product
- **GitHub**: https://github.com/hongping-zh/circular-bias-detection
- **Web App**: https://is.gd/check_sleuth
- **Web App (Latest Dataset)**: https://is.gd/check_sleuth?dataset=latest

### Datasets
- **CBD v3/v3.1 (Latest)**: https://doi.org/10.5281/zenodo.17637303
- **Concept DOI**: https://doi.org/10.5281/zenodo.17637302
- **CBD v2.0**: https://doi.org/10.5281/zenodo.17201032

### Documentation
- **Main README**: [README.md](README.md)
- **CLI Guide**: [ZENODO_17637303_USAGE.md](ZENODO_17637303_USAGE.md)
- **Quick Reference**: [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
- **CBD Package**: [cbd/README.md](cbd/README.md)
- **Contributing**: [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 🎯 Use Cases

### Research
```bash
# Quick validation before publication
circular-bias detect zenodo://17637303 --format json --output results.json
```

### Teaching
```
# Share pre-loaded demo with students
https://is.gd/check_sleuth?dataset=latest
```

### Production
```python
# Integrate into ML pipeline
from cbd import detect_bias, SklearnCBDModel

result = detect_bias(model, X_val, y_val, metric=accuracy_score)
if result["p_value"] < 0.05:
    logger.warning("Potential circular bias detected!")
```

---

## 🐛 Bug Fixes

- Fixed file selection logic in Zenodo loader
- Improved error handling in CLI
- Enhanced cache key generation

---

## ⚡ Performance Improvements

- Optimized cache lookup (O(1) hash-based)
- Reduced redundant network requests
- Faster dataset loading with smart file selection

---

## 🙏 Acknowledgments

Thanks to:
- The open science community for feedback
- Zenodo for hosting our datasets
- All contributors and users

---

## 📝 Citation

If you use this release in your research, please cite:

```bibtex
@software{zhang2024cbd_v1_2_0,
  author    = {Zhang, Hongping},
  title     = {Circular Bias Detection v1.2.0},
  year      = {2024},
  publisher = {GitHub},
  version   = {v1.2.0},
  doi       = {10.5281/zenodo.17201032},
  url       = {https://github.com/hongping-zh/circular-bias-detection}
}
```

---

## 🔮 What's Next (v1.3.0)

Planned features:
- PyTorch and TensorFlow adapters
- Parallel permutation testing
- Advanced statistical tests
- More dataset integrations
- Enhanced visualization

---

## 💬 Feedback

We'd love to hear from you!

- **Issues**: https://github.com/hongping-zh/circular-bias-detection/issues
- **Discussions**: https://github.com/hongping-zh/circular-bias-detection/discussions
- **Email**: yujjam@uest.edu.gr

---

**Full Changelog**: https://github.com/hongping-zh/circular-bias-detection/compare/v1.1.0...v1.2.0

**Download**: https://github.com/hongping-zh/circular-bias-detection/releases/tag/v1.2.0
