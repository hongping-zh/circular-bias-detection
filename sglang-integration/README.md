# SGLang Integration - Circular Bias Detection

This directory contains the implementation for integrating circular-bias-detection into SGLang.

## 📁 Structure

```
sglang-integration/
├── README.md                      # This file
├── python/
│   └── sglang/
│       └── lang/
│           └── bias_audit.py      # Core BiasAuditor implementation
├── tests/
│   └── test_bias_audit.py         # Unit tests
├── examples/
│   └── bias_detection_demo.py     # Usage example
├── docs/
│   └── bias_detection.md          # Documentation
└── PR_TEMPLATE.md                 # Pull request template
```

## 🎯 Implementation Plan

### Phase 1: Core Implementation ✅
- [x] BiasAuditor class
- [x] Integration with circular_bias_detector
- [x] Performance scoring utilities

### Phase 2: SGLang Integration (Next)
- [ ] Runtime integration
- [ ] Optional enable/disable flag
- [ ] Minimal API changes

### Phase 3: Testing & Documentation
- [ ] Unit tests
- [ ] Integration tests
- [ ] Usage examples
- [ ] API documentation

### Phase 4: PR Submission
- [ ] Create fork of SGLang
- [ ] Apply changes
- [ ] Submit PR
- [ ] Address review feedback

## 🚀 Quick Start (Testing Locally)

```bash
# 1. Install circular-bias-detection
cd C:\Users\14593\CascadeProjects\circular-bias-detection
pip install -e .

# 2. Test the BiasAuditor independently
python sglang-integration/tests/test_bias_audit.py

# 3. Run example (requires SGLang)
python sglang-integration/examples/bias_detection_demo.py
```

## 📚 Academic Reference

This implementation is based on:

**Paper**: "Circular Reasoning Bias Detection in AI Algorithm Evaluation"  
**Authors**: Hongping Zhang et al.  
**Status**: Under review at Journal of Open Source Software (JOSS)  
**Repository**: https://github.com/[username]/circular-bias-detection  
**License**: MIT

## 🔗 Links

- SGLang Repository: https://github.com/sgl-project/sglang
- Circular Bias Detection: https://github.com/[username]/circular-bias-detection
- JOSS Submission: [link when available]
