# Data Dictionary - Algorithm Benchmark Suite v2.0

## Overview

This document provides detailed specifications for all fields in the Algorithm Benchmark Suite dataset.

**Dataset Version:** 2.0.0  
**Last Updated:** October 13, 2024  
**DOI:** [10.5281/zenodo.17201032](https://doi.org/10.5281/zenodo.17201032)

---

## File Structure

The dataset consists of 10 CSV files:

| File | Records | Description |
|------|---------|-------------|
| `algorithm_benchmark_suite.csv` | 20 | Main benchmark with clean data |
| `scenario_no_bias_low_noise.csv` | 60 | No bias, minimal noise (σ=0.05) |
| `scenario_no_bias_high_noise.csv` | 60 | No bias, high noise (σ=0.2) |
| `scenario_mild_bias.csv` | 60 | Mild circular bias (intensity=0.3) |
| `scenario_moderate_bias.csv` | 60 | Moderate circular bias (intensity=0.6) |
| `scenario_high_bias.csv` | 60 | High circular bias (intensity=0.9) |
| `scenario_few_periods.csv` | 32 | Limited temporal data (8 periods) |
| `scenario_many_algorithms.csv` | 72 | Extended algorithm set (6 algorithms) |
| `scenario_mixed_conditions.csv` | 100 | Complex scenario (20 periods, 5 algorithms) |
| `scenario_edge_case.csv` | 30 | Edge case testing (3 algorithms, high bias) |

---

## Field Specifications

### 1. `time_period`

**Type:** Integer  
**Required:** Yes  
**Range:** [1, ∞)  
**Description:** Sequential identifier for evaluation time periods. Represents chronological order of algorithm evaluations.

**Examples:**
```
1, 2, 3, 4, 5
```

**Use Case:** Temporal analysis, trend detection, circular bias identification

**Notes:**
- Consecutive integers starting from 1
- Each time period may represent weeks, months, or evaluation cycles depending on context

---

### 2. `algorithm`

**Type:** String  
**Required:** Yes  
**Constraints:** Non-empty, alphanumeric with hyphens/underscores allowed  
**Description:** Unique identifier or name of the algorithm being evaluated.

**Examples:**
```
"ResNet"
"VGG"
"DenseNet"
"EfficientNet"
"BERT-base"
"GPT-3.5"
```

**Use Case:** Algorithm identification, performance comparison

**Notes:**
- Case-sensitive
- Common naming conventions from ML literature
- May include version numbers (e.g., "ResNet-50")

---

### 3. `performance`

**Type:** Float  
**Required:** Yes  
**Range:** [0.0, 1.0]  
**Precision:** 4 decimal places  
**Description:** Normalized performance metric (e.g., accuracy, F1 score) on a 0-1 scale.

**Examples:**
```
0.7234  # 72.34% accuracy
0.8901  # 89.01% F1 score
0.6543  # 65.43% AUC-ROC
```

**Use Case:** Performance comparison, bias detection (dependent variable)

**Calculation:**
```
performance = raw_metric / max_possible_value
```

**Notes:**
- Higher values indicate better performance
- Accounts for metric-specific normalization
- Missing values not permitted

---

### 4. `constraint_compute`

**Type:** Float  
**Required:** Yes  
**Range:** [0, ∞)  
**Unit:** Domain-specific (e.g., FLOPs, milliseconds)  
**Description:** Computational resource constraint or limit applied during evaluation.

**Examples:**
```
300.0   # 300 GFLOPs
1500.5  # 1500.5 ms inference time
42.7    # 42.7 GPU hours
```

**Use Case:** Resource-performance trade-off analysis, constraint consistency checking

**Notes:**
- Units may vary by domain (document in `evaluation_protocol`)
- Represents maximum allowed, not actual usage
- Can detect constraint manipulation if values vary suspiciously with performance

---

### 5. `constraint_memory`

**Type:** Float  
**Required:** Yes  
**Range:** [0, ∞)  
**Unit:** Gigabytes (GB)  
**Description:** Memory constraint limit during algorithm execution.

**Examples:**
```
8.0    # 8 GB RAM
16.5   # 16.5 GB GPU memory
32.0   # 32 GB combined memory
```

**Use Case:** Hardware requirement analysis, memory-performance correlation

**Notes:**
- Typically represents GPU or system RAM
- May include model parameters + activations + batch size overhead
- Precision: 1 decimal place

---

### 6. `constraint_dataset_size`

**Type:** Integer  
**Required:** Yes  
**Range:** [0, ∞)  
**Unit:** Number of samples  
**Description:** Training dataset size constraint (number of labeled examples allowed).

**Examples:**
```
50000   # 50K training samples (e.g., ImageNet subset)
1000000 # 1M samples (e.g., full dataset)
5000    # 5K samples (few-shot scenario)
```

**Use Case:** Data efficiency analysis, dataset size impact on performance

**Notes:**
- Represents number of training samples, not validation/test
- Integer values only (no fractional samples)
- Can reveal data augmentation or subset selection strategies

---

### 7. `evaluation_protocol`

**Type:** String  
**Required:** Yes  
**Pattern:** `^[A-Za-z0-9._-]+$`  
**Description:** Version identifier of the evaluation protocol/benchmark used.

**Examples:**
```
"ImageNet-v1.0"
"GLUE-v1.2"
"MovieLens-2023"
"COCO-2017"
```

**Use Case:** Protocol version tracking, consistency verification

**Format Convention:**
```
{BenchmarkName}-v{MajorVersion}.{MinorVersion}
{BenchmarkName}-{Year}
{BenchmarkName}-{CustomID}
```

**Notes:**
- Changes to this field across time periods may indicate protocol drift
- Essential for detecting circular bias through protocol manipulation
- Should remain constant within an evaluation campaign

---

## Data Quality Indicators

### Completeness
- **Missing Values:** Not permitted in any field
- **Null Handling:** All fields are required

### Consistency Checks
1. **Temporal Ordering:** `time_period` should be sequential per algorithm
2. **Performance Bounds:** All `performance` values in [0, 1]
3. **Constraint Positivity:** Constraint values should be > 0
4. **Protocol Stability:** `evaluation_protocol` should be stable or have justified changes

### Validation Script
```bash
python generate_benchmark_data.py --validate
```

---

## Usage Examples

### Loading Data

```python
import pandas as pd

# Load main benchmark
df = pd.read_csv('algorithm_benchmark_suite.csv')

# Load specific scenario
df_biased = pd.read_csv('scenario_high_bias.csv')
```

### Basic Analysis

```python
# Performance by algorithm
perf_by_algo = df.groupby('algorithm')['performance'].mean()

# Constraint evolution
import matplotlib.pyplot as plt
df.groupby('time_period')['constraint_compute'].mean().plot()
plt.xlabel('Time Period')
plt.ylabel('Average Compute Constraint')
plt.show()
```

### Bias Detection

```python
from circular_bias_detector import BiasDetector

# Prepare matrices
algorithms = df['algorithm'].unique()
time_periods = df['time_period'].unique()

performance_matrix = df.pivot(
    index='time_period',
    columns='algorithm',
    values='performance'
).values

constraint_matrix = df.groupby('time_period')[
    ['constraint_compute', 'constraint_memory', 'constraint_dataset_size']
].first().values

# Detect bias
detector = BiasDetector()
results = detector.detect_bias(
    performance_matrix=performance_matrix,
    constraint_matrix=constraint_matrix,
    algorithm_names=list(algorithms)
)

print(results)
```

---

## Changelog

### v2.0.0 (2024-10-13)
- Added 9 scenario-specific files
- Introduced structured bias intensity levels
- Enhanced data generation with reproducible scripts
- Added JSON Schema validation

### v1.0.0 (2024-09-25)
- Initial release with main benchmark file
- 20 evaluation records
- 4 algorithms across 5 time periods

---

## Citation

```bibtex
@dataset{zhang2024_benchmark,
  author = {Zhang, Hongping},
  title = {Algorithm Benchmark Suite v2.0},
  year = {2024},
  publisher = {Zenodo},
  version = {2.0.0},
  doi = {10.5281/zenodo.17201032},
  url = {https://doi.org/10.5281/zenodo.17201032}
}
```

---

## License

Creative Commons Attribution 4.0 International (CC BY 4.0)

## Contact

- **Author:** Hongping Zhang
- **Email:** yujjam@uest.edu.gr
- **ORCID:** [0009-0000-2529-4613](https://orcid.org/0009-0000-2529-4613)
- **Repository:** https://github.com/hongping-zh/circular-bias-detection
