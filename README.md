# Circular Reasoning Bias Detection Framework

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17201032.svg)](https://doi.org/10.5281/zenodo.17201032)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

A comprehensive statistical framework for detecting circular reasoning bias in AI algorithm evaluation. This repository provides the implementation of the methodology described in:

**"A Comprehensive Statistical Framework for Detecting Circular Reasoning Bias in AI Algorithm Evaluation: Theory, Implementation, and Empirical Validation"**

## 🎯 Overview

Circular reasoning bias occurs when evaluation protocols are iteratively modified based on preliminary performance observations, leading to inflated performance estimates and unreliable conclusions. Our framework introduces three novel indicators:

- **PSI** (Performance-Structure Independence): Detects parameter instability
- **CCS** (Constraint-Consistency Score): Measures constraint specification consistency  
- **ρ_PC** (Performance-Constraint Correlation): Quantifies performance-constraint dependencies

### Why This Framework?

Unlike existing bias detection tools that focus on **model outputs** (e.g., fairness metrics in predictions), our framework audits the **evaluation process itself**—detecting when the rules of the game are being changed mid-evaluation to favor certain algorithms.

| Framework | Focus | Circular Bias Detection | Target Users |
|-----------|-------|-------------------------|--------------|
| [AIF360](https://github.com/Trusted-AI/AIF360) | Model fairness (demographic parity, equalized odds) | ❌ | ML practitioners |
| [Fairlearn](https://github.com/fairlearn/fairlearn) | Algorithmic fairness constraints | ❌ | Data scientists |
| [Themis-ML](https://github.com/cosmicBboy/themis-ml) | Discrimination testing | ❌ | Researchers |
| **This Framework** | **Evaluation protocol integrity** | ✅ | **Researchers, Reviewers, Auditors** |

**Use this framework when:**
- Reviewing algorithm comparison papers
- Auditing published evaluation methodologies
- Designing robust evaluation protocols
- Teaching research methodology best practices

## 📊 Dataset

### Full Dataset (Zenodo)

The complete dataset contains 200K+ **Open datasets** with 200K+ evaluation records archived on Zenodo (DOI: 10.5281/zenodo.17201032):
- **Computer Vision**: ImageNet classification evaluations
- **NLP**: GLUE benchmark sequences
- **Recommender Systems**: MovieLens-100K protocols
- **Monte Carlo Simulations**: 13 controlled bias scenarios

**Access**: [Zenodo Dataset (DOI: 10.5281/zenodo.17201032)](https://doi.org/10.5281/zenodo.17201032)

### Data Format

The framework expects two input matrices:

#### Performance Matrix (T × K)
- **Rows**: Time periods (evaluation iterations)
- **Columns**: Algorithms being evaluated
- **Values**: Performance metrics (e.g., accuracy, F1-score)

#### Constraint Matrix (T × p)
- **Rows**: Time periods (evaluation iterations)
- **Columns**: Constraint specifications
- **Values**: Resource limits or evaluation settings

**Example constraint types:**
- Computational budget (FLOPs, GPU hours)
- Memory limits (RAM, VRAM)
- Dataset size (number of training samples)
- Evaluation time limits

### Sample Data

A sample dataset is provided in `data/sample_data.csv` with the following fields:

| Field | Type | Description |
|-------|------|-------------|
| `time_period` | int | Sequential evaluation period (1, 2, 3, ...) |
| `algorithm` | str | Algorithm name |
| `performance` | float | Performance metric (0-1 scale) |
| `constraint_compute` | float | Computational resource limit |
| `constraint_memory` | float | Memory limit (GB) |
| `constraint_dataset_size` | int | Training dataset size |
| `evaluation_protocol` | str | Protocol version identifier |

See `data/README.md` for detailed usage instructions.

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/hongping-zh/circular-bias-detection.git
cd circular-bias-detection
pip install -r requirements.txt
```

### Basic Usage

```python
import numpy as np
import pandas as pd
from circular_bias_detector import BiasDetector

# Option 1: Load from CSV file
df = pd.read_csv('data/sample_data.csv')

# Prepare performance matrix (T x K)
performance_matrix = df.pivot(
    index='time_period',
    columns='algorithm',
    values='performance'
).values

# Prepare constraint matrix (T x p)
constraint_matrix = df.groupby('time_period')[[
    'constraint_compute',
    'constraint_memory',
    'constraint_dataset_size'
]].first().values

algorithms = df['algorithm'].unique().tolist()

# Option 2: Use your own numpy arrays
# performance_matrix = np.array([...])  # Shape: (T, K)
# constraint_matrix = np.array([...])    # Shape: (T, p)
# algorithms = ['ResNet', 'VGG', 'DenseNet']

# Run bias detection
detector = BiasDetector()
results = detector.detect_bias(
    performance_matrix=performance_matrix,
    constraint_matrix=constraint_matrix,
    algorithm_names=algorithms
)

# Display results
print(f"PSI Score: {results['psi_score']:.4f}")
print(f"CCS Score: {results['ccs_score']:.4f}")
print(f"ρ_PC Score: {results['rho_pc_score']:+.4f}")
print(f"Bias Detected: {results['overall_bias']}")
print(f"Confidence: {results['confidence']:.1%}")

# Generate detailed report
report = detector.generate_report(results)
print(report)
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
├── LICENSE                     # CC-BY-4.0 License
└── README.md                   # This file
```

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

## 📄 License

This project is licensed under the Creative Commons Attribution 4.0 International License (CC BY 4.0) - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Hongping Zhang**
- ORCID: [0009-0000-2529-4613](https://orcid.org/0009-0000-2529-4613)
- Email: yujjam@uest.edu.gr

## 🙏 Acknowledgments

This work contributes to the broader effort of ensuring reliable and unbiased AI evaluation methodologies. We thank the research community for valuable feedback and discussions.
