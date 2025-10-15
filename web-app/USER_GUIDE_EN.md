# 🔍 Sleuth - User Guide

**AI Evaluation Bias Hunter**

**Live Demo:** https://hongping-zh.github.io/circular-bias-detection/

## 📖 What is Sleuth?

Sleuth is a free, browser-based tool for detecting circular reasoning bias in AI algorithm evaluation. Think of it as your AI detective for spotting manipulated benchmarks. It identifies when evaluation protocols have been manipulated to favor specific algorithms, ensuring research integrity and fair comparisons.

### 🔢 Circular Bias Score: Mathematical Definition

The **Circular Bias Score (CBS)** is a composite metric ranging from 0 to 1, where:
- **CBS = 0**: No circular bias detected (ideal)
- **CBS = 1**: Maximum circular bias (highly problematic)

**Formula:**

```
CBS = w₁ · ψ(PSI) + w₂ · ψ(CCS) + w₃ · ψ(ρ_PC)

where:
  ψ(x) = normalized indicator score [0, 1]
  w₁, w₂, w₃ = weights (default: 1/3 each)
```

**Component Indicators:**

1. **PSI (Performance-Structure Independence):**
   ```
   PSI = (1/T) Σᵢ₌₁ᵀ ||θᵢ - θᵢ₋₁||₂
   
   where:
     θᵢ = parameter vector at time period i
     T = total time periods
     ||·||₂ = L2 norm
   ```
   
   **Statistical Meaning:** Measures parameter drift. High PSI indicates parameters were adjusted between evaluations, suggesting iterative tuning.

2. **CCS (Constraint-Consistency Score):**
   ```
   CCS = 1 - (1/p) Σⱼ₌₁ᵖ CV(cⱼ)
   
   where:
     CV(cⱼ) = coefficient of variation for constraint j
     p = number of constraints
   ```
   
   **Statistical Meaning:** Measures constraint stability. Low CCS indicates inconsistent evaluation conditions.

3. **ρ_PC (Performance-Constraint Correlation):**
   ```
   ρ_PC = Pearson(P, C̄)
   
   where:
     P = performance vector across time
     C̄ = mean constraint vector across time
   ```
   
   **Statistical Meaning:** Correlation coefficient. High |ρ_PC| suggests constraints were adjusted to improve performance.

**Interpretation:**
- **CBS < 0.3:** Low risk - Evaluation likely sound
- **0.3 ≤ CBS < 0.6:** Medium risk - Review methodology
- **CBS ≥ 0.6:** High risk - Strong evidence of circular bias

### Why Use This Tool?

**Traditional bias detection tools focus on model outputs** (e.g., fairness in predictions). **This tool focuses on the evaluation process itself** - detecting whether the rules of the game were changed mid-evaluation to produce desired results.

**Use cases:**
- 📄 Reviewing algorithm comparison papers
- 🔍 Auditing published evaluation methodologies
- ✅ Verifying research integrity before publication
- 🎓 Teaching research methodology best practices

---

## ✨ Key Features

### 🚀 Zero Installation
- No signup required
- No software installation
- Works directly in your web browser
- Compatible with Chrome, Firefox, Safari, Edge

### 🔒 Privacy First
- **100% client-side processing**
- Your data never leaves your computer
- No server uploads
- No data collection or tracking

### ⚡ Fast Results
- Detection completes in < 30 seconds
- Instant visual feedback
- Three statistical indicators (PSI, CCS, ρ_PC)
- Clear interpretation and confidence scores

### 📊 Multiple Data Sources
- **Upload your own CSV** - Analyze your evaluation data
- **Use example data** - Try with sample from Zenodo dataset
- **Generate synthetic data** - Test with simulated scenarios

### 📥 Export & Share
- Download results as JSON
- Copy citation with one click
- Share results with collaborators

---

## 📋 Data Preparation

### Required Data Format

Your CSV file must include these **required columns:**

| Column | Type | Range | Description |
|--------|------|-------|-------------|
| `time_period` | integer | ≥ 1 | Sequential evaluation period |
| `algorithm` | string | - | Algorithm name or identifier |
| `performance` | float | [0, 1] | Normalized performance metric |

### Optional Constraint Columns

Include at least one constraint to enable full analysis:

| Column | Type | Description | Example Values |
|--------|------|-------------|----------------|
| `constraint_compute` | float | Computational budget (FLOPs, GPU hours) | 100, 500, 1000 |
| `constraint_memory` | float | Memory limit (GB) | 8.0, 16.0, 32.0 |
| `constraint_dataset_size` | integer | Training dataset size | 10000, 50000, 100000 |
| `evaluation_protocol` | string | Protocol version identifier | "v1.0", "baseline" |

### LLM-Specific Columns (Optional)

For LLM evaluation analysis:

| Column | Type | Description | Example Values |
|--------|------|-------------|----------------|
| `max_tokens` | integer | Maximum generation length | 256, 512, 1024 |
| `temperature` | float | Sampling temperature | 0.5, 0.7, 1.0 |
| `top_p` | float | Nucleus sampling parameter | 0.9, 0.95, 1.0 |
| `prompt_variant` | string | Prompting technique | "zero-shot", "few-shot", "CoT" |

### Data Requirements

**Minimum data size:**
- ✅ At least **2 algorithms**
- ✅ At least **3 time periods** (recommended: 5+)
- ✅ At least **1 constraint column**

**Data quality:**
- ✅ No missing values in required columns
- ✅ Performance values normalized to [0, 1]
- ✅ Time periods are sequential (1, 2, 3, ...)
- ✅ Consistent algorithm names across periods

### Example CSV Format

```csv
time_period,algorithm,performance,constraint_compute,constraint_memory,constraint_dataset_size,evaluation_protocol
1,ResNet,0.72,300,8.0,50000,ImageNet-v1.0
1,VGG,0.68,450,12.0,50000,ImageNet-v1.0
1,DenseNet,0.75,280,9.0,50000,ImageNet-v1.0
2,ResNet,0.74,305,8.2,51000,ImageNet-v1.0
2,VGG,0.70,455,12.1,51000,ImageNet-v1.0
2,DenseNet,0.77,285,9.1,51000,ImageNet-v1.0
3,ResNet,0.76,310,8.5,52000,ImageNet-v1.1
3,VGG,0.72,460,12.3,52000,ImageNet-v1.1
3,DenseNet,0.79,290,9.3,52000,ImageNet-v1.1
```

### Common Issues and Solutions

**❌ Issue:** "Missing required columns: performance"
- **Solution:** Rename your metric column to `performance`
- If using accuracy/F1/AUC, normalize to [0, 1] range

**❌ Issue:** "Row 5: 'performance' must be a number"
- **Solution:** Remove non-numeric values (e.g., "N/A", "-", empty cells)
- Replace missing values with interpolation or mean

**❌ Issue:** "At least 2 different algorithms required"
- **Solution:** Include evaluations of multiple algorithms
- Each algorithm should appear in multiple time periods

**⚠️ Warning:** "Minimum 3 time periods recommended"
- **Impact:** Results may be less reliable with < 3 periods
- **Recommendation:** Collect data from more evaluation iterations

### Handling Sparse Data

**Cold start problem:**
- If some algorithms don't appear in early periods, use synthetic baseline values or skip those periods
- Ensure at least 70% data completeness

**Missing constraints:**
- Tool can work with performance-only data, but constraint analysis will be limited
- Include as many constraint columns as available

### Sample Datasets

Download ready-to-use example datasets:

1. **Computer Vision** (ImageNet evaluation)
   - `data/sample_data.csv`
   - 4 algorithms, 5 time periods

2. **LLM Benchmarking** (GLUE scores)
   - `data/llm_eval_sample.csv`
   - 4 models, 5 prompt variants

3. **Synthetic Data** (Monte Carlo simulation)
   - Generate within the tool
   - Customizable parameters

---

## 🎯 How to Use

### Step 1: Access the Tool

Visit: **https://hongping-zh.github.io/circular-bias-detection/**

**First-time loading:** The Python engine (PyOdide) may take 30-60 seconds to load. This only happens once - subsequent visits are instant.

**Note:** Current version uses test mode with mock data. Full Python detection coming soon.

---

### Step 2: Load Your Data

You have three options:

#### Option A: Upload Your Own Data 📁

1. Click **"📁 Upload Your Data"** or drag & drop your CSV file
2. Ensure your CSV has these required columns:

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `time_period` | int | Evaluation period (1, 2, 3...) | 1, 2, 3... |
| `algorithm` | string | Algorithm name | ResNet, VGG |
| `performance` | float | Performance score [0-1] | 0.72, 0.85 |
| `constraint_compute` | float | Computational limit | 300, 450 |
| `constraint_memory` | float | Memory limit (GB) | 8.0, 12.0 |
| `constraint_dataset_size` | int | Dataset size | 50000, 100000 |
| `evaluation_protocol` | string | Protocol version | v1.0, v1.1 |

3. After upload, you'll see: **✓ your_file.csv**

**Example CSV format:**
```csv
time_period,algorithm,performance,constraint_compute,constraint_memory,constraint_dataset_size,evaluation_protocol
1,ResNet,0.72,300,8.0,50000,ImageNet-v1.0
1,VGG,0.68,450,12.0,50000,ImageNet-v1.0
2,ResNet,0.73,305,8.2,51000,ImageNet-v1.0
2,VGG,0.69,455,12.1,51000,ImageNet-v1.0
```

#### Option B: Try Example Data 📊

1. Click **"📊 Try Example from Zenodo"**
2. Pre-loaded data from our research dataset (DOI: 10.5281/zenodo.17201032)
3. Perfect for first-time users to understand the tool

#### Option C: Generate Synthetic Data 🎲

1. Click **"🎲 Generate Synthetic Data"**
2. Automatically creates random evaluation data
3. Useful for testing and demonstrations

---

### Step 3: Run Detection

1. After loading data, the **"🔍 Scan for Bias"** button becomes active (green)
2. Click the button to start analysis
3. Button changes to **"Scanning..."** (orange) while processing
4. Wait 1-2 seconds for results

---

### Step 4: Interpret Results

The results dashboard displays three key indicators:

#### 📊 PSI Score (Performance-Structure Independence)
- **What it measures:** Parameter stability over time
- **Default Threshold:** 0.15
- **Recommended Range:** [0.10, 0.20]
- **Interpretation:**
  - PSI < 0.10: ✅ Stable (Good)
  - 0.10 ≤ PSI < 0.15: ⚠️ Moderate
  - PSI ≥ 0.15: ❌ Unstable (Potential Bias)

**Example:** PSI = 0.0158 → Parameters are very stable, evaluation is consistent.

**Threshold Guidelines:**
- **Strict (0.10):** Use for high-stakes evaluations (e.g., benchmark leaderboards)
- **Standard (0.15):** Default for most research evaluations
- **Lenient (0.20):** For exploratory or early-stage research

**What causes high PSI?**
- Hyperparameter changes between evaluations
- Different random seeds affecting model initialization
- Architecture modifications during evaluation
- Training procedure adjustments

#### 📊 CCS Score (Constraint-Consistency Score)
- **What it measures:** Consistency of constraint specifications
- **Default Threshold:** 0.85
- **Recommended Range:** [0.80, 0.90]
- **Interpretation:**
  - CCS ≥ 0.90: ✅ Highly Consistent (Good)
  - 0.85 ≤ CCS < 0.90: ⚠️ Moderate
  - CCS < 0.85: ❌ Inconsistent (Potential Bias)

**Example:** CCS = 0.9422 → Constraints are highly consistent across periods.

**Threshold Guidelines:**
- **Strict (0.90):** For controlled experiments requiring high reproducibility
- **Standard (0.85):** Default for typical evaluation scenarios
- **Lenient (0.80):** For evaluations with expected constraint variations

**What causes low CCS?**
- Computational budget changes between periods
- Memory limit adjustments
- Dataset size variations
- Hardware upgrades/changes
- Protocol version updates without documentation

**Note:** Some variation is normal (e.g., dataset size growing over time). Focus on **systematic changes** that correlate with performance improvements.

#### 📊 ρ_PC Score (Performance-Constraint Correlation)
- **What it measures:** Correlation between performance and constraints
- **Default Threshold:** ±0.5
- **Recommended Range:** [0.40, 0.60]
- **Interpretation:**
  - |ρ_PC| < 0.3: ✅ Weak Correlation (Good)
  - 0.3 ≤ |ρ_PC| < 0.5: ⚠️ Moderate
  - |ρ_PC| ≥ 0.5: ❌ Strong Correlation (Potential Bias)

**Example:** ρ_PC = +0.9921 → Very strong positive correlation, constraints may have been tuned to performance.

**Threshold Guidelines:**
- **Strict (0.40):** For high-impact publications
- **Standard (0.50):** Default for most research
- **Lenient (0.60):** For preliminary studies

**Interpreting correlation sign:**
- **Positive ρ_PC:** Performance increases as constraints loosen
  - Could indicate: Resources were increased to improve scores
  - Natural in some cases (more compute → better results)
  - **Red flag:** If constraints increased *only* for best-performing models

- **Negative ρ_PC:** Performance increases as constraints tighten
  - **Strong red flag:** Suggests evaluation was gamed
  - Could indicate: Cherry-picking favorable test conditions

**What causes high |ρ_PC|?**
- Adjusting computational budget based on preliminary results
- Increasing dataset size after seeing performance plateau
- Tuning memory limits to favor specific architectures
- Protocol changes triggered by poor initial results

#### 🎯 Overall Decision

The tool combines all three indicators:

- **Bias Detected:** ≥2 of 3 indicators triggered
- **No Bias:** <2 indicators triggered
- **Confidence:** Percentage of indicators triggered (33.3%, 66.7%, or 100%)

**Example result:**
```
Overall Bias Detected: NO ✓
Confidence: 33.3%

Interpretation:
No circular bias detected (confidence: 33.3%). 
Evaluation appears sound.
```

#### 📈 NEW: Statistical Significance (Bootstrap Confidence Intervals)

**Enhanced version includes:**
- **Confidence Intervals:** 95% CI computed via bootstrap resampling (n=1000)
- **P-values:** Statistical significance testing
- **Adaptive Thresholds:** Data-driven threshold selection

**Example enhanced output:**
```
PSI Score:  0.0238 [0.0113-0.0676], p=0.355
CCS Score:  0.8860 [0.8723-0.9530], p=0.342
ρ_PC Score: +0.9983 [+0.9972-+1.0000], p=0.772
```

**Interpretation:**
- **[Lower-Upper]:** 95% confidence interval
- **p-value:** Statistical significance (p < 0.05 = significant)
- Narrower intervals = more precise estimates
- p < 0.05 = statistically significant bias

**Adaptive Thresholds:**
Instead of fixed thresholds (PSI=0.15, CCS=0.85, ρ_PC=0.5), the system can compute data-specific thresholds at the 95th percentile of null distributions, reducing false positives.

---

### Step 5: Export & Share

#### Download Report 📥
1. Click **"📥 Download Report (JSON)"**
2. A JSON file downloads with complete results
3. Share with reviewers or archive for records

**JSON format:**
```json
{
  "psi": 0.0158,
  "ccs": 0.9422,
  "rho_pc": 0.9921,
  "overall_bias": false,
  "confidence": 0.333,
  "details": {
    "algorithms_evaluated": ["ResNet", "VGG", "DenseNet", "EfficientNet"],
    "time_periods": 5,
    "indicators_triggered": 1
  }
}
```

#### Copy Citation 📋
1. Click **"📋 Copy Citation"**
2. BibTeX citation copied to clipboard
3. Paste into your paper's references

#### Start New Analysis ↻
- Click **"← New Scan"** to return to data input
- Analyze different datasets

---

## 🔬 Technical Specifications

### Statistical Methods

#### PSI (Performance-Structure Independence)
```
PSI = mean(|Δθ_t|)
```
Measures absolute changes in parameters over time periods.

#### CCS (Constraint-Consistency Score)
```
CCS = mean(corr(C_i, C_j)) for all period pairs
```
Calculates average correlation between constraint vectors across time.

#### ρ_PC (Performance-Constraint Correlation)
```
ρ_PC = Pearson(mean(P_t), mean(C_t))
```
Computes correlation between average performance and constraint intensity.

### Decision Framework

```
overall_bias = (PSI > 0.15) + (CCS < 0.85) + (|ρ_PC| > 0.5) ≥ 2
confidence = (indicators_triggered / 3) × 100%
```

---

## 💡 Best Practices

### Data Preparation

1. **Minimum data requirements:**
   - At least 3 time periods (T ≥ 3)
   - At least 2 algorithms (K ≥ 2)
   - At least 2 constraint types (p ≥ 2)

2. **Ensure data quality:**
   - No missing values
   - Consistent algorithm names across periods
   - Performance values in [0, 1] range
   - Positive constraint values

3. **Time period definition:**
   - Each row represents one algorithm in one period
   - Periods should be sequential (1, 2, 3, ...)
   - All algorithms should appear in each period

### Interpretation Guidelines

1. **Single indicator triggered:**
   - Investigate further but not conclusive
   - May be due to natural variation
   - Check data quality

2. **Two indicators triggered:**
   - Strong evidence of potential bias
   - Recommend detailed manual review
   - Consider additional validation

3. **All three indicators triggered:**
   - High confidence of circular bias
   - Evaluation methodology likely manipulated
   - Results should not be trusted

### Common Pitfalls

❌ **Don't:**
- Use data with < 3 time periods
- Mix different evaluation tasks
- Include missing values
- Compare across different benchmarks

✅ **Do:**
- Use consistent evaluation protocols
- Include all constraint types
- Document any protocol changes
- Archive raw data for reproducibility

---

## 🤖 LLM Evaluation Use Cases

### Detecting Bias in Large Language Model Benchmarking

The tool now supports detecting circular bias in LLM evaluations where prompt engineering and sampling parameters are iteratively tuned.

### LLM-Specific Data Format

In addition to standard columns, include LLM-specific constraints:

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `max_tokens` | int | Maximum generation length | 512, 1024, 2048 |
| `temperature` | float | Sampling temperature | 0.7, 0.8, 0.9 |
| `top_p` | float | Nucleus sampling | 0.9, 0.95, 1.0 |
| `prompt_variant` | str | Prompting technique | vanilla, few-shot, chain-of-thought |

### Example LLM Dataset

See `data/llm_eval_sample.csv` for a complete example with:
- **Models:** GPT-3.5, Llama-2-7B, Claude-Instant, Mistral-7B
- **Benchmark:** GLUE scores
- **Prompt evolution:** vanilla → few-shot → chain-of-thought → role-play → system-prompt
- **Parameter tuning:** Temperature increases from 0.7 to 0.9 over time

### Interpretation for LLM Evaluations

**High ρ_PC (>0.5) indicates:**
- Sampling parameters (temperature, top_p) were adjusted based on performance
- Prompt engineering strategies were iteratively refined to improve scores
- Max token limits were tuned to favor certain models

**Example warning:**
```
⚠️ High correlation detected (ρ_PC = 0.99)

Sampling parameters and prompt strategies may have been iteratively 
adjusted to inflate benchmark scores. This suggests potential circular 
bias where the evaluation protocol was tailored to favor certain models.
```

### Best Practices for LLM Evaluation

✅ **Do:**
- Pre-register prompt templates before evaluation
- Fix sampling parameters (temperature, top_p) across all runs
- Document any protocol changes explicitly
- Report all attempted prompting strategies (not just best-performing)

❌ **Don't:**
- Tune temperature based on preliminary results
- Cherry-pick best-performing prompt variants
- Adjust max_tokens to improve specific model scores
- Iterate on prompts until target performance is reached

---

## ❓ Frequently Asked Questions

### General Questions

**Q: Is this tool free?**  
A: Yes, completely free and open-source (CC BY 4.0).

**Q: Do I need to create an account?**  
A: No, no signup or registration required.

**Q: Is my data safe?**  
A: Yes, all processing happens locally in your browser. Data never leaves your computer.

**Q: What browsers are supported?**  
A: Chrome, Firefox, Safari, Edge - any modern browser with JavaScript enabled.

### Technical Questions

**Q: How accurate is the detection?**  
A: 93.2% accuracy on synthetic scenarios, 87-91% on real-world case studies (see paper).

**Q: Can I adjust the thresholds?**  
A: Web App uses default thresholds. Use the CLI tool for custom thresholds:
```bash
circular-bias detect data.csv --psi-threshold 0.2 --ccs-threshold 0.8
```

**Q: What if I only have 2 time periods?**  
A: Minimum 3 periods required for reliable detection. With 2 periods, results may be unreliable.

**Q: Can I analyze multiple evaluation tasks?**  
A: Analyze each task separately. Don't mix ImageNet and GLUE evaluations in one analysis.

### Data Format Questions

**Q: My CSV has different column names. Can I use it?**  
A: Column names must match exactly. Rename columns in your spreadsheet before upload.

**Q: What if I have more than 3 constraints?**  
A: Include all constraint columns (constraint_*). The tool will analyze all of them.

**Q: Can I use accuracy instead of performance?**  
A: Yes, but normalize to [0, 1] range and rename column to `performance`.

**Q: What should I put in evaluation_protocol?**  
A: Any version identifier (e.g., "v1.0", "baseline", "protocol_A"). Should change when protocols change.

### Results Interpretation

**Q: All three indicators are green, but I suspect bias. Why?**  
A: The tool detects statistical patterns. Manual review is always recommended for critical decisions.

**Q: One indicator is red, should I be worried?**  
A: Single indicator may be false positive. Investigate but not conclusive. Focus on 2+ indicators.

**Q: Can the tool detect other types of bias?**  
A: No, this tool specifically detects **circular reasoning bias** in evaluation protocols. For model output bias, use tools like AIF360 or Fairlearn.

### Troubleshooting

**Q: Page stuck on "Loading Python engine..."**  
A: First load takes 30-60 seconds. Refresh page if stuck > 2 minutes. Current test version skips this.

**Q: Upload button doesn't work**  
A: Ensure your file is CSV format and < 10MB. Try different browser if issue persists.

**Q: Results show "NaN" or errors**  
A: Check data format, ensure no missing values, verify all required columns present.

---

## 📚 Additional Resources

### Documentation
- **GitHub Repository:** https://github.com/hongping-zh/circular-bias-detection
- **Research Paper:** (Submitted to JASA)
- **Dataset:** https://doi.org/10.5281/zenodo.17201032

### CLI Tool
For advanced users and automation:
```bash
pip install circular-bias-detector[cli]
circular-bias detect data.csv --format json
```

### Python API
For integration into your workflow:
```python
from circular_bias_detector import BiasDetector
detector = BiasDetector()
results = detector.detect_bias(performance_matrix, constraint_matrix)
```

### Support
- **Issues:** https://github.com/hongping-zh/circular-bias-detection/issues
- **Email:** yujjam@uest.edu.gr

---

## 📄 Citation

If you use this tool in your research, please cite:

```bibtex
@software{zhang2024biasscanner,
  author = {Zhang, Hongping},
  title = {Circular Bias Scanner: Web Tool for Evaluation Bias Detection},
  year = {2024},
  url = {https://hongping-zh.github.io/circular-bias-detection/}
}

@dataset{zhang2024dataset,
  author = {Zhang, Hongping},
  title = {Algorithm Benchmark Suite v2.0: Synthetic Dataset for Circular Bias Detection},
  year = {2024},
  publisher = {Zenodo},
  doi = {10.5281/zenodo.17201032}
}
```

---

## 📝 License

CC BY 4.0 - Free to use, share, and adapt with attribution.

---

**Version:** 1.0.0 (MVP - Test Mode)  
**Last Updated:** October 2024  
**Feedback:** https://github.com/hongping-zh/circular-bias-detection/issues
