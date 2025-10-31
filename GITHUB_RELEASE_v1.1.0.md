# v1.1.0 - Modular Architecture and LLM Integration

**Release Date**: 2024-10-24  
**Tag**: v1.1.0  
**Type**: Major Release

---

## 🎯 Overview

This major release completes **Phase 1** of the circular-bias-detection project, introducing a modular architecture and production-ready LLM inference integration. The framework is now optimized for integration into LLM serving systems like SGLang and vLLM.

---

## ✨ Major Features

### 🏗️ Modular Architecture

The monolithic `core.py` has been refactored into specialized submodules:

- **`circular_bias_detector.core.metrics`** (280 lines)
  - `compute_psi()` - Parameter Stability Index
  - `compute_ccs()` - Constraint Consistency Score  
  - `compute_rho_pc()` - Performance-Constraint Correlation
  - `detect_bias_threshold()` - Threshold-based detection

- **`circular_bias_detector.core.bootstrap`** (240 lines)
  - `bootstrap_resample()` - Statistical resampling
  - `compute_confidence_intervals()` - CI computation
  - `compute_p_value()` - Significance testing
  - `detect_bias_bootstrap()` - Bootstrap-based detection

- **`circular_bias_detector.core.matrix`** (260 lines)
  - `validate_matrices()` - Input validation
  - `build_performance_matrix()` - Performance matrix construction
  - `build_constraint_matrix()` - Constraint matrix construction
  - `aggregate_time_periods()` - Temporal aggregation

**Backward Compatibility**: ✅ All existing code continues to work without changes.

### 🚀 LLM Inference Integration

New `inference` submodule for end-to-end bias detection:

- **`circular_bias_detector.inference.base`** (190 lines)
  - `InferenceBackend` - Abstract base class
  - `LLMOutput` - Structured output dataclass
  - `MockBackend` - Testing support

- **`circular_bias_detector.inference.backends.vllm_backend`** (250 lines)
  - `VLLMBackend` - Production vLLM integration
  - Batch processing support
  - Constraint tracking
  - Performance monitoring

- **`circular_bias_detector.inference.detector`** (270 lines)
  - `BiasDetectorWithInference` - End-to-end workflow
  - Automatic matrix construction
  - Generation history tracking
  - Real-time bias detection

**Usage**:
```python
from circular_bias_detector.inference import VLLMBackend
from circular_bias_detector.inference.detector import BiasDetectorWithInference

backend = VLLMBackend(model="meta-llama/Llama-2-7b-hf")
detector = BiasDetectorWithInference(backend=backend)

results = detector.detect_from_prompts(
    prompts=["Analyze sentiment..."] * 10,
    constraints={'temperature': 0.7},
    time_periods=4
)
```

### 🧪 Enhanced Testing Framework

Comprehensive test suite with 1100+ lines:

- **`tests/test_core_metrics.py`** (250+ lines)
  - All metric calculations
  - Edge cases and boundary conditions
  - Performance validation

- **`tests/test_core_bootstrap.py`** (230+ lines)
  - Statistical resampling
  - Confidence intervals
  - P-value computation

- **`tests/test_core_matrix.py`** (230+ lines)
  - Matrix construction
  - Validation logic
  - Temporal aggregation

- **`tests/test_inference.py`** (320+ lines)
  - Backend integration
  - MockBackend functionality
  - VLLMBackend (when available)

- **`tests/test_integration.py`** (300+ lines)
  - End-to-end workflows
  - Historical analysis
  - Cross-module integration

**Coverage**: 95%+ across all modules

---

## 🔧 Improvements

### Bug Fixes

- **Fixed** `ZeroDivisionError` in `compute_rho_pc()` when all constraints are constant
  - Now correctly handles cases where constraint variance is zero
  - Returns ρ_PC = 0.0 (no correlation) as expected
  - Added specific test case `test_rho_pc_constant_constraints`

- **Fixed** edge cases in matrix construction with uneven time periods

- **Improved** error messages for invalid inputs

### Performance Optimizations

- Optimized matrix operations using vectorized NumPy operations
- Reduced memory footprint in bootstrap resampling
- Improved computational efficiency of constraint aggregation

### Documentation

- **Added** `PHASE1_COMPLETION_SUMMARY.md` - Complete Phase 1 overview
- **Added** `QUICK_TEST_GUIDE.md` - Testing guide
- **Added** `INSTALL_GUIDE.md` - Installation instructions
- **Updated** API documentation with new modules
- **Enhanced** docstrings with detailed examples

---

## 📦 Installation

### Stable Release (v1.1.0)

```bash
pip install circular-bias-detection==1.1.0
```

### From GitHub

```bash
pip install git+https://github.com/hongping-zh/circular-bias-detection.git@v1.1.0
```

### Development Installation

```bash
git clone https://github.com/hongping-zh/circular-bias-detection.git
cd circular-bias-detection
pip install -e .
```

---

## 📊 Statistics

| Metric | Value |
|--------|-------|
| **New Code** | 1500+ lines |
| **Test Code** | 1100+ lines |
| **Documentation** | 500+ lines |
| **Test Coverage** | 95%+ |
| **Modules** | 8 new submodules |
| **Breaking Changes** | 0 (100% backward compatible) |

---

## 🎓 Academic Status

- **Paper**: "Circular Reasoning Bias Detection in AI Algorithm Evaluation"
- **Status**: Under review at *Journal of Open Source Software* (JOSS)
- **Authors**: Hongping Zhang et al.

---

## 🚀 Integration Status

### Current

- ✅ Standalone Python package
- ✅ vLLM backend support
- ✅ Comprehensive API for custom backends

### In Progress

- 🔄 **SGLang integration** (PR in preparation)
- 🔄 Additional backend implementations

---

## 🔄 Migration Guide

### For Existing Users

**Good news**: No changes required! All existing code continues to work:

```python
# Your existing code (still works!)
from circular_bias_detector import BiasDetector
detector = BiasDetector()
results = detector.detect_bias(perf_matrix, const_matrix)
```

### For New Features

To use the new modular API:

```python
# Import from specific modules
from circular_bias_detector.core.metrics import compute_psi, compute_ccs
from circular_bias_detector.core.bootstrap import bootstrap_resample

# Or use the new inference integration
from circular_bias_detector.inference import VLLMBackend
```

---

## 🐛 Known Issues

None currently reported. Please report issues at:
https://github.com/hongping-zh/circular-bias-detection/issues

---

## 🙏 Acknowledgments

Thanks to:
- JOSS reviewers for valuable feedback
- Early adopters and testers
- The Python scientific computing community

---

## 📝 Full Changelog

See [PHASE1_COMPLETION_SUMMARY.md](https://github.com/hongping-zh/circular-bias-detection/blob/main/PHASE1_COMPLETION_SUMMARY.md) for complete details.

---

## 🔗 Links

- **Repository**: https://github.com/hongping-zh/circular-bias-detection
- **Documentation**: [README.md](https://github.com/hongping-zh/circular-bias-detection/blob/main/README.md)
- **Issues**: https://github.com/hongping-zh/circular-bias-detection/issues
- **JOSS Paper**: [Under review]

---

## ⬆️ Upgrade

```bash
pip install --upgrade circular-bias-detection
```

---

**What's Next**: Phase 2 will focus on performance optimization, additional backends, and web interface development.

Stay tuned! 🚀
