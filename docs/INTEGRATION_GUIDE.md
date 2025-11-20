## Integration Guide - Popular Evaluation Frameworks

This guide shows how to integrate CBD into your existing evaluation workflow.

## 🎯 Supported Frameworks

1. **OpenCompass** - LLM evaluation
2. **lm-evaluation-harness** (EleutherAI) - LLM benchmarking
3. **RecBole** - Recommender systems

## 📦 Installation

```bash
pip install circular-bias-detector
```

---

## 1. OpenCompass Integration

### Quick Start

```python
from cbd.integrations import OpenCompassHook

# Create hook
hook = OpenCompassHook(
    output_dir='./bias_detection',
    auto_detect=True,
    n_permutations=1000
)

# In your OpenCompass config
config = {
    'model': {'name': 'gpt-3.5-turbo'},
    'datasets': [
        {'name': 'mmlu'},
        {'name': 'hellaswag'}
    ]
}

# Before evaluation
hook.before_evaluation(config)

# ... run OpenCompass evaluation ...

# After evaluation
results = {...}  # OpenCompass results
hook.after_evaluation(results)

# Export report
hook.export_for_paper('bias_report.md')
```

### Automatic Detection

The hook automatically:
- ✅ Records evaluation constraints
- ✅ Detects suspicious patterns
- ✅ Generates risk summaries
- ✅ Creates paper-ready reports

### Output Files

```
./bias_detection/
├── constraints.json          # Recorded constraints
├── metrics.json              # Evaluation metrics
├── bias_analysis.json        # Detection results
└── bias_report.md           # Paper-ready report
```

---

## 2. LM Evaluation Harness Integration

### Quick Start

```python
from cbd.integrations import LMEvaluationHarnessHook, quick_check

# Method 1: Quick check after evaluation
analysis = quick_check('results.json', output_dir='./cbd_lm_eval')
print(analysis['summary'])

# Method 2: Full integration
hook = LMEvaluationHarnessHook(
    output_dir='./cbd_lm_eval',
    fast_mode=True  # Use pre-computed thresholds
)

# Load results
results = hook.load_results('results.json')

# Detect bias
analysis = hook.detect_bias(results)

# Create report
hook.create_report(analysis)
```

### Command Line Usage

```bash
# 1. Run lm_eval
lm_eval --model hf \
    --model_args pretrained=gpt2 \
    --tasks hellaswag,arc_easy,winogrande \
    --output_path results.json

# 2. Check for bias
python -c "
from cbd.integrations import quick_check
analysis = quick_check('results.json')
print(analysis['summary'])
"
```

### Example Output

```
🔍 Circular Bias Detection Results
====================================
⚠️ 中等风险：3个测试中1个显示异常（33%），
其中1个高风险，⚡ 部分测试异常，建议重点审查
====================================
```

---

## 3. RecBole Integration

### Quick Start

```python
from cbd.integrations import RecBoleHook

# Create hook
hook = RecBoleHook(
    output_dir='./cbd_recbole',
    metrics_to_check=['Recall', 'NDCG', 'Hit']
)

# In RecBole training loop
hook.before_training(config)

for epoch in range(num_epochs):
    train_metrics = train_epoch(model, train_data)
    valid_metrics = evaluate(model, valid_data)
    
    # Record metrics
    hook.on_epoch_end(epoch, train_metrics, valid_metrics)

# After training
hook.after_training(model, valid_data, test_data)

# Get analysis
analysis = hook.get_analysis()
print(analysis['summary'])

# Create report
hook.create_report()
```

### Overfitting Detection

The hook automatically detects:
- ✅ Validation performance degradation
- ✅ Train-test performance gap
- ✅ Data leakage patterns

### Example Output

```
⚡ 中等风险：检测到过拟合模式，验证集性能在训练后期下降。
建议：使用early stopping或增加正则化。
```

---

## 🚀 Advanced Usage

### 1. Batch Analysis Across Multiple Models

```python
from cbd.integrations import OpenCompassHook

models = ['gpt-3.5', 'gpt-4', 'claude-2']
results_all = {}

for model_name in models:
    hook = OpenCompassHook(output_dir=f'./bias_{model_name}')
    
    # Run evaluation
    results = evaluate_model(model_name)
    hook.after_evaluation(results)
    
    results_all[model_name] = hook.analyze_results(results)

# Compare models
for model, analysis in results_all.items():
    print(f"{model}: {analysis['summary']}")
```

### 2. Custom Metrics

```python
from cbd.integrations import LMEvaluationHarnessHook

hook = LMEvaluationHarnessHook()

# Define custom metric extractor
def extract_custom_metrics(results):
    return {
        'task': results['task_name'],
        'custom_score': results['my_metric']
    }

# Use in analysis
results = hook.load_results('results.json')
custom_analysis = extract_custom_metrics(results)
```

### 3. CI/CD Integration

```yaml
# .github/workflows/eval.yml
name: LLM Evaluation with Bias Detection

on: [push, pull_request]

jobs:
  evaluate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Install dependencies
        run: |
          pip install circular-bias-detector
          pip install lm-evaluation-harness
      
      - name: Run evaluation
        run: |
          lm_eval --model hf \
            --model_args pretrained=gpt2 \
            --tasks hellaswag \
            --output_path results.json
      
      - name: Detect bias
        run: |
          python -c "
          from cbd.integrations import quick_check
          analysis = quick_check('results.json')
          print(analysis['summary'])
          
          # Fail if high risk
          if analysis['overall_risk'] == 'High':
              exit(1)
          "
      
      - name: Upload reports
        uses: actions/upload-artifact@v4
        with:
          name: bias-reports
          path: ./cbd_lm_eval/
```

---

## 📊 Output Formats

### JSON Format

```json
{
  "n_tasks": 3,
  "overall_risk": "Medium",
  "summary": "⚡ 中等风险：3个测试中1个显示异常...",
  "per_task_analysis": {
    "hellaswag": {
      "accuracy": 0.456,
      "suspicious": false
    },
    "arc_easy": {
      "accuracy": 0.923,
      "suspicious": true,
      "reason": "Unusually high accuracy"
    }
  }
}
```

### Markdown Report

```markdown
# Bias Detection Report

## Overall Assessment
- **Risk Level:** Medium
- **Tasks Analyzed:** 3
- **Summary:** ⚡ 中等风险：3个测试中1个显示异常...

## Per-Task Results
| Task | Accuracy | Suspicious | Status |
|------|----------|------------|--------|
| hellaswag | 0.4560 | false | ✅ OK |
| arc_easy | 0.9230 | true | ⚠️ Review |

## Recommendations
- ⚡ Medium risk - Further validation recommended
- Re-run evaluation on independent test set
```

---

## 🎓 Best Practices

### 1. When to Run Detection

**Always run detection when:**
- Publishing benchmark results
- Comparing multiple models
- Submitting to leaderboards
- Before production deployment

### 2. Interpreting Results

**Risk Levels:**
- 🚨 **High**: Immediate investigation required
- ⚡ **Medium**: Revalidation recommended
- ✅ **Low**: Results appear normal

### 3. Common Issues

**Issue: High risk detected**
- ✅ Check for data leakage
- ✅ Verify train/test split
- ✅ Review evaluation setup

**Issue: Inconsistent results**
- ✅ Use fixed random seeds
- ✅ Run multiple trials
- ✅ Check for non-determinism

---

## 🔧 Troubleshooting

### Import Errors

```python
# If integration module not found
pip install --upgrade circular-bias-detector

# Verify installation
python -c "from cbd.integrations import OpenCompassHook; print('OK')"
```

### Performance Issues

```python
# Use fast mode for large evaluations
hook = LMEvaluationHarnessHook(fast_mode=True)

# Or reduce permutations
hook = OpenCompassHook(n_permutations=100)  # Default: 1000
```

### Custom Frameworks

```python
# For unsupported frameworks, use core API
from cbd.api import detect_bias
from cbd.risk_summary import generate_risk_summary

# Your evaluation code
results = your_evaluation_framework.evaluate(model)

# Extract data
X, y, y_pred = extract_from_results(results)

# Detect bias
from sklearn.metrics import accuracy_score
result = detect_bias(model, X, y, accuracy_score)
summary = generate_risk_summary(result, "accuracy")
print(summary)
```

---

## 📚 Examples Repository

Complete examples available at:
```
examples/integrations/
├── opencompass_example.py
├── lm_eval_example.py
├── recbole_example.py
└── custom_framework_example.py
```

---

## 🤝 Contributing

To add support for a new framework:

1. Create `cbd/integrations/your_framework_hook.py`
2. Implement hook methods
3. Add tests in `tests/test_integrations.py`
4. Update this guide

See `CONTRIBUTING.md` for details.

---

## 📞 Support

- **Issues**: https://github.com/hongping-zh/circular-bias-detection/issues
- **Discussions**: https://github.com/hongping-zh/circular-bias-detection/discussions
- **Email**: yujjam@uest.edu.gr
