# Circular Reasoning Bias Detection Framework

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17196639.svg)](https://doi.org/10.5281/zenodo.17196639)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive statistical framework for detecting circular reasoning bias in AI algorithm evaluation. This repository provides the implementation of the methodology described in:

**"A Comprehensive Statistical Framework for Detecting Circular Reasoning Bias in AI Algorithm Evaluation: Theory, Implementation, and Empirical Validation"**

## 🎯 Overview

Circular reasoning bias occurs when evaluation protocols are iteratively modified based on preliminary performance observations, leading to inflated performance estimates and unreliable conclusions. Our framework introduces three novel indicators:

- **PSI** (Performance-Structure Independence): Detects parameter instability
- **CCS** (Constraint-Consistency Score): Measures constraint specification consistency  
- **ρ_PC** (Performance-Constraint Correlation): Quantifies performance-constraint dependencies

## 📊 Dataset

The accompanying dataset contains 2,000+ AI algorithm evaluation records across multiple domains:
- **Computer Vision**: ImageNet classification evaluations
- **NLP**: GLUE benchmark sequences
- **Recommender Systems**: MovieLens-100K protocols
- **Monte Carlo Simulations**: 13 controlled bias scenarios

**Access**: [Zenodo Dataset](https://doi.org/10.5281/zenodo.17196639)

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/hongping-zh/circular-bias-detection.git
cd circular-bias-detection
pip install -r requirements.txt
```

### Basic Usage

```python
from circular_bias_detector import BiasDetector

# Load your evaluation data
detector = BiasDetector()
results = detector.detect_bias(
    performance_matrix=P,
    constraint_matrix=C,
    algorithms=['A1', 'A2', 'A3']
)

print(f"PSI Score: {results['psi_score']:.4f}")
print(f"CCS Score: {results['ccs_score']:.4f}")
print(f"ρ_PC Correlation: {results['rho_pc']:.4f}")
print(f"Bias Detected: {results['bias_detected']}")
```

## 📁 Repository Structure

```
circular-bias-detection/
├── circular_bias_detector/     # Core implementation
│   ├── __init__.py
│   ├── core.py                 # PSI, CCS, ρ_PC algorithms
│   ├── detection.py            # Main detection framework
│   └── utils.py               # Utility functions
├── examples/                   # Usage examples
│   ├── reproduce_simulations.py
│   ├── reproduce_case_studies.py
│   └── basic_usage_example.py
├── tests/                      # Test suite
│   └── test_basic.py
├── data/                       # Sample datasets
│   └── sample_data.csv
├── requirements.txt            # Dependencies
├── LICENSE                     # MIT License
└── README.md                   # This file
```

## 🔬 Core Algorithms

### Performance-Structure Independence (PSI)
Measures parameter stability across evaluation periods:

```python
def compute_psi(theta_matrix):
    """
    Compute PSI score for parameter stability detection
    """
    T, K = theta_matrix.shape
    psi_scores = []
    
    for k in range(K):
        differences = np.diff(theta_matrix[:, k])
        psi_k = np.mean(np.abs(differences))
        psi_scores.append(psi_k)
    
    return np.mean(psi_scores)
```

### Constraint-Consistency Score (CCS)
Evaluates consistency in constraint specifications:

```python
def compute_ccs(constraint_matrix):
    """
    Compute CCS score for constraint consistency
    """
    T, p = constraint_matrix.shape
    consistency_scores = []
    
    for j in range(p):
        constraint_series = constraint_matrix[:, j]
        cv = np.std(constraint_series) / np.mean(constraint_series)
        consistency_scores.append(1 / (1 + cv))
    
    return np.mean(consistency_scores)
```

## 📈 Experimental Results

Our framework successfully detected bias in:
- **93.2%** of synthetically biased scenarios
- **Computer Vision**: 89% detection rate in constraint manipulation
- **NLP**: 87% detection rate in metric cherry-picking  
- **Recommender Systems**: 91% detection rate in dataset curation

## 🏃‍♂️ Reproduction Scripts

Reproduce all paper results:

```bash
# Monte Carlo simulations
python examples/reproduce_simulations.py

# Real-world case studies
python examples/reproduce_case_studies.py

# Generate figures and tables
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

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Hongping Zhang**
- ORCID: [0009-0000-2529-4613](https://orcid.org/0009-0000-2529-4613)
- Email: yujjam@uest.edu.gr

## 🙏 Acknowledgments

This work contributes to the broader effort of ensuring reliable and unbiased AI evaluation methodologies. We thank the research community for valuable feedback and discussions.
