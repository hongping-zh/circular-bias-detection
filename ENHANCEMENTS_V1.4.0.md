# Enhancements v1.4.0 - Advanced Detection & User Experience

## Overview
This release adds three critical features to address the most common cheating patterns in LLM evaluation and improve accessibility for non-expert users.

## 🎯 New Features

### 1. Prompt Variation Quantification (constraint_text) ✅

**Module:** `cbd.prompt_analysis`

**Problem Solved:**
The most common cheating method in LLM evaluation is prompt engineering - making tiny changes to prompts to boost scores. Traditional methods can't detect this because they don't analyze the prompts themselves.

**Solution:**
Uses Sentence-BERT to compute semantic similarity between prompts, detecting when:
- Prompts are nearly identical (high constraint)
- But performance varies significantly (suspicious)

**Key Functions:**

```python
from cbd.prompt_analysis import (
    compute_prompt_similarity,
    detect_prompt_constraint_cheating,
    analyze_prompt_diversity,
    compute_prompt_constraint_score
)

# Example 1: Detect cheating through prompt manipulation
prompts = [
    "Translate to French: Hello world",
    "Translate into French: Hello world",  # Nearly identical
    "French translation: Hello world"      # Nearly identical
]
scores = [0.95, 0.72, 0.88]  # But performance varies!

result = detect_prompt_constraint_cheating(prompts, scores)
print(result['conclusion'])
# "High risk: Found 3 prompt pairs with high similarity but varying performance"

# Example 2: Compute constraint score for PSI analysis
constraint_score = compute_prompt_constraint_score(prompts)
# Use as "constraint_text" dimension: higher = more constrained prompts
```

**Features:**
- **Semantic similarity**: Uses state-of-the-art Sentence-BERT embeddings
- **Multiple models**: Supports multilingual and domain-specific models
- **Batch analysis**: Analyze multiple prompt groups simultaneously
- **Diversity metrics**: Assess prompt coverage and variety

**Models Supported:**
- `all-MiniLM-L6-v2` (fast, 384 dim, recommended)
- `all-mpnet-base-v2` (best quality, 768 dim)
- `paraphrase-multilingual-MiniLM-L12-v2` (multilingual)

**Installation:**
```bash
pip install sentence-transformers
```

### 2. One-Sentence Risk Summary ✅

**Module:** `cbd.risk_summary`

**Problem Solved:**
Statistical results (p-values, correlations) are hard for non-experts to understand. Users need plain language summaries.

**Solution:**
Automatically generates clear, actionable risk summaries in plain language (supports Chinese and English).

**Key Functions:**

```python
from cbd.risk_summary import (
    generate_risk_summary,
    generate_batch_risk_summary,
    generate_prompt_risk_summary,
    generate_multivariate_risk_summary,
    create_risk_report
)

# Example 1: Simple risk summary
result = detect_bias(model, X, y, accuracy_score)
summary = generate_risk_summary(result, "accuracy")
print(summary)
# "🚨 高风险：accuracy异常高 (观测值=0.950, p=0.0010)，
#  性能随计算资源线性增长（ρ_PC=0.78），可能存在调参作弊，
#  建议：立即暂停使用该模型；进行完整的数据审计"

# Example 2: Batch summary
results = [detect_bias(...) for _ in range(5)]
summary = generate_batch_risk_summary(results)
print(summary)
# "🔍 批量检测：5个测试中3个显示异常（60%），其中1个高风险，
#  ⚠️ 多个测试异常，建议全面审查"

# Example 3: Full report
report = create_risk_report(result, "F1 score")
print(report)
# Includes: risk assessment, technical details, recommendations
```

**Risk Levels:**
- 🚨 **极高风险** (p ≤ 0.001): Immediate action required
- ⚠️ **高风险** (p ≤ 0.01): Deep investigation needed
- ⚡ **中等风险** (p ≤ 0.05): Revalidation recommended
- ℹ️ **低风险** (p ≤ 0.10): Monitor
- ✅ **无明显风险** (p > 0.10): Normal

**Automatic Pattern Detection:**
- Linear growth with compute (调参作弊)
- Extremely high performance (数据泄露)
- Subsampling bias (样本选择偏差)

**Actionable Recommendations:**
- Specific steps based on risk level
- Prioritized by urgency
- Clear and actionable

### 3. Multivariate Joint Detection ✅

**Module:** `cbd.multivariate_detection`

**Problem Solved:**
Testing metrics individually misses joint patterns. A model might pass all individual tests but fail when metrics are considered together.

**Solution:**
Multivariate tests (MANOVA, energy distance) that detect joint anomalies across multiple metrics or tasks.

**Key Functions:**

```python
from cbd.multivariate_detection import (
    detect_multivariate_bias,
    detect_multitask_bias,
    compute_multivariate_psi
)

# Example 1: Joint detection across multiple metrics
from sklearn.metrics import accuracy_score, f1_score, precision_score

metrics = [accuracy_score, f1_score, precision_score]
result = detect_multivariate_bias(
    model, X, y, metrics,
    metric_names=['Accuracy', 'F1', 'Precision'],
    method='energy',  # or 'manova', 'hotelling'
    n_permutations=1000
)
print(result['conclusion'])
# "High risk: Multivariate test significant (p=0.0023). 
#  Joint metric distribution is suspicious across 3 metrics."

# Example 2: GLUE benchmark (9 tasks)
models = {
    'cola': model_cola,
    'sst2': model_sst2,
    'mrpc': model_mrpc,
    'qqp': model_qqp,
    'mnli': model_mnli,
    'qnli': model_qnli,
    'rte': model_rte,
    'wnli': model_wnli,
    'stsb': model_stsb
}

result = detect_multitask_bias(
    models, X_dict, y_dict,
    accuracy_score,
    method='energy'
)
print(result['conclusion'])
# "High risk: Multitask performance is jointly suspicious (p=0.0045) 
#  across 9 tasks. Pattern suggests systematic bias or overfitting."

# Example 3: Multivariate PSI
# Test if accuracy, F1, precision jointly correlate with model size
performance_matrix = np.array([
    [0.70, 0.68, 0.72],  # Small model
    [0.85, 0.83, 0.87],  # Medium model
    [0.95, 0.94, 0.96]   # Large model
])
costs = np.array([1e6, 1e8, 1e10])  # Parameters

result = compute_multivariate_psi(performance_matrix, costs)
print(result['conclusion'])
# "High risk: Strong multivariate correlation between performance and cost 
#  (avg |ρ|=0.89, p=0.0001). Suggests systematic overfitting."
```

**Methods:**

1. **Energy Distance** (Recommended)
   - Distribution-free
   - No normality assumption
   - Most robust for real data
   - Good for any number of metrics

2. **MANOVA** (Wilks' Lambda)
   - Classic multivariate test
   - Assumes multivariate normality
   - Good for balanced designs
   - Interpretable test statistic

3. **Hotelling's T²**
   - Multivariate t-test
   - For comparing single observation to distribution
   - Assumes normality

**Use Cases:**

**GLUE Benchmark (9 tasks):**
```python
# Detect if model cheats across multiple NLU tasks
glue_tasks = ['cola', 'sst2', 'mrpc', 'qqp', 'mnli', 'qnli', 'rte', 'wnli', 'stsb']
result = detect_multitask_bias(models, X_dict, y_dict, accuracy_score)
```

**MMLU Benchmark (57 subtasks):**
```python
# Detect systematic bias across knowledge domains
mmlu_tasks = ['abstract_algebra', 'anatomy', 'astronomy', ...]  # 57 tasks
result = detect_multitask_bias(models, X_dict, y_dict, accuracy_score)
```

**Multiple Metrics:**
```python
# Test accuracy, F1, precision, recall jointly
metrics = [accuracy_score, f1_score, precision_score, recall_score]
result = detect_multivariate_bias(model, X, y, metrics)
```

## 📊 Complete Usage Example

```python
from cbd.api import detect_bias
from cbd.prompt_analysis import detect_prompt_constraint_cheating
from cbd.multivariate_detection import detect_multivariate_bias
from cbd.risk_summary import (
    generate_risk_summary,
    generate_prompt_risk_summary,
    generate_multivariate_risk_summary,
    create_risk_report
)
from sklearn.metrics import accuracy_score, f1_score, precision_score

# 1. Standard bias detection
result = detect_bias(
    model, X, y, accuracy_score,
    n_permutations=1000,
    stratify=True,
    random_state=42
)

# Get plain language summary
summary = generate_risk_summary(result, "accuracy")
print(summary)
# "⚠️ 高风险：accuracy异常高 (观测值=0.950, p=0.0080)，
#  性能随计算资源线性增长（ρ_PC=0.78），可能存在调参作弊"

# 2. Prompt constraint analysis
prompts = [...]  # Your evaluation prompts
scores = [...]   # Corresponding performance scores

prompt_result = detect_prompt_constraint_cheating(prompts, scores)
prompt_summary = generate_prompt_risk_summary(prompt_result)
print(prompt_summary)
# "🚨 高风险：大量提示词异常相似但性能波动（15组可疑配对），
#  强烈怀疑通过提示词微调来操纵评测结果"

# 3. Multivariate detection
metrics = [accuracy_score, f1_score, precision_score]
multi_result = detect_multivariate_bias(
    model, X, y, metrics,
    metric_names=['Accuracy', 'F1', 'Precision'],
    method='energy',
    n_permutations=1000
)

multi_summary = generate_multivariate_risk_summary(
    multi_result,
    ['Accuracy', 'F1', 'Precision']
)
print(multi_summary)
# "🚨 高风险：Accuracy, F1, Precision联合显示异常（Energy Distance, p=0.0023），
#  多维度作弊模式，建议全面审查"

# 4. Generate comprehensive report
full_report = create_risk_report(result, "accuracy", include_technical=True)
print(full_report)
```

## 🔧 Installation

```bash
# Core package (already installed)
pip install circular-bias-detector

# For prompt analysis (new dependency)
pip install sentence-transformers

# For multivariate tests (optional, usually already installed)
pip install scipy scikit-learn
```

## 📈 Performance

**Prompt Analysis:**
- Similarity computation: ~50ms per prompt pair (CPU)
- GPU acceleration available with sentence-transformers
- Batch processing for efficiency

**Multivariate Detection:**
- Energy distance: O(n²) for n permutations
- MANOVA: O(n·m²) for m metrics
- Parallel execution supported

**Risk Summary:**
- Generation: <1ms (pure Python)
- No additional overhead

## 🎓 Best Practices

### When to Use Prompt Analysis

**Always use when:**
- Evaluating LLMs with custom prompts
- Comparing different prompt formulations
- Suspicious performance variation across similar tasks

**Example scenarios:**
- Few-shot learning with varying examples
- Instruction tuning evaluation
- Prompt engineering competitions

### When to Use Multivariate Detection

**Always use when:**
- Testing multiple metrics simultaneously
- Evaluating multi-task benchmarks (GLUE, MMLU, etc.)
- Individual tests show borderline results

**Example scenarios:**
- GLUE: 9 tasks, test jointly
- MMLU: 57 subtasks, test by domain
- Multiple metrics: accuracy + F1 + precision + recall

### Choosing Multivariate Method

| Method | Use When | Pros | Cons |
|--------|----------|------|------|
| Energy | Default choice | Robust, no assumptions | Slower for large n |
| MANOVA | Data looks normal | Interpretable, fast | Assumes normality |
| Hotelling | Single vs. distribution | Classic, well-studied | Assumes normality |

## 🔄 Backward Compatibility

**100% Backward Compatible:**
- All new modules are independent
- Existing code runs without changes
- New features are opt-in

## 📦 Package Updates

**New Dependencies:**
- `sentence-transformers` (optional, for prompt analysis)
- `scipy` (usually already installed)

**Version:**
- 1.3.1 → 1.4.0

## 🧪 Testing

**New Test Suite:**
- `tests/test_advanced_features.py`
- 20+ test cases
- Coverage: 90%+

**Run Tests:**
```bash
pytest tests/test_advanced_features.py -v
pytest tests/test_advanced_features.py::TestPromptAnalysis -v
pytest tests/test_advanced_features.py::TestMultivariateDetection -v
```

## 📚 Real-World Examples

### Example 1: GLUE Benchmark Validation

```python
from cbd.multivariate_detection import detect_multitask_bias
from cbd.risk_summary import generate_multivariate_risk_summary

# Load GLUE models and data
glue_models = {...}  # 9 task-specific models
glue_X = {...}       # Test data for each task
glue_y = {...}       # Labels for each task

# Joint detection
result = detect_multitask_bias(
    glue_models, glue_X, glue_y,
    accuracy_score,
    method='energy',
    n_permutations=1000
)

# Plain language summary
summary = generate_multivariate_risk_summary(result, list(glue_models.keys()))
print(summary)

# Check individual tasks
for task, stats in result['task_stats'].items():
    print(f"{task}: {stats['observed']:.3f} (p={stats['p_value']:.4f})")
```

### Example 2: Prompt Engineering Detection

```python
from cbd.prompt_analysis import (
    detect_prompt_constraint_cheating,
    batch_prompt_analysis
)
from cbd.risk_summary import generate_prompt_risk_summary

# Analyze prompts from different models
prompt_groups = {
    'model_A': [...],  # Prompts used by model A
    'model_B': [...],  # Prompts used by model B
    'model_C': [...]   # Prompts used by model C
}

performance_groups = {
    'model_A': [...],  # Scores for model A
    'model_B': [...],  # Scores for model B
    'model_C': [...]   # Scores for model C
}

# Batch analysis
results = batch_prompt_analysis(prompt_groups, performance_groups)

# Check each model
for model_name, result in results.items():
    if 'cheating_detection' in result:
        summary = generate_prompt_risk_summary(result['cheating_detection'])
        print(f"{model_name}: {summary}")
```

### Example 3: Comprehensive Multi-Metric Validation

```python
from cbd.multivariate_detection import (
    detect_multivariate_bias,
    compute_multivariate_psi
)

# Test multiple metrics jointly
metrics = [accuracy_score, f1_score, precision_score, recall_score]
metric_names = ['Accuracy', 'F1', 'Precision', 'Recall']

# Multivariate bias detection
bias_result = detect_multivariate_bias(
    model, X, y, metrics,
    metric_names=metric_names,
    method='energy',
    n_permutations=1000,
    n_jobs=-1  # Use all CPUs
)

# Multivariate PSI (if testing multiple models)
performance_matrix = np.array([...])  # Shape: (n_models, n_metrics)
costs = np.array([...])               # Model sizes

psi_result = compute_multivariate_psi(performance_matrix, costs)

# Generate summaries
print(generate_multivariate_risk_summary(bias_result, metric_names))
print(psi_result['conclusion'])
```

## 🐛 Known Limitations

1. **Prompt Analysis:**
   - Requires sentence-transformers (large download ~400MB)
   - GPU recommended for large prompt sets (>100 prompts)
   - English prompts work best (use multilingual model for others)

2. **Multivariate Detection:**
   - Computational cost grows with number of metrics/tasks
   - MANOVA assumes normality (use energy distance if unsure)
   - Requires sufficient permutations (≥1000 recommended)

3. **Risk Summary:**
   - Currently supports Chinese and English
   - Technical terms may need domain knowledge

## 🔮 Future Enhancements

**Potential v1.5 Features:**
- Automated prompt clustering and analysis
- Time-series bias detection
- Causal inference for bias sources
- Integration with popular LLM evaluation frameworks

## 📞 Support

**Issues:** https://github.com/hongping-zh/circular-bias-detection/issues
**Discussions:** https://github.com/hongping-zh/circular-bias-detection/discussions
**Email:** yujjam@uest.edu.gr

---

**Version:** 1.4.0  
**Release Date:** 2025-11-19  
**Status:** Production Ready ✅
