# Data Directory

This directory contains sample datasets for the Circular Reasoning Bias Detection Framework.

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

## Full Dataset

The complete dataset used in the paper is available on Zenodo:
- **DOI**: [10.5281/zenodo.17196639](https://doi.org/10.5281/zenodo.17196639)
- **Size**: 200K+ evaluation records
- **Domains**: Computer Vision, NLP, Recommender Systems, Monte Carlo Simulations

See the main README for more details about the full dataset.
