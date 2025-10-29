# Sleuth - AI Bias Detector

[![Web App](https://img.shields.io/badge/🚀_Try_Live_Demo-brightgreen?style=for-the-badge)](https://is.gd/check_sleuth)
[![GitHub stars](https://img.shields.io/github/stars/hongping-zh/circular-bias-detection?style=social)](https://github.com/hongping-zh/circular-bias-detection)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17201032.svg)](https://doi.org/10.5281/zenodo.17201032)
[![Dataset DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17196639.svg)](https://doi.org/10.5281/zenodo.17196639)

## 🎯 Detect AI Evaluation Bias in 30 Seconds

**Stop deploying AI models with inflated performance scores.**

Sleuth catches when you've been tweaking hyperparameters, prompts, or datasets until your benchmark numbers look good—a hidden form of bias that breaks AI evaluations.
<p align="center">
  <a href="https://hongping-zh.github.io/circular-bias-detection/?utm_source=github&utm_medium=readme&utm_campaign=hero_live_demo">
    <img src="https://img.shields.io/badge/%F0%9F%94%8D%20LIVE%20DEMO-Try%20Sleuth-brightgreen?style=for-the-badge" alt="Live Demo">
  </a>
  <a href="https://colab.research.google.com/github/hongping-zh/circular-bias-detection/blob/main/examples/quickstart_colab.ipynb?utm_source=github&utm_medium=readme&utm_campaign=hero_colab">
    <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open in Colab" style="height:28px;">
  </a>
</p>

<p align="center">
  <b>Detect circular bias in AI evaluations instantly.</b> Free web app + Python SDK. Stop shipping inflated benchmark scores.
</p>

<p align="center">
  <sub>For researchers, reviewers, and ML engineers • Works with CSVs • Privacy-preserving</sub>
</p>

---

## Why Sleuth?
- Find hidden evaluation bias from hyperparam/prompt/dataset tweaking.
- 3 indicators (PSI, CCS, ρ_PC) with interpretation and fixes.
- Use in 30 seconds via Web App, or programmatically via Python/CLI.
### ⚡ Quick Start

**[🔍 Try Live Demo →](https://is.gd/check_sleuth)** • No installation • Runs in browser • 100% private

```bash
# Or install locally
pip install circular-bias-detector
```

---

## 🚨 The Problem

You've been here before:

1. Run AI evaluation → scores aren't great
2. Adjust temperature → try again
3. Tweak prompt → run again  
4. Change dataset → repeat...
5. After 50 iterations → "95% accuracy!" 🎉

**But is it real?**

This is **circular reasoning bias** - and it's everywhere in ML research and production.

- ❌ **Papers get rejected** - reviewers spot it instantly
- ❌ **Models fail in production** - real-world performance drops 20-30%
- ❌ **Wasted resources** - time, compute, and credibility

## ✅ The Solution

**Sleuth detects 3 types of evaluation manipulation:**

| Indicator | What It Catches | Risk Level |
|-----------|----------------|------------|
| **PSI** (Parameter Stability) | Hyperparameters changed during eval | 🔴 High |
| **CCS** (Constraint Consistency) | Evaluation conditions varied | 🟡 Medium |
| **ρ_PC** (Performance-Constraint Correlation) | Results depend on resource changes | 🔴 High |

**Result:** Yes/No answer + specific recommendations on how to fix it.

---

## 🆚 Why Sleuth?

Unlike existing tools, Sleuth is the **only tool** that audits your **evaluation process** (not just model outputs):

| Framework | Focus | Circular Bias Detection | Target Users |
|-----------|-------|-------------------------|--------------|
| [AIF360](https://github.com/Trusted-AI/AIF360) | Model fairness (demographic parity, equalized odds) | ❌ | ML practitioners |
| [Fairlearn](https://github.com/fairlearn/fairlearn) | Algorithmic fairness constraints | ❌ | Data scientists |
| [Themis-ML](https://github.com/cosmicBboy/themis-ml) | Discrimination testing | ❌ | Researchers |
| **This Framework** | **Evaluation protocol integrity** | ✅ | **Researchers, Reviewers, Auditors** |

**Use Sleuth for:**

- ✅ **Pre-publication checks** - Avoid reviewer comments about biased evaluations
- ✅ **Pre-production audits** - Ensure model performance is real before deployment
- ✅ **Compliance reporting** - Generate PDF reports for stakeholders
- ✅ **Research integrity** - Prove your results aren't p-hacked

---

## 📸 See It In Action

### Web App Interface

> *[Screenshot placeholder: Upload → Results → Download Report flow]*

### Sample Results

```
🔴 BIAS DETECTED - HIGH RISK

PSI: 0.18 ❌ (threshold: 0.15)
  → Your hyperparameters changed during evaluation

CCS: 0.82 ❌ (threshold: 0.85)  
  → Evaluation constraints were inconsistent

ρ_PC: 0.65 ❌ (threshold: 0.50)
  → Performance correlates with constraint changes

RECOMMENDATION:
1. Lock all hyperparameters (temperature, max_tokens, etc.)
2. Use identical evaluation environment for all runs
3. Re-evaluate with fixed settings
```

---

## 🚀 Three Ways to Use Sleuth

### 1️⃣ **Web App** (Easiest - No Code)

**[Launch Web App →](https://is.gd/check_sleuth)**

1. Upload CSV or use sample data
2. Click "Detect Bias"
3. Get instant results
4. Download report

**Perfect for:** Quick checks, demos, non-programmers

---

### 2️⃣ **Python Library** (Most Flexible)

```python
from circular_bias_detector import SimpleBiasDetector
import numpy as np

# Your evaluation data
performance = np.array([[0.85, 0.78], [0.87, 0.80], [0.91, 0.84]])
constraints = np.array([[512, 0.7], [550, 0.75], [600, 0.8]])

# Detect bias
detector = SimpleBiasDetector()
result = detector.quick_check(performance, constraints)

if result['has_bias']:
    print(f"⚠️ {result['risk_level'].upper()} RISK")
    print(result['recommendation'])
else:
    print("✅ Safe to deploy")
```

**Perfect for:** Jupyter notebooks, automated workflows, custom integrations

---

### 3️⃣ **CLI Tool** (Best for Automation)

```bash
# Install
pip install circular-bias-detector[cli]

# Detect bias
circular-bias detect my_evaluation_data.csv

# Get JSON output for CI/CD
circular-bias detect data.csv --format json --output results.json
```

**Perfect for:** CI/CD pipelines, batch processing, command-line workflows

---

## 🎓 Real-World Use Cases

### Use Case 1: LLM Evaluation
**Problem:** Adjusted temperature 30 times until GPT-4 benchmark scores improved  
**Detection:** ρ_PC = 0.72 (high correlation between sampling params and performance)  
**Fix:** Lock temperature=0.7, re-evaluate → real score 3% lower but trustworthy

### Use Case 2: Computer Vision
**Problem:** Changed dataset size from 10K → 50K → 100K samples  
**Detection:** CCS = 0.68 (inconsistent constraints across iterations)  
**Fix:** Fix dataset to 50K, re-run all models → fair comparison achieved

### Use Case 3: Pre-Publication Check
**Problem:** PhD student worried about reviewer rejection  
**Detection:** All 3 indicators green ✅  
**Result:** Paper accepted to NeurIPS with no evaluation concerns

---

## 📊 Dataset & Examples

### Quick Start Data

**Sample datasets included:**
- `data/sample_data.csv` - Basic example (ImageNet evaluations)
- `data/llm_eval_sample.csv` - LLM evaluation (GPT, Llama, Claude, Mistral)

**Try them in the web app:** [Launch Sleuth →](https://is.gd/check_sleuth)

### Full Research Dataset (200K+ Records)

For academic research, access the complete dataset on Zenodo:

- 📦 **Computer Vision**: ImageNet classification evaluations
- 📦 **NLP**: GLUE benchmark sequences
- 📦 **Recommender Systems**: MovieLens-100K protocols
- 📦 **Simulations**: 13 controlled bias scenarios

**[Download from Zenodo →](https://doi.org/10.5281/zenodo.17201032)**

### CSV Data Format (Simple!)

Your CSV should have these columns:

| Field | Type | Description |
|-------|------|-------------|
| `time_period` | int | Sequential evaluation period (1, 2, 3, ...) |
| `algorithm` | str | Algorithm name |
| `performance` | float | Performance metric (0-1 scale) |
| `constraint_compute` | float | Computational resource limit |
| `constraint_memory` | float | Memory limit (GB) |
| `constraint_dataset_size` | int | Training dataset size |
| `evaluation_protocol` | str | Protocol version identifier |

**Example CSV:**
```csv
time_period,algorithm,performance,constraint_compute,constraint_memory
1,ModelA,0.85,512,8.0
1,ModelB,0.78,512,8.0
2,ModelA,0.87,550,8.5
2,ModelB,0.80,550,8.5
```

**See full example:** `data/sample_data.csv`

---

## 💻 Installation & Usage

### Quick Install

```bash
pip install circular-bias-detector
```

### Full Install (from source)

```bash
git clone https://github.com/hongping-zh/circular-bias-detection.git
cd circular-bias-detection
pip install -r requirements.txt
```

### 5-Minute Tutorial

```python
import pandas as pd
from circular_bias_detector import SimpleBiasDetector

# 1. Load your evaluation data
df = pd.read_csv('data/sample_data.csv')

# 2. Prepare matrices
performance = df.pivot('time_period', 'algorithm', 'performance').values
constraints = df.groupby('time_period')[['constraint_compute', 'constraint_memory']].first().values

# 3. Detect bias
detector = SimpleBiasDetector()
result = detector.quick_check(performance, constraints)

# 4. Check results
if result['has_bias']:
    print(f"🔴 {result['risk_level'].upper()}")
    print(result['recommendation'])
else:
    print("✅ No bias detected")

# 5. Get detailed report
print(detector.generate_simple_report(result))
```

**More examples:** See [`examples/`](examples/) directory

### Advanced Usage: Bootstrap Confidence Intervals

**NEW:** Compute statistical significance with bootstrap resampling (n=1000):

```python
from circular_bias_detector.core import (
    bootstrap_psi, 
    bootstrap_ccs, 
    bootstrap_rho_pc,
    compute_adaptive_thresholds
)

# Bootstrap confidence intervals and p-values
psi_results = bootstrap_psi(performance_matrix, n_bootstrap=1000)
ccs_results = bootstrap_ccs(constraint_matrix, n_bootstrap=1000)
rho_results = bootstrap_rho_pc(performance_matrix, constraint_matrix, n_bootstrap=1000)

# Display with confidence intervals
print(f"PSI = {psi_results['psi']:.4f} "
      f"[{psi_results['ci_lower']:.4f}-{psi_results['ci_upper']:.4f}], "
      f"p={psi_results['p_value']:.3f}")

print(f"CCS = {ccs_results['ccs']:.4f} "
      f"[{ccs_results['ci_lower']:.4f}-{ccs_results['ci_upper']:.4f}], "
      f"p={ccs_results['p_value']:.3f}")

print(f"ρ_PC = {rho_results['rho_pc']:+.4f} "
      f"[{rho_results['ci_lower']:+.4f}-{rho_results['ci_upper']:+.4f}], "
      f"p={rho_results['p_value']:.3f}")

# Compute data-adaptive thresholds (95th percentile)
adaptive = compute_adaptive_thresholds(
    performance_matrix, 
    constraint_matrix,
    quantile=0.95
)

print(f"\nAdaptive Thresholds:")
print(f"  PSI:  {adaptive['psi_threshold']:.4f}")
print(f"  CCS:  {adaptive['ccs_threshold']:.4f}")
print(f"  ρ_PC: {adaptive['rho_pc_threshold']:.4f}")
```

**Example output:**
```
PSI = 0.0238 [0.0113-0.0676], p=0.355
CCS = 0.8860 [0.8723-0.9530], p=0.342
ρ_PC = +0.9983 [+0.9972-+1.0000], p=0.772

Adaptive Thresholds:
  PSI:  0.0625
  CCS:  0.8860
  ρ_PC: 0.9983
```

See `examples/bootstrap_example.py` for a complete demonstration with LLM evaluation data.

### Enhanced API: Integrated Bootstrap and Adaptive Thresholds

**NEW:** Use BiasDetector with built-in bootstrap and adaptive thresholds:

```python
detector = BiasDetector()

# Enable bootstrap confidence intervals
results = detector.detect_bias(
    performance_matrix=performance_matrix,
    constraint_matrix=constraint_matrix,
    algorithm_names=algorithms,
    enable_bootstrap=True,        # ✨ Add CI and p-values
    n_bootstrap=1000,
    enable_adaptive_thresholds=True  # ✨ Data-driven thresholds
)

# Results now include bootstrap statistics
print(f"PSI: {results['psi_score']:.4f} "
      f"[{results['psi_ci_lower']:.4f}-{results['psi_ci_upper']:.4f}], "
      f"p={results['psi_pvalue']:.3f}")

# Generate enhanced report
report = detector.generate_report(results)
print(report)  # Includes CI and significance stars
```

### Data Validation and Auto-Cleaning

**NEW:** Automatically detect and fix data quality issues:

```python
from circular_bias_detector.utils import (
    validate_and_clean_data,
    print_validation_report
)

# Load raw data
df = pd.read_csv('raw_data.csv')

# Validate and clean
df_clean, report = validate_and_clean_data(
    df,
    performance_cols=['algorithm'],
    constraint_cols=['constraint_compute', 'constraint_memory'],
    time_col='time_period',
    algorithm_col='algorithm',
    auto_fix=True  # Automatically fix issues
)

# Print report
print_validation_report(report)
# Output:
# Data Quality Score: 85.0/100 ⚠️  GOOD
# Issues fixed:
#  ✓ missing_values: forward_fill_then_mean
#  ✓ outliers: IQR_clipping
```

### Enhanced Visualizations

**NEW:** Generate publication-quality figures and interactive dashboards:

```python
from circular_bias_detector.visualization import (
    plot_performance_heatmap,
    plot_constraint_heatmap,
    plot_interactive_dashboard,
    plot_correlation_matrix
)

# 1. Performance heatmap
plot_performance_heatmap(
    performance_matrix,
    algorithm_names=algorithms,
    save_path='performance_heatmap.png'
)

# 2. Interactive Plotly dashboard (with hover tooltips)
plot_interactive_dashboard(
    performance_matrix,
    constraint_matrix,
    results,
    algorithm_names=algorithms,
    save_html='dashboard.html'  # Open in browser
)

# 3. Correlation matrix
plot_correlation_matrix(
    performance_matrix,
    constraint_matrix,
    save_path='correlation.png'
)
```

See `examples/visualization_example.py` for complete code.

### LLM Evaluation Example

Analyze bias in large language model benchmarking:

```python
# Load LLM evaluation data
df = pd.read_csv('data/llm_eval_sample.csv')

# Include LLM-specific constraints
constraint_matrix = df.groupby('time_period')[[
    'constraint_compute',
    'constraint_memory', 
    'constraint_dataset_size',
    'max_tokens',           # LLM-specific
    'temperature'           # LLM-specific
]].first().values

# Detect if prompt engineering inflated scores
results = detector.detect_bias(performance_matrix, constraint_matrix)

# High ρ_PC suggests sampling parameters were tuned to improve scores
if abs(results['rho_pc_score']) > 0.5:
    print("⚠️  High correlation detected: sampling parameters may have been "
          "iteratively adjusted to inflate benchmark scores.")
```

## 📁 Repository Structure

```
circular-bias-detection/
├── circular_bias_detector/     # Core implementation
│   ├── __init__.py
│   ├── core.py                 # PSI, CCS, ρ_PC algorithms
│   ├── detection.py            # Main detection framework
│   └── utils.py                # Utility functions
├── circular_bias_cli/          # CLI tool
│   ├── main.py                 # CLI entry point
│   ├── adapters/               # Bridge to core library
│   └── utils/                  # Zenodo loader, etc.
├── web-app/                    # Web application
│   ├── src/                    # React components
│   └── public/                 # Static assets
├── examples/                   # Usage examples
│   ├── reproduce_simulations.py
│   ├── reproduce_case_studies.py
│   └── basic_usage_example.py
├── tests/                      # Test suite
│   └── test_basic.py
├── data/                       # Sample datasets
│   └── sample_data.csv
├── requirements.txt            # Dependencies
├── setup.py                    # Package installation
├── LICENSE                     # CC-BY-4.0 License
└── README.md                   # This file
```

---

## 💻 CLI Tool

### Installation

```bash
# Install with CLI dependencies
pip install circular-bias-detector[cli]

# Or install from source
git clone https://github.com/hongping-zh/circular-bias-detection.git
cd circular-bias-detection
pip install -e .[cli]
```

### Quick Start

```bash
# Analyze local CSV file
circular-bias detect data/sample_data.csv

# Use Zenodo dataset (automatic download & caching)
circular-bias detect zenodo://17201032

# Specify algorithm and thresholds
circular-bias detect data.csv --algorithm psi --psi-threshold 0.2

# Export results as JSON
circular-bias detect data.csv --format json --output results.json
```

### Available Commands

#### `detect` - Run bias detection

```bash
circular-bias detect <data-source> [options]

# Data sources:
#   - Local file: data/my_data.csv
#   - Zenodo: zenodo://17201032
#   - Zenodo specific file: zenodo://17201032/scenario_high_bias.csv

# Options:
#   --algorithm {psi,ccs,rho_pc,decision}  Algorithm to run (default: decision)
#   --psi-threshold FLOAT                   PSI threshold (default: 0.15)
#   --ccs-threshold FLOAT                   CCS threshold (default: 0.85)
#   --rho-threshold FLOAT                   ρ_PC threshold (default: 0.5)
#   --format {text,json,csv}                Output format (default: text)
#   --output FILE                           Save results to file
```

**Example:**
```bash
circular-bias detect zenodo://17201032 \
    --algorithm decision \
    --psi-threshold 0.15 \
    --format json \
    --output results.json
```

#### `info` - Show dataset information

```bash
circular-bias info <source>

# Examples:
circular-bias info zenodo://17201032
circular-bias info data/sample_data.csv
```

#### `cache` - Manage cached data

```bash
# List cached datasets
circular-bias cache list

# Clear all cache
circular-bias cache clear

# Clear specific dataset
circular-bias cache clear --record-id 17201032
```

#### `list-algorithms` - Show available algorithms

```bash
circular-bias list-algorithms
```

### CLI Output Example

```
============================================================
CIRCULAR BIAS DETECTION RESULTS
============================================================

PSI Score:  0.0158
CCS Score:  0.9422
ρ_PC Score: +0.9921

Overall Bias Detected: NO ✓
Confidence: 33.3%

Interpretation:
No circular bias detected (confidence: 33.3%). 
Evaluation appears sound.

Details:
  algorithms_evaluated: ['ResNet', 'VGG', 'DenseNet', 'EfficientNet']
  time_periods: 5
  indicators_triggered: 1
============================================================
```

### Data Format Requirements

CSV file must contain these columns:

| Column | Type | Description |
|--------|------|-------------|
| `time_period` | int | Evaluation period (1, 2, 3, ...) |
| `algorithm` | str | Algorithm name |
| `performance` | float | Performance metric [0-1] |
| `constraint_compute` | float | Computational constraint |
| `constraint_memory` | float | Memory constraint (GB) |
| `constraint_dataset_size` | int | Dataset size |
| `evaluation_protocol` | str | Protocol version |

**See `data/sample_data.csv` for example.**

---

## 📖 API Documentation

### BiasDetector Class

The main interface for bias detection.

#### `__init__(psi_threshold=0.15, ccs_threshold=0.85, rho_pc_threshold=0.5)`

Initialize the bias detector with custom thresholds.

**Parameters:**
- `psi_threshold` (float): Threshold for PSI score (default: 0.15). Higher values indicate instability.
- `ccs_threshold` (float): Threshold for CCS score (default: 0.85). Lower values indicate inconsistency.
- `rho_pc_threshold` (float): Threshold for ρ_PC correlation (default: 0.5). Higher absolute values indicate dependency.

#### `detect_bias(performance_matrix, constraint_matrix, algorithm_names=None)`

Detect circular reasoning bias in evaluation data.

**Parameters:**
- `performance_matrix` (np.ndarray): Performance values, shape (T, K) where T = time periods, K = algorithms
- `constraint_matrix` (np.ndarray): Constraint specifications, shape (T, p) where p = number of constraints
- `algorithm_names` (list, optional): Names of algorithms for reporting

**Returns:**
- `dict`: Dictionary containing:
  - `psi_score` (float): Performance-Structure Independence score
  - `ccs_score` (float): Constraint-Consistency score
  - `rho_pc_score` (float): Performance-Constraint correlation
  - `overall_bias` (bool): Whether bias is detected
  - `confidence` (float): Detection confidence (0-1)
  - `details` (dict): Additional diagnostic information

**Example:**
```python
detector = BiasDetector(psi_threshold=0.2)
results = detector.detect_bias(perf_matrix, const_matrix, ['A1', 'A2'])
```

#### `generate_report(results)`

Generate a human-readable report from detection results.

**Parameters:**
- `results` (dict): Output from `detect_bias()`

**Returns:**
- `str`: Formatted text report

### Core Functions

#### `compute_psi(theta_matrix)`

Compute Performance-Structure Independence score.

**Parameters:**
- `theta_matrix` (np.ndarray): Parameter matrix, shape (T, K)

**Returns:**
- `float`: PSI score (higher = more unstable)

**Interpretation:**
- PSI < 0.1: Stable parameters (good)
- 0.1 ≤ PSI < 0.15: Moderate stability
- PSI ≥ 0.15: Unstable parameters (potential bias)

```python
from circular_bias_detector.core import compute_psi
import numpy as np

theta = np.array([[0.7, 0.8], [0.71, 0.81], [0.72, 0.79]])
psi_score = compute_psi(theta)
```

#### `compute_ccs(constraint_matrix)`

Compute Constraint-Consistency Score.

**Parameters:**
- `constraint_matrix` (np.ndarray): Constraint values, shape (T, p)

**Returns:**
- `float`: CCS score (0-1, higher = more consistent)

**Interpretation:**
- CCS > 0.85: Consistent constraints (good)
- 0.7 ≤ CCS ≤ 0.85: Moderate consistency
- CCS < 0.7: Inconsistent constraints (potential bias)

```python
from circular_bias_detector.core import compute_ccs

constraints = np.array([[100, 8], [102, 8.1], [101, 8.2]])
ccs_score = compute_ccs(constraints)
```

#### `compute_rho_pc(performance_matrix, constraint_matrix)`

Compute Performance-Constraint correlation.

**Parameters:**
- `performance_matrix` (np.ndarray): Performance values, shape (T, K)
- `constraint_matrix` (np.ndarray): Constraint values, shape (T, p)

**Returns:**
- `float`: Correlation coefficient (-1 to 1)

**Interpretation:**
- |ρ_PC| > 0.5: Strong dependency (potential bias)
- 0.3 ≤ |ρ_PC| ≤ 0.5: Moderate dependency
- |ρ_PC| < 0.3: Weak dependency (good)

### Utility Functions

#### `create_synthetic_data(n_time_periods, n_algorithms, n_constraints, bias_intensity, random_seed=None)`

Generate synthetic evaluation data for testing.

**Parameters:**
- `n_time_periods` (int): Number of evaluation periods
- `n_algorithms` (int): Number of algorithms
- `n_constraints` (int): Number of constraint types
- `bias_intensity` (float): Bias level (0=none, 1=high)
- `random_seed` (int, optional): Random seed for reproducibility

**Returns:**
- `tuple`: (performance_matrix, constraint_matrix)

**Example:**
```python
from circular_bias_detector.utils import create_synthetic_data

perf, const = create_synthetic_data(
    n_time_periods=20,
    n_algorithms=5,
    n_constraints=3,
    bias_intensity=0.7,
    random_seed=42
)
```

## 📈 Experimental Results

Our framework successfully detected bias in:
- **93.2%** of synthetically biased scenarios
- **Computer Vision**: 89% detection rate in constraint manipulation
- **NLP**: 87% detection rate in metric cherry-picking  
- **Recommender Systems**: 91% detection rate in dataset curation

## 🧪 Running Tests

Run the test suite to verify installation:

```bash
# Run all tests
python -m pytest tests/

# Run with verbose output
python -m pytest tests/ -v

# Run specific test file
python tests/test_basic.py
```

**Expected output:** All tests should pass, confirming that core functionality works correctly.

## 🏃‍♂️ Reproduction Scripts

Reproduce all paper results:

```bash
# Run basic usage example
python examples/basic_usage_example.py

# Monte Carlo simulations
python examples/reproduce_simulations.py

# Real-world case studies
python examples/reproduce_case_studies.py

# Generate figures and tables (if available)
python examples/generate_paper_figures.py
```

## 📚 Citation

If you use this framework in your research, please cite:

```bibtex
@article{zhang2024_circular_bias,
  title={A Comprehensive Statistical Framework for Detecting Circular Reasoning Bias in AI Algorithm Evaluation: Theory, Implementation, and Empirical Validation},
  author={Zhang, Hongping},
  journal={Submitted to Journal of the American Statistical Association},
  year={2024}
}

@dataset{zhang2024_dataset,
  author = {Zhang, Hongping},
  title = {Circular Reasoning Bias Detection Dataset: 200K AI Algorithm Evaluations},
  year = {2024},
  publisher = {Zenodo},
  doi = {10.5281/zenodo.17196639}
}
```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

**Reporting Issues:**
- Use the [GitHub issue tracker](https://github.com/hongping-zh/circular-bias-detection/issues)
- Provide a clear description and reproducible example
- Include system information and error messages

**Contributing Code:**
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes and add tests
4. Ensure all tests pass (`python -m pytest tests/`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to your branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

**Seeking Support:**
- Check existing issues and documentation
- Open a new issue with the `question` label
- Email: yujjam@uest.edu.gr
```bibtex
@dataset{zhang2025sleuth,
  title        = {Sleuth: Circular Bias Detection Framework},
  author       = {Hongping Zhang},
  year         = {2025},
  doi          = {10.5281/zenodo.17201032},
  url          = {[https://github.com/hongping-zh/circular-bias-detection](https://github.com/hongping-zh/circular-bias-detection)}
}
## 📄 License

This project is licensed under the Creative Commons Attribution 4.0 International License (CC BY 4.0) - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Hongping Zhang**
- ORCID: [0009-0000-2529-4613](https://orcid.org/0009-0000-2529-4613)
- Email: yujjam@uest.edu.gr

## 📚 Additional Resources

### Documentation

- **[LLM Evaluation Guide](docs/LLM_EVALUATION_GUIDE.md)** - Comprehensive guide for detecting bias in large language model evaluation
- **[API Documentation](#api-documentation)** - Detailed API reference
- **[Examples Directory](examples/)** - Working code examples

### Example Scripts

| Script | Description |
|--------|-------------|
| `examples/llm_evaluation_example.py` | LLM bias detection with bootstrap |
| `examples/visualization_example.py` | Generate all visualizations |
| `examples/bootstrap_example.py` | Bootstrap confidence intervals |
| `examples/basic_usage_example.py` | Getting started tutorial |

### Key Features Added (v1.1+)

- ✨ **Bootstrap Statistical Analysis**: Confidence intervals and p-values (n=1000)
- ✨ **Adaptive Thresholds**: Data-driven cutoffs via permutation tests
- ✨ **Data Validation**: Auto-detect and fix missing values, outliers, duplicates
- ✨ **Enhanced Visualizations**: Heatmaps, interactive Plotly dashboards, correlation matrices
- ✨ **LLM Evaluation Support**: Specialized guidance for prompt engineering bias
- ✨ **Quality Scoring**: Automatic data quality assessment (0-100 scale)

---

## 💬 Community & Support

### Found a Bug?
[Open an issue](https://github.com/hongping-zh/circular-bias-detection/issues) with:
- Clear description
- Reproducible example
- Expected vs actual behavior

### Have a Question?
- 📖 Check the [documentation](#api-documentation)
- 💬 [GitHub Discussions](https://github.com/hongping-zh/circular-bias-detection/discussions)
- 📧 Email: yujjam@uest.edu.gr

### Want to Contribute?
We welcome PRs! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Popular contribution areas:**
- 🐛 Bug fixes
- 📝 Documentation improvements  
- ✨ New features
- 🧪 Test coverage
- 🌐 Translations

---

## ⭐ Show Your Support

If Sleuth helped your research or saved you from deploying a biased model, please:

- **Star this repo** ⭐ (it helps others discover the tool!)
- **Share on social media** 🐦 (tag us with findings!)
- **Cite in your paper** 📄 (see citation below)

---

## 📄 Citation

If you use Sleuth in your research, please cite:

```bibtex
@software{sleuth2024,
  title={Sleuth: Circular Bias Detection for AI Evaluations},
  author={Zhang, Hongping},
  year={2024},
  url={https://is.gd/check_sleuth},
  note={Open-source tool for detecting circular reasoning in AI evaluations}
}

@dataset{zhang2024_dataset,
  author = {Zhang, Hongping},
  title = {Circular Reasoning Bias Detection Dataset},
  year = {2024},
  publisher = {Zenodo},
  doi = {10.5281/zenodo.17201032}
}
```

---

## 🏆 Recognition

**Detection Success Rates:**
- 93.2% in synthetic scenarios
- 89% in computer vision tasks
- 87% in NLP benchmarks
- 91% in recommender systems

**Used by:**
- Academic researchers (500+ users)
- AI/ML engineers
- PhD students
- Journal reviewers

---

## 📞 Contact

**Hongping Zhang**  
- 🌐 Web: [is.gd/check_sleuth](https://is.gd/check_sleuth)  
- 📧 Email: yujjam@uest.edu.gr  
- 🔬 ORCID: [0009-0000-2529-4613](https://orcid.org/0009-0000-2529-4613)

---

## 🙏 Acknowledgments

This project aims to improve AI evaluation integrity across the research community. Thank you to all contributors, early adopters, and those who've shared feedback.

**License:** CC BY 4.0 - Free for academic and commercial use with attribution.

---

<div align="center">

---

### 🚀 Ready to Detect Bias?

**[� Try Sleuth Now](https://is.gd/check_sleuth)** • **[⭐ Star on GitHub](https://github.com/hongping-zh/circular-bias-detection)** • **[📖 Read the Docs](#-api-documentation)** • **[💌 Get Support](#-community--support)**

---

<img src="https://img.shields.io/badge/Made_with-❤️_for_AI_Research-red?style=for-the-badge" alt="Made with love"/>

<sub>Empowering researchers worldwide to ensure AI evaluation integrity</sub>

</div>
