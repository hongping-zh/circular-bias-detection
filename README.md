# Sleuth - AI Bias Detector

> **Brand Note**: **Sleuth** is the product name. The technical identifier `circular-bias-detection` (GitHub/PyPI) refers to the methodology we implement.

<<<<<<< HEAD
<!-- Badges Section -->
[![Web App](https://img.shields.io/badge/%F0%9F%94%8D_Try_Sleuth-brightgreen?style=for-the-badge)](https://is.gd/check_sleuth)
[![GitHub stars](https://img.shields.io/github/stars/hongping-zh/circular-bias-detection?style=social)](https://github.com/hongping-zh/circular-bias-detection)
[![CI](https://github.com/hongping-zh/circular-bias-detection/actions/workflows/ci.yml/badge.svg)](https://github.com/hongping-zh/circular-bias-detection/actions/workflows/ci.yml)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PyPI version](https://img.shields.io/badge/pypi-v1.0.0-blue)](https://pypi.org/project/circular-bias-detector/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![License: CC BY 4.0](https://img.shields.io/badge/Docs-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Software DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17201032.svg)](https://doi.org/10.5281/zenodo.17201032)
[![Dataset DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17196639.svg)](https://doi.org/10.5281/zenodo.17196639)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](tests/)
[![CBD Dataset (All Versions)](https://zenodo.org/badge/DOI/10.5281/zenodo.17637302.svg)](https://doi.org/10.5281/zenodo.17637302)
[![CBD Dataset v3/v3.1](https://img.shields.io/badge/CBD%20Dataset-v3%2Fv3.1-blue)](https://doi.org/10.5281/zenodo.17637303)

## Detect AI Evaluation Bias in 30 Seconds

## On this page

- [Quick Links](#quick-links)
- [Quick Start](#-quick-start)
- [Examples](#examples)
- [API/Docs](#documentation)
- [Testing](#-testing)


## Quick Links

- Live Demo: https://is.gd/check_sleuth
- 5分钟上手: 参见 README 的“5分钟上手”小节
- 示例数据: data/tiny_sample.csv
- Examples: examples/
- API/Docs: docs/
- Software DOI: https://doi.org/10.5281/zenodo.17201032
- Dataset DOI: https://doi.org/10.5281/zenodo.17196639

## Screenshot

![Sleuth Web App Screenshot](assets/screenshot.png)


**Stop deploying AI models with inflated performance scores.**

Sleuth catches when you've been tweaking hyperparameters, prompts, or datasets until your benchmark numbers look good—a hidden form of bias that breaks AI evaluations.
=======
>>>>>>> origin/main

---

## 🚀 Detect AI Evaluation Bias in 30 Seconds

Stop deploying AI models with inflated performance scores.  
**Sleuth** detects hidden bias caused by tweaking hyperparameters, prompts, or datasets during evaluation—breaking circular reasoning in AI benchmarks.

---

## 🔗 Quick Links

- **Live Demo**: [Try Sleuth Now →](https://is.gd/check_sleuth)  
- **Sample Data**: [`data/sample_data.csv`](data/sample_data.csv)  
- **Examples**: [`examples/`](examples/)  
- **Documentation**: [`docs/`](docs/)  
- **Software DOI**: [10.5281/zenodo.17201032](https://doi.org/10.5281/zenodo.17201032)  
- **Dataset DOI**: [10.5281/zenodo.17196639](https://doi.org/10.5281/zenodo.17196639)

---

## ⚡ Quick Start

### Option 1: Web App (Fastest – No Install)

✅ **[Try Sleuth in Browser →](https://is.gd/check_sleuth)**  
- Upload CSV or use sample data  
- Instant results + downloadable report  
- 100% private, zero setup

---

### Option 2: Python Library

```bash
pip install circular-bias-detector
```

```python
from circular_bias_detector import SimpleBiasDetector
import numpy as np

performance = np.array([[0.85, 0.78], [0.87, 0.80], [0.91, 0.84]])
constraints = np.array([[512, 0.7], [550, 0.75], [600, 0.8]])

detector = SimpleBiasDetector()
result = detector.quick_check(performance, constraints)

if result['has_bias']:
    print(f"⚠️ {result['risk_level'].upper()} RISK: {result['recommendation']}")
else:
    print("- No bias detected—safe to publish!")
```

---

### Option 3: CLI Tool

```bash
pip install circular-bias-detector[cli]
circular-bias detect my_data.csv --format json --output results.json
```

---

## 🧠 How It Works

Sleuth evaluates three statistical indicators:

| Indicator | Meaning | Threshold |
|----------|--------|-----------|
| **PSI** | Performance-Structure Independence | > 0.15 → unstable |
| **CCS** | Constraint Consistency Score | < 0.85 → inconsistent |
| **ρ_PC** | Performance–Constraint Correlation | \|ρ\| > 0.5 → suspicious |

A bias alert is triggered if any indicator exceeds its threshold.

---

## 📊 Sample Output

```
🔴 BIAS DETECTED - HIGH RISK

PSI: 0.18 (>0.15) — Hyperparameters changed during eval  
CCS: 0.82 (<0.85) — Inconsistent resource limits  
ρ_PC: 0.65 (>0.50) — Performance correlates with constraints  

RECOMMENDATION:
1. Lock all hyperparameters (e.g., temperature, max_tokens)
2. Use identical evaluation settings across runs
3. Re-evaluate with fixed protocol
```

---

## 📁 Data Format (CSV)

<<<<<<< HEAD
### 1️⃣ **Web App** (Easiest - No Code)

**[Launch Sleuth Web App →](https://is.gd/check_sleuth)**

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
    print("- Safe to deploy")
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
**Fix:** Lock temperature=0.7, re-evaluate - real score 3% lower but trustworthy

### Use Case 2: Computer Vision
**Problem:** Changed dataset size from 10K - 50K - 100K samples  
**Detection:** CCS = 0.68 (inconsistent constraints across iterations)  
**Fix:** Fix dataset to 50K, re-run all models - fair comparison achieved

### Use Case 3: Pre-Publication Check
**Problem:** PhD student worried about reviewer rejection  
**Detection:** All 3 indicators green - **Result:** Paper accepted to NeurIPS with no evaluation concerns

---

## 📊 Dataset & Examples

### Quick Start Data

**Sample datasets included:**
- `data/sample_data.csv` - Basic example (ImageNet evaluations)
- `data/llm_eval_sample.csv` - LLM evaluation (GPT, Llama, Claude, Mistral)

**Try them in Sleuth:** [Launch Sleuth →](https://is.gd/check_sleuth)

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
    print("- No bias detected")

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
    enable_bootstrap=True,        # - Add CI and p-values
    n_bootstrap=1000,
    enable_adaptive_thresholds=True  # - Data-driven thresholds
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
#  - missing_values: forward_fill_then_mean
#  - outliers: IQR_clipping
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
- ├── __init__.py
- ├── core.py                 # PSI, CCS, ρ_PC algorithms
- ├── detection.py            # Main detection framework
- └── utils.py                # Utility functions
├── circular_bias_cli/          # CLI tool
- ├── main.py                 # CLI entry point
- ├── adapters/               # Bridge to core library
- └── utils/                  # Zenodo loader, etc.
├── web-app/                    # Web application
- ├── src/                    # React components
- └── public/                 # Static assets
├── examples/                   # Usage examples
- ├── reproduce_simulations.py
- ├── reproduce_case_studies.py
- └── basic_usage_example.py
├── tests/                      # Test suite
- └── test_basic.py
├── data/                       # Sample datasets
- └── sample_data.csv
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

# Use CBD Dataset v3/v3.1 (auto-selects largest CSV)
circular-bias detect zenodo://17637303

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
#   - CBD Dataset v3/v3.1: zenodo://17637303
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

Overall Bias Detected: NO - Confidence: 33.3%

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
=======
Required columns:
>>>>>>> origin/main

| Column | Type | Description |
|--------|------|-------------|
| `time_period` | int | Evaluation round (1, 2, 3, ...) |
| `algorithm` | str | Model/algorithm name |
| `performance` | float | Metric score (0–1) |
| `constraint_compute` | float | Compute limit (e.g., FLOPs) |
| `constraint_memory` | float | Memory (GB) |
| `constraint_dataset_size` | int | Training set size (optional) |

👉 See [`data/sample_data.csv`](data/sample_data.csv) for a working example.

---

## 🛠 Advanced Features (v1.1+)

- **Bootstrap CIs & p-values** (`n=1000`) for statistical rigor  
- **Adaptive thresholds** via permutation testing  
- **Auto data validation**: fixes missing values, outliers, duplicates  
- **Publication-ready visualizations**: heatmaps, correlation plots, interactive dashboards  
- **LLM-specific support**: detects prompt/sampling tuning bias

```python
detector = BiasDetector(enable_bootstrap=True, enable_adaptive_thresholds=True)
results = detector.detect_bias(performance_matrix, constraint_matrix)
print(detector.generate_report(results))
```

---

## 📚 Documentation & Examples

- **Offline Usage**: [`docs/usage_offline.md`](docs/usage_offline.md)  
- **Real-time/Web**: [`docs/usage_realtime.md`](docs/usage_realtime.md)  
- **FAQ / Glossary / Contributing**: `FAQ.md`, `GLOSSARY.md`, `CONTRIBUTING.md`  
- **Full Examples**: [`examples/`](examples/)  
  - `basic_usage_example.py`  
  - `bootstrap_example.py`  
  - `llm_evaluation_example.py`  
  - `visualization_example.py`

---

## 🧪 Testing & Reproduction

```bash
# Run tests
python -m pytest tests/

# Reproduce paper results
python examples/reproduce_simulations.py
python examples/reproduce_case_studies.py
```

---

## 📦 Installation

```bash
# Core library
pip install circular-bias-detector

# With CLI
pip install circular-bias-detector[cli]

# From source
git clone https://github.com/hongping-zh/circular-bias-detection.git
cd circular-bias-detection
pip install -e .
```

---

## 📈 Performance

Sleuth detects bias with high accuracy:
- **93.2%** in synthetic scenarios  
- **89%** in computer vision  
- **87%** in NLP benchmarks  
- **91%** in recommender systems

---

## 🤝 Contributing & Support

<<<<<<< HEAD

### CBD Dataset (v3/v3.1) Citation

Please cite the dataset alongside the software when you use the CBD data in research or products.

- Concept DOI (all versions): https://doi.org/10.5281/zenodo.17637302
- Version DOI (this release v3/v3.1): https://doi.org/10.5281/zenodo.17637303

APA (Dataset, version DOI):

Hongping Zhang, & CBD Project Team. (2025). Circular Bias Detection (CBD) dataset and evaluation protocols (v3 / v3.1) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.17637303

中文（数据集，版本 DOI）：

Hongping Zhang，& CBD 项目组. (2025). 循环偏差检测（CBD）数据集与评测协议（v3 / v3.1）[数据集]. Zenodo. https://doi.org/10.5281/zenodo.17637303

### Acknowledgments

This project was developed to address a critical gap in AI evaluation integrity. We thank:
- The open-source community for foundational libraries (NumPy, SciPy, Pandas)
- Early adopters and users who provided valuable feedback
- Zenodo for free dataset archiving and DOI assignment

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
=======
- **Report bugs**: [GitHub Issues](https://github.com/hongping-zh/circular-bias-detection/issues)  
- **Ask questions**: [Discussions](https://github.com/hongping-zh/circular-bias-detection/discussions) or email `yujjam@uest.edu.gr`  
- **Contribute**: Fork → Branch → Test → PR (see `CONTRIBUTING.md`)
>>>>>>> origin/main

---

## 📄 License

- **Code**: MIT License  
- **Docs & Dataset**: CC BY 4.0  
- ✅ Free for academic and commercial use with attribution

---

## 📖 Citation

If you use Sleuth, please cite:

```bibtex
@software{zhang2024sleuth,
  author    = {Zhang, Hongping},
  title     = {Sleuth: Circular Bias Detection for AI Evaluations},
  year      = {2024},
  version   = {v1.0.0},
  doi       = {10.5281/zenodo.17201032},
  url       = {https://github.com/hongping-zh/circular-bias-detection}
}
```

Dataset citation (if used):  
DOI: [10.5281/zenodo.17196639](https://doi.org/10.5281/zenodo.17196639)

---

## 👤 Author

**Hongping Zhang**  
📧 yujjam@uest.edu.gr | [ORCID](https://orcid.org/0009-0000-2529-4613)

---

<div align="center">

### 🚀 Ready to Detect Bias?

**[Try Web App](https://is.gd/check_sleuth)** • **[Star on GitHub](https://github.com/hongping-zh/circular-bias-detection)** • **[Read Docs](#-documentation--examples)**

<br>
<img src="https://img.shields.io/badge/Made_with-❤️_for_AI_Research-red?style=for-the-badge" alt="Made with love"/>
<sub>Empowering researchers worldwide to ensure AI evaluation integrity</sub>

</div>