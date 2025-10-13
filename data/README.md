# Data Directory

This directory contains sample datasets and documentation for the Circular Reasoning Bias Detection Framework.

## 📁 Directory Contents

| File | Description |
|------|-------------|
| `sample_data.csv` | Sample evaluation data (20 records) |
| `schema.json` | JSON Schema for data validation |
| `DATA_DICTIONARY.md` | Detailed field specifications |
| `generate_benchmark_data.py` | Script to reproduce all benchmark data |
| `README.md` | This file |

## Sample Data Files

### sample_data.csv

A simplified example dataset demonstrating the expected data format for bias detection.

**Structure:**
- Each row represents one algorithm's performance in one evaluation period
- Multiple algorithms evaluated across multiple time periods
- Performance metrics and constraint values are recorded

**Fields:**
- `time_period`: Sequential evaluation period (1, 2, 3, ...)
- `algorithm`: Name of the algorithm being evaluated
- `performance`: Performance metric (e.g., accuracy, 0-1 scale)
- `constraint_compute`: Computational resource limit (e.g., FLOPs)
- `constraint_memory`: Memory limit (e.g., GB)
- `constraint_dataset_size`: Training dataset size (number of samples)
- `evaluation_protocol`: Version identifier of the evaluation protocol

**Usage:**
```python
import pandas as pd
from circular_bias_detector import BiasDetector

# Load sample data
df = pd.read_csv('data/sample_data.csv')

# Prepare matrices
algorithms = df['algorithm'].unique()
time_periods = df['time_period'].unique()

# Create performance matrix (T x K)
performance_matrix = df.pivot(
    index='time_period', 
    columns='algorithm', 
    values='performance'
).values

# Create constraint matrix (T x p)
constraint_matrix = df.groupby('time_period')[
    ['constraint_compute', 'constraint_memory', 'constraint_dataset_size']
].first().values

# Run bias detection
detector = BiasDetector()
results = detector.detect_bias(
    performance_matrix=performance_matrix,
    constraint_matrix=constraint_matrix,
    algorithm_names=list(algorithms)
)

print(results)
```

## 📖 Documentation

### Data Dictionary
For detailed field specifications, see [`DATA_DICTIONARY.md`](DATA_DICTIONARY.md):
- Field types and constraints
- Value ranges and examples
- Validation rules
- Usage examples

### JSON Schema
Validate your data against the schema:
```bash
pip install jsonschema
python -c "
import pandas as pd
import json
import jsonschema

# Load schema
with open('data/schema.json') as f:
    schema = json.load(f)

# Load and validate data
df = pd.read_csv('data/sample_data.csv')
for _, record in df.iterrows():
    jsonschema.validate(record.to_dict(), schema)
print('✓ Data is valid!')
"
```

## 🔄 Reproducing the Data

Generate all benchmark scenarios:
```bash
cd data
python generate_benchmark_data.py --output-dir ./generated_data --validate
```

This will create 10 CSV files with various bias and noise configurations.

## 📊 Full Dataset

The complete Algorithm Benchmark Suite v2.0 is available on Zenodo:
- **DOI**: [10.5281/zenodo.17196639](https://doi.org/10.5281/zenodo.17196639)
- **Version**: 2.0.0
- **Files**: 10 CSV files (algorithm_benchmark_suite.csv + 9 scenarios)
- **Total Records**: 500+
- **Scenarios**: Varying bias intensities, noise levels, and temporal configurations

### Zenodo Dataset Contents
1. `algorithm_benchmark_suite.csv` - Main benchmark (20 records)
2. `scenario_no_bias_low_noise.csv` - Clean baseline
3. `scenario_no_bias_high_noise.csv` - High measurement noise
4. `scenario_mild_bias.csv` - Bias intensity 0.3
5. `scenario_moderate_bias.csv` - Bias intensity 0.6
6. `scenario_high_bias.csv` - Bias intensity 0.9
7. `scenario_few_periods.csv` - Limited temporal data
8. `scenario_many_algorithms.csv` - Extended algorithm set
9. `scenario_mixed_conditions.csv` - Complex scenario
10. `scenario_edge_case.csv` - Edge case testing

## 📝 Citation

```bibtex
@dataset{zhang2024_benchmark,
  author = {Zhang, Hongping},
  title = {Algorithm Benchmark Suite v2.0},
  year = {2024},
  publisher = {Zenodo},
  version = {2.0.0},
  doi = {10.5281/zenodo.17196639}
}
```

## 🔗 Links

- **GitHub Repository**: https://github.com/hongping-zh/circular-bias-detection
- **Software Framework**: See main README for installation and usage
- **Issue Tracker**: https://github.com/hongping-zh/circular-bias-detection/issues
- **Contact**: yujjam@uest.edu.gr

See the main README for more details about the detection framework.
