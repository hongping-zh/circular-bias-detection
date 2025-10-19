# 📚 Sleuth Examples & Tutorials

**Learn how to use Sleuth with hands-on examples!**

---

## 🚀 Quick Start

### For Beginners

1. **[Google Colab Quick Start](quickstart_colab.ipynb)** ⭐ **Recommended**
   - [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/hongping-zh/circular-bias-detection/blob/main/examples/quickstart_colab.ipynb)
   - Zero installation required
   - 5-minute tutorial
   - Interactive widgets

2. **[Jupyter Extension Guide](jupyter_extension_guide.md)**
   - Install in your local Jupyter
   - Custom magic commands
   - Export to PDF/JSON

3. **[Interactive Demo](demo_notebook.ipynb)**
   - [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/hongping-zh/circular-bias-detection/blob/main/examples/demo_notebook.ipynb)
   - Comprehensive walkthrough
   - Visualizations included

---

## 📂 Example Files

### Python Scripts

| File | Description | Use Case |
|------|-------------|----------|
| [`basic_usage_example.py`](basic_usage_example.py) | Simple 10-line example | Quick checks |
| [`llm_evaluation_example.py`](llm_evaluation_example.py) | LLM-specific evaluation | GPT/Llama/Claude testing |
| [`bootstrap_example.py`](bootstrap_example.py) | Statistical significance | Research papers |
| [`visualization_example.py`](visualization_example.py) | Publication-ready plots | Conference submissions |
| [`reproduce_case_studies.py`](reproduce_case_studies.py) | Paper case studies | Academic validation |
| [`reproduce_simulations.py`](reproduce_simulations.py) | Controlled experiments | Benchmarking |
| [`generate_paper_figures.py`](generate_paper_figures.py) | Figure generation | Publication figures |

### Jupyter Notebooks

| Notebook | Best For | Open in Colab |
|----------|----------|---------------|
| [`quickstart_colab.ipynb`](quickstart_colab.ipynb) | **First-time users** | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/hongping-zh/circular-bias-detection/blob/main/examples/quickstart_colab.ipynb) |
| [`demo_notebook.ipynb`](demo_notebook.ipynb) | **Comprehensive learning** | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/hongping-zh/circular-bias-detection/blob/main/examples/demo_notebook.ipynb) |

---

## 🎯 Use Case Examples

### Example 1: LLM Evaluation

```python
from circular_bias_detector import SimpleBiasDetector
import pandas as pd

# Your GPT-4, Llama, Claude evaluation data
df = pd.read_csv('llm_eval.csv')

detector = SimpleBiasDetector()
performance = df.pivot('time_period', 'algorithm', 'performance').values
constraints = df.groupby('time_period')[['constraint_compute']].first().values

result = detector.quick_check(performance, constraints)

if result['has_bias']:
    print(f"⚠️ Risk: {result['recommendation']}")
else:
    print("✅ Safe to report results")
```

### Example 2: Computer Vision

```python
# ImageNet classification across multiple runs
df = pd.read_csv('imagenet_eval.csv')

detector = BiasDetector(enable_bootstrap=True, n_bootstrap=1000)
results = detector.detect_bias(performance_matrix, constraint_matrix)

print(f"PSI: {results['psi']:.4f} [CI: {results['psi_ci_lower']:.4f}-{results['psi_ci_upper']:.4f}]")
```

### Example 3: CI/CD Integration

```bash
# Automated testing in your pipeline
circular-bias detect evaluation_data.csv --format json --output results.json

# Check exit code
if [ $? -ne 0 ]; then
    echo "Bias detected - blocking deployment"
    exit 1
fi
```

---

## 📊 Data Format Examples

### Minimal Example

```csv
time_period,algorithm,performance,constraint_compute
1,ModelA,0.85,512
1,ModelB,0.78,512
2,ModelA,0.87,550
2,ModelB,0.80,550
```

### Full Example

```csv
time_period,algorithm,performance,constraint_compute,constraint_memory,constraint_dataset_size,evaluation_protocol
1,GPT-4,0.92,1000,16.0,10000,v1.0
1,Llama-2,0.88,1200,18.0,10000,v1.0
2,GPT-4,0.94,1050,17.0,12000,v1.1
2,Llama-2,0.90,1250,19.0,12000,v1.1
```

**See full examples:** [`../data/sample_data.csv`](../data/sample_data.csv)

---

## 🎓 Tutorials by Level

### Beginner (< 5 minutes)

1. [Google Colab Quickstart](quickstart_colab.ipynb) - No setup required
2. [Basic Usage Example](basic_usage_example.py) - Simple Python script

### Intermediate (15-30 minutes)

1. [LLM Evaluation Guide](llm_evaluation_example.py) - Practical scenarios
2. [Visualization Tutorial](visualization_example.py) - Publication plots
3. [Jupyter Extension](jupyter_extension_guide.md) - Workflow integration

### Advanced (1+ hour)

1. [Bootstrap Analysis](bootstrap_example.py) - Statistical rigor
2. [Case Study Reproduction](reproduce_case_studies.py) - Academic validation
3. [Custom Simulations](reproduce_simulations.py) - Benchmark creation

---

## 🔧 Running Examples

### Option 1: Google Colab (Easiest)

Click any "Open in Colab" badge above - no installation needed!

### Option 2: Local Jupyter

```bash
# Install dependencies
pip install numpy pandas scipy matplotlib seaborn jupyter

# Clone repository
git clone https://github.com/hongping-zh/circular-bias-detection.git
cd circular-bias-detection/examples

# Launch Jupyter
jupyter notebook
```

### Option 3: Python Scripts

```bash
# Install framework
pip install numpy pandas scipy matplotlib

# Clone repository
git clone https://github.com/hongping-zh/circular-bias-detection.git
cd circular-bias-detection

# Run example
python examples/basic_usage_example.py
```

---

## 📖 Additional Resources

### Documentation
- [Main README](../README.md) - Project overview
- [Data Dictionary](../data/DATA_DICTIONARY.md) - Field specifications
- [Jupyter Extension Guide](jupyter_extension_guide.md) - Notebook integration

### Datasets
- [Sample Data](../data/sample_data.csv) - 20 records for testing
- [Full Dataset (Zenodo)](https://doi.org/10.5281/zenodo.17201032) - 200K+ records

### Tools
- [Web App](https://hongping-zh.github.io/circular-bias-detection/) - No-code interface
- [CLI Tool](../README.md#cli-tool) - Command-line usage

---

## 💡 Tips & Best Practices

### Tip 1: Start Simple
Begin with `basic_usage_example.py` before exploring advanced features.

### Tip 2: Use Colab for Experiments
Google Colab is perfect for trying examples without local setup.

### Tip 3: Check Data Format
Validate your CSV matches the expected format before running detection.

### Tip 4: Enable Bootstrap for Papers
If publishing results, always use `enable_bootstrap=True` for statistical rigor.

### Tip 5: Export Results
Save results to JSON/PDF for reproducibility and sharing.

---

## 🐛 Troubleshooting

### Issue: Module not found

```python
import sys
sys.path.insert(0, '/path/to/circular-bias-detection')
```

### Issue: Import errors

```bash
pip install numpy pandas scipy matplotlib seaborn
```

### Issue: Data format errors

Check your CSV has these required columns:
- `time_period` (int)
- `algorithm` (str)
- `performance` (float)
- At least one constraint column

---

## 🤝 Contributing Examples

Have a useful example? Share it!

1. Fork the repository
2. Add your example to `examples/`
3. Update this README
4. Submit a pull request

**Example template:**
- Clear docstrings
- Sample data included
- Expected output shown
- < 100 lines of code

---

## 📬 Questions?

- **Issues**: [GitHub Issues](https://github.com/hongping-zh/circular-bias-detection/issues)
- **Email**: yujjam@uest.edu.gr
- **Web App**: [Try online](https://hongping-zh.github.io/circular-bias-detection/)

---

**Happy learning! 🚀**
