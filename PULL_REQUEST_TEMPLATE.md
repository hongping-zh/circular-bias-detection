# Pull Request: CBD Project v1.2.0 - Complete Feature Set

## 📋 Summary

This PR introduces three major features to the Circular Bias Detection project:

1. **CLI One-Line Command Support** for CBD Dataset v3/v3.1
2. **Web App "Try with Latest Dataset" Banner**
3. **Lightweight CBD Python Package** with sklearn adapter

## 🎯 Changes Overview

### 1. CLI Enhancement (Commit: f0ea19d)
- **Smart CSV Selection**: Automatically selects the largest CSV file from Zenodo records
- **Enhanced Caching**: Verified cache mechanism works correctly
- **CLI Integration**: Added `zenodo://17637303` example to help text
- **Comprehensive Tests**: 3 new unit tests + standalone test script
- **Complete Documentation**: Usage guide, quick reference, and changelog

**Key Command**:
```bash
circular-bias detect zenodo://17637303
```

### 2. Web App Feature (Commit: 3a692af)
- **Prominent Banner**: Eye-catching gradient purple banner on homepage
- **One-Click Loading**: Instant dataset loading with button click
- **URL Parameter Support**: Auto-load via `?dataset=latest` or `?dataset=17637303`
- **Marketing Materials**: Complete social media copy and documentation

**Live Demo**:
- Manual: https://is.gd/check_sleuth
- Auto-load: https://is.gd/check_sleuth?dataset=latest

### 3. CBD Package (Commit: a9c3c32)
- **CBDModel Protocol**: Minimal interface for bias detection
- **detect_bias Function**: Permutation-based statistical test
- **SklearnCBDModel Adapter**: Wrap scikit-learn estimators
- **Type-Safe API**: Full type hints and documentation
- **CI/CD**: GitHub Actions workflow for automated testing

**Quick Example**:
```python
from cbd import detect_bias, SklearnCBDModel
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

clf = LogisticRegression().fit(X_train, y_train)
model = SklearnCBDModel(clf)
result = detect_bias(model, X_test, y_test, metric=accuracy_score)
```

## 📊 Statistics

| Metric | Count |
|--------|-------|
| Files Changed | 26 |
| Lines Added | 2,669+ |
| Lines Deleted | 9 |
| New Documentation Files | 14 |
| Git Commits | 3 |
| Tests Added | 4 |

## ✅ Testing

### CLI Tests
```bash
$ python test_zenodo_17637303.py
✓ Test 1: Largest CSV Selection
✓ Test 2: Cache Mechanism
✓ Test 3: CLI Integration
```

### CBD Package Tests
```bash
$ python run_cbd_test.py
✓ test_detect_bias_sanity
```

### Example Execution
```bash
$ python examples/quickstart.py
Observed metric: 0.826
p-value: 0.002
Conclusion: Suspicious: p <= 0.05 — potential circular bias detected
```

## 📝 Documentation

### New Files
- `ZENODO_17637303_USAGE.md` - CLI detailed usage guide
- `QUICK_REFERENCE.md` - CLI quick reference card
- `cbd/README.md` - CBD package documentation
- `docs/CBDModel.md` - Protocol documentation
- `CONTRIBUTING.md` - Contribution guidelines
- `web-app/MARKETING_COPY.md` - Marketing materials
- `CBD_PACKAGE_SUMMARY.md` - Implementation summary
- `FINAL_SESSION_REPORT.md` - Complete session report

### Updated Files
- `README.md` - Added usage examples
- `circular_bias_cli/main.py` - Updated CLI help
- `web-app/src/App.jsx` - Added banner and URL support
- `pyproject.toml` - Added cbd package

## 🔄 Backward Compatibility

✅ All changes are backward compatible:
- Existing `zenodo://17201032` continues to work
- All current CLI commands unchanged
- Web App existing functionality preserved
- No breaking API changes

## 🚀 Impact

### For Researchers
- Zero-configuration CLI usage
- Shareable demo links
- Real-world dataset testing

### For Developers
- Easy MLOps integration
- Type-safe Python API
- Automated testing

### For Educators
- Pre-loaded tutorial links
- Instant demonstrations
- Copy-paste examples

## 🔗 Related Links

- **Dataset v3/v3.1**: https://doi.org/10.5281/zenodo.17637303
- **Concept DOI**: https://doi.org/10.5281/zenodo.17637302
- **Web App**: https://is.gd/check_sleuth
- **GitHub**: https://github.com/hongping-zh/circular-bias-detection

## 📋 Checklist

- [x] Code follows project style guidelines
- [x] All tests passing
- [x] Documentation updated
- [x] No breaking changes
- [x] CI/CD configured
- [x] Examples working
- [x] Backward compatible

## 🎯 Next Steps After Merge

1. Tag release v1.2.0
2. Update PyPI package (if applicable)
3. Announce on social media
4. Update main README badges
5. Deploy web app updates

## 💬 Additional Notes

This PR represents a significant enhancement to the CBD project, making it more accessible and easier to integrate into existing workflows. The three features complement each other:

- **CLI**: For automation and quick validation
- **Web App**: For demonstrations and teaching
- **CBD Package**: For production integration

All features have been tested and documented thoroughly.

---

**Branch**: `feat/zenodo-badges-citation`  
**Target**: `main`  
**Commits**: 3 (f0ea19d, 3a692af, a9c3c32)  
**Reviewers**: @hongping-zh
