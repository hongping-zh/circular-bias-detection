# LLM Evaluation Bias Detection Guide

## 🎯 Overview

This guide demonstrates how to use Sleuth to detect circular bias in Large Language Model (LLM) evaluation, particularly when:
- Prompt engineering techniques are iteratively refined
- Sampling parameters (temperature, top_p) are tuned based on observed scores
- Evaluation protocols change between benchmark runs

## 🔍 Why LLM Evaluation is Susceptible to Circular Bias

Unlike traditional ML models, LLM evaluation involves many degrees of freedom:

| Factor | Traditional ML | LLM Evaluation | Risk Level |
|--------|---------------|----------------|------------|
| **Prompt Design** | N/A | Vanilla → Few-shot → CoT → System prompts | ⚠️ HIGH |
| **Sampling Params** | Fixed | Temperature, top_p, top_k tuning | ⚠️ HIGH |
| **Context Length** | Fixed | max_tokens adaptation | ⚠️ MEDIUM |
| **Dataset** | Train/test split | In-context examples selection | ⚠️ HIGH |
| **Evaluation Metric** | Fixed | Multiple metrics cherry-picking | ⚠️ HIGH |

**⚠️ Warning:** Each of these adjustments, when done iteratively based on observed scores, can introduce circular bias that inflates reported performance.

---

## 📊 Quick Start Example

### 1. Prepare Your Data

Your CSV should include LLM-specific constraints:

```csv
time_period,algorithm,performance,constraint_compute,constraint_memory,constraint_dataset_size,max_tokens,temperature,top_p,prompt_variant
1,GPT-4,0.72,300,8.0,50000,512,0.7,0.9,vanilla
1,Claude-3,0.68,450,12.0,50000,512,0.7,0.9,vanilla
2,GPT-4,0.76,310,8.5,52000,768,0.8,0.95,few_shot
2,Claude-3,0.73,455,12.1,52000,768,0.8,0.95,few_shot
```

**Key columns:**
- `time_period`: Evaluation iteration (1, 2, 3, ...)
- `algorithm`: LLM name
- `performance`: GLUE/MMLU/HumanEval score
- `max_tokens`: Generation length limit
- `temperature`: Sampling temperature
- `top_p`: Nucleus sampling parameter
- `prompt_variant`: Prompt engineering technique

### 2. Run Detection with Bootstrap

```python
import pandas as pd
from circular_bias_detector import BiasDetector

# Load data
df = pd.read_csv('data/llm_eval_sample.csv')

# Prepare matrices
performance_matrix = df.pivot(
    index='time_period',
    columns='algorithm',
    values='performance'
).values

# Include LLM-specific constraints
constraint_matrix = df.groupby('time_period')[[
    'constraint_compute',
    'constraint_memory',
    'constraint_dataset_size',
    'max_tokens',      # LLM-specific
    'temperature',     # LLM-specific
    'top_p'            # LLM-specific (optional)
]].first().values

# Run detection with bootstrap (recommended for LLMs)
detector = BiasDetector(
    psi_threshold=0.15,
    ccs_threshold=0.85,
    rho_pc_threshold=0.5
)

results = detector.detect_bias(
    performance_matrix=performance_matrix,
    constraint_matrix=constraint_matrix,
    algorithm_names=df['algorithm'].unique().tolist(),
    enable_bootstrap=True,      # ✨ Get confidence intervals
    n_bootstrap=1000,
    enable_adaptive_thresholds=True  # ✨ Data-driven thresholds
)

# Display results
print(f"PSI = {results['psi_score']:.4f} "
      f"[{results['psi_ci_lower']:.4f}-{results['psi_ci_upper']:.4f}], "
      f"p={results['psi_pvalue']:.3f}")

print(f"ρ_PC = {results['rho_pc_score']:+.4f} "
      f"[{results['rho_pc_ci_lower']:+.4f}-{results['rho_pc_ci_upper']:+.4f}], "
      f"p={results['rho_pc_pvalue']:.3f}")
```

### 3. Interpret Results

**High ρ_PC (> 0.5):**
```
⚠️  High correlation detected: sampling parameters may have been
    iteratively adjusted to inflate benchmark scores.
    
    LIKELY CAUSES:
    - Temperature increased when scores were low
    - top_p tuned to maximize specific metrics
    - Prompt variants correlated with constraint changes
    
    RECOMMENDATION:
    - Pre-register evaluation protocol
    - Fix all sampling parameters before experiments
    - Use separate validation set for hyperparameter tuning
```

**High PSI (> 0.15):**
```
⚠️  Parameter instability detected
    
    LIKELY CAUSES:
    - Model configurations changed between evaluations
    - Different model versions used
    - Inconsistent prompting strategies
```

**Low CCS (< 0.85):**
```
⚠️  Constraint inconsistency detected
    
    LIKELY CAUSES:
    - max_tokens varied significantly
    - Computational budget adjusted
    - Dataset size changed
```

---

## 🧪 Common LLM Bias Scenarios

### Scenario 1: Prompt Engineering Inflation

**Symptoms:**
- ρ_PC > 0.7 (very high correlation)
- Performance improves with each prompt variant
- Prompt changes: vanilla → few-shot → CoT → role-play

**Example:**
```python
# Time 1: Vanilla prompt, score = 0.72
# Time 2: Few-shot, score = 0.76
# Time 3: Chain-of-thought, score = 0.80
# Time 4: Role-play + examples, score = 0.85

# ⚠️  Each prompt variant was chosen because previous score was insufficient
# ✅ CORRECT: Pre-specify prompt variants, evaluate all, report all
```

### Scenario 2: Temperature Tuning

**Symptoms:**
- CCS < 0.8 (constraint inconsistency)
- Temperature increases over time: 0.7 → 0.8 → 0.9 → 1.0
- Scores improve with temperature

**Example:**
```python
# Detected: temperature values [0.7, 0.75, 0.8, 0.85, 0.9]
# Scores: [0.68, 0.71, 0.74, 0.78, 0.81]
# ρ_PC = +0.92 (p < 0.001) ⚠️

# INTERPRETATION: Temperature was tuned to improve scores
```

### Scenario 3: Context Length Optimization

**Symptoms:**
- max_tokens varies: 512 → 768 → 1024 → 2048
- High ρ_PC with max_tokens as constraint
- Longer contexts = higher scores

**Red flag:**
```python
# max_tokens: [512, 768, 1024, 2048]
# Scores:     [0.70, 0.74, 0.77, 0.82]
# CCS = 0.73 (< 0.85) ⚠️

# PROBLEM: Context length adjusted to improve metrics
```

---

## 📈 Advanced: Adaptive Thresholds for LLMs

LLM evaluation has higher natural variability. Use adaptive thresholds:

```python
results = detector.detect_bias(
    performance_matrix=performance_matrix,
    constraint_matrix=constraint_matrix,
    enable_adaptive_thresholds=True,  # ✨ Compute from data
    enable_bootstrap=True,
    n_bootstrap=1000
)

print(f"Adaptive PSI threshold: {results['metadata']['thresholds']['psi']:.4f}")
print(f"Adaptive ρ_PC threshold: {results['metadata']['thresholds']['rho_pc']:.4f}")
```

**When to use:**
- First-time LLM benchmark evaluation
- Multiple prompt variants legitimately needed
- Uncertain about appropriate fixed thresholds

---

## 🚀 Best Practices for Bias-Free LLM Evaluation

### ✅ DO:

1. **Pre-register evaluation protocol**
   - Specify all prompt variants before experiments
   - Fix sampling parameters (temperature, top_p, etc.)
   - Document all constraint choices upfront

2. **Use separate validation sets**
   - Tune hyperparameters on dev set
   - Report only test set results
   - Never iterate on test performance

3. **Report all evaluations**
   - Include failed prompt variants
   - Show all sampled configurations
   - Avoid metric cherry-picking

4. **Use bootstrap statistics**
   ```python
   detector.detect_bias(
       ...,
       enable_bootstrap=True,
       n_bootstrap=1000
   )
   ```

5. **Monitor LLM-specific constraints**
   ```python
   constraint_columns = [
       'max_tokens',
       'temperature',
       'top_p',
       'num_few_shot_examples',
       'prompt_length'
   ]
   ```

### ❌ DON'T:

1. **Don't tune sampling parameters based on observed scores**
   ```python
   # ❌ WRONG:
   if score < 0.75:
       temperature = 0.9  # Increase to improve
   
   # ✅ CORRECT:
   temperature = 0.7  # Fixed before experiments
   ```

2. **Don't iterate prompt engineering on test set**
   ```python
   # ❌ WRONG:
   for prompt_variant in ['vanilla', 'few_shot', 'cot']:
       score = evaluate(test_set, prompt_variant)
       if score > best_score:
           best_prompt = prompt_variant
   
   # ✅ CORRECT:
   # Tune prompts on dev set, evaluate once on test set
   ```

3. **Don't adjust constraints mid-evaluation**
   ```python
   # ❌ WRONG: max_tokens changed from 512 → 2048 during evaluation
   # ✅ CORRECT: Fix max_tokens=1024 for all runs
   ```

---

## 📚 Example Use Cases

### Use Case 1: GLUE Benchmark Audit

```python
# Scenario: Published paper reports GPT-4 scores improving over 5 iterations
# Goal: Check if prompt engineering introduced circular bias

df = pd.read_csv('glue_eval_logs.csv')
detector = BiasDetector()

results = detector.detect_bias(
    performance_matrix=...,
    constraint_matrix=...,  # Include prompt_variant as constraint
    enable_bootstrap=True
)

if results['rho_pc_pvalue'] < 0.05:
    print("⚠️  Significant correlation detected - likely circular bias")
```

### Use Case 2: Internal LLM Development

```python
# Scenario: Your team is developing a new LLM
# Goal: Ensure evaluation protocol is bias-free

# Step 1: Pre-register protocol
protocol = {
    'temperature': 0.7,
    'top_p': 0.9,
    'max_tokens': 1024,
    'prompt_template': 'fixed_template.txt',
    'evaluation_metrics': ['accuracy', 'F1', 'BLEU']
}

# Step 2: Run evaluation
results = evaluate_llm(model, test_set, protocol)

# Step 3: Check for bias
detector = BiasDetector()
bias_check = detector.detect_bias(..., enable_bootstrap=True)

# Step 4: Report
if not bias_check['overall_bias']:
    print("✅ Evaluation is bias-free - safe to publish")
else:
    print("⚠️  Circular bias detected - revise protocol")
```

---

## 🔗 Additional Resources

- **Sample Data**: `data/llm_eval_sample.csv`
- **Example Script**: `examples/llm_evaluation_example.py`
- **Web App**: Upload LLM evaluation logs to https://hongping-zh.github.io/circular-bias-detection/
- **Paper**: See README for citation details

---

## ❓ FAQ

**Q: Should I include prompt_variant as a constraint?**  
A: Yes! If prompts changed over time, include as categorical constraint (encode as numeric).

**Q: What's a "safe" ρ_PC value for LLMs?**  
A: |ρ_PC| < 0.3 is ideal. Values > 0.5 indicate likely circular bias.

**Q: Can I use this for ChatGPT API evaluations?**  
A: Yes! Include API parameters (temperature, presence_penalty, etc.) as constraints.

**Q: How many time periods do I need?**  
A: Minimum 3, ideally 5+ for reliable ρ_PC estimation.

**Q: What if my LLM evaluation legitimately needs parameter tuning?**  
A: Use separate dev/test splits. Tune on dev, freeze parameters, evaluate once on test.

---

## 🎯 Summary Checklist

Before publishing LLM evaluation results, verify:

- [ ] All prompts pre-registered before experiments
- [ ] Sampling parameters (temp, top_p) fixed across time periods
- [ ] Separate validation set used for hyperparameter tuning
- [ ] Test set evaluated only once with final configuration
- [ ] All constraint changes documented
- [ ] Bootstrap p-values computed (p > 0.05 for all indicators)
- [ ] |ρ_PC| < 0.5
- [ ] CCS > 0.85
- [ ] PSI < 0.15
- [ ] Bias detection report included in supplementary materials

---

**✅ Following these guidelines will ensure your LLM evaluation is scientifically rigorous and free from circular bias!**
