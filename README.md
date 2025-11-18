# Sleuth - AI Bias Detector

> **Brand Note**: **Sleuth** is the product name. The technical identifier `circular-bias-detection` (GitHub/PyPI) refers to the methodology we implement.

[![Web App](https://img.shields.io/badge/%F0%9F%94%8D_Try_Sleuth-brightgreen?style=for-the-badge)](https://is.gd/check_sleuth)
[![GitHub stars](https://img.shields.io/github/stars/hongping-zh/circular-bias-detection?style=social)](https://github.com/hongping-zh/circular-bias-detection)
[![CI](https://github.com/hongping-zh/circular-bias-detection/actions/workflows/ci.yml/badge.svg)](https://github.com/hongping-zh/circular-bias-detection/actions/workflows/ci.yml)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PyPI version](https://img.shields.io/badge/pypi-v1.0.0-blue)](https://pypi.org/project/circular-bias-detector/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![License: CC BY 4.0](https://img.shields.io/badge/Docs-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Software DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17201032.svg)](https://doi.org/10.5281/zenodo.17201032)
[![Dataset DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17196639.svg)](https://doi.org/10.5281/zenodo.17196639)

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

Required columns:

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

- **Report bugs**: [GitHub Issues](https://github.com/hongping-zh/circular-bias-detection/issues)  
- **Ask questions**: [Discussions](https://github.com/hongping-zh/circular-bias-detection/discussions) or email `yujjam@uest.edu.gr`  
- **Contribute**: Fork → Branch → Test → PR (see `CONTRIBUTING.md`)

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