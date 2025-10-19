# 📓 Jupyter Notebook Extension for Sleuth

**Make bias detection seamless in your Jupyter workflow!**

---

## 🎯 Quick Install

### Option 1: Jupyter Notebook Magic (Recommended)

Add this cell at the top of your notebook:

```python
# Install and configure Sleuth
!pip install -q numpy pandas scipy matplotlib seaborn
!git clone -q https://github.com/hongping-zh/circular-bias-detection.git

import sys
sys.path.insert(0, 'circular-bias-detection')

from circular_bias_detector import BiasDetector
import pandas as pd
import numpy as np

print("✅ Sleuth ready to use!")
```

### Option 2: Permanent Installation

```bash
# Install in your environment
pip install numpy pandas scipy matplotlib seaborn
git clone https://github.com/hongping-zh/circular-bias-detection.git
cd circular-bias-detection
pip install -e .
```

---

## 🚀 Usage Patterns

### Pattern 1: One-Liner Bias Check

```python
from circular_bias_detector import SimpleBiasDetector

# Your evaluation data
df = pd.read_csv('my_eval.csv')

# Quick check
detector = SimpleBiasDetector()
performance = df.pivot('time_period', 'algorithm', 'performance').values
constraints = df.groupby('time_period')[['constraint_compute', 'constraint_memory']].first().values

result = detector.quick_check(performance, constraints)

# Display
if result['has_bias']:
    print(f"⚠️ {result['risk_level'].upper()} RISK: {result['recommendation']}")
else:
    print("✅ No bias detected - safe to deploy!")
```

### Pattern 2: Interactive Dashboard

```python
from IPython.display import display, HTML
import matplotlib.pyplot as plt

def show_bias_dashboard(results):
    """Display interactive bias detection dashboard"""
    
    # Create visualizations
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    
    indicators = ['PSI', 'CCS', 'ρ_PC']
    values = [results['psi'], results['ccs'], results['rho_pc']]
    thresholds = [0.15, 0.85, 0.50]
    colors = ['red' if (v > t if i != 1 else v < t) else 'green' 
              for i, (v, t) in enumerate(zip(values, thresholds))]
    
    for i, (ax, name, value, threshold, color) in enumerate(
        zip(axes, indicators, values, thresholds, colors)
    ):
        ax.bar([name], [value], color=color, alpha=0.7)
        ax.axhline(threshold, color='black', linestyle='--', linewidth=2)
        ax.set_ylabel('Value')
        ax.set_title(f'{name} = {value:.3f}', fontweight='bold')
        ax.set_ylim([0, 1])
    
    plt.tight_layout()
    plt.show()
    
    # Display HTML summary
    status = "🔴 BIAS DETECTED" if results['overall_bias'] else "✅ NO BIAS"
    html = f"""
    <div style='padding: 20px; border: 3px solid {"red" if results["overall_bias"] else "green"}; 
                border-radius: 10px; background-color: {"#ffe6e6" if results["overall_bias"] else "#e6ffe6"};'>
        <h2 style='margin: 0;'>{status}</h2>
        <p style='font-size: 1.1em; margin-top: 10px;'>
            <strong>Interpretation:</strong> {results.get('interpretation', 'N/A')}
        </p>
    </div>
    """
    display(HTML(html))

# Usage
detector = BiasDetector()
results = detector.detect_bias(performance, constraints, ['Model A', 'Model B'])
show_bias_dashboard(results)
```

### Pattern 3: Inline Cell Magic (Advanced)

Create a custom IPython magic command:

```python
from IPython.core.magic import register_cell_magic
from circular_bias_detector import BiasDetector
import pandas as pd

@register_cell_magic
def detect_bias(line, cell):
    """
    Cell magic for quick bias detection
    
    Usage:
    %%detect_bias
    df = pd.read_csv('data.csv')
    """
    # Execute cell code
    exec(cell, globals())
    
    # Auto-detect DataFrame
    df = globals().get('df')
    if df is None:
        return "❌ No DataFrame named 'df' found"
    
    # Run detection
    detector = BiasDetector()
    performance = df.pivot('time_period', 'algorithm', 'performance').values
    constraints = df.groupby('time_period')[['constraint_compute', 'constraint_memory']].first().values
    
    results = detector.detect_bias(performance, constraints)
    
    if results['overall_bias']:
        print(f"🔴 BIAS DETECTED")
    else:
        print(f"✅ NO BIAS")
    
    return results

print("✅ Cell magic registered! Use %%detect_bias in cells")
```

Then use it:

```python
%%detect_bias
df = pd.read_csv('my_evaluation.csv')
```

---

## 🎨 Notebook Widgets

### Interactive Parameter Tuning

```python
from ipywidgets import interact, FloatSlider

def interactive_detection(psi_threshold, ccs_threshold, rho_threshold):
    detector = BiasDetector(
        psi_threshold=psi_threshold,
        ccs_threshold=ccs_threshold,
        rho_pc_threshold=rho_threshold
    )
    
    results = detector.detect_bias(performance, constraints, ['Model A', 'Model B'])
    
    print(f"PSI: {results['psi']:.4f} {'❌' if results['psi'] > psi_threshold else '✅'}")
    print(f"CCS: {results['ccs']:.4f} {'❌' if results['ccs'] < ccs_threshold else '✅'}")
    print(f"ρ_PC: {results['rho_pc']:.4f} {'❌' if results['rho_pc'] > rho_threshold else '✅'}")
    print(f"\nOverall: {'🔴 BIAS' if results['overall_bias'] else '✅ CLEAN'}")

interact(
    interactive_detection,
    psi_threshold=FloatSlider(min=0.05, max=0.30, step=0.01, value=0.15),
    ccs_threshold=FloatSlider(min=0.70, max=0.95, step=0.01, value=0.85),
    rho_threshold=FloatSlider(min=0.30, max=0.70, step=0.01, value=0.50)
)
```

---

## 📊 Export Options

### Export to PDF Report

```python
def export_report(results, filename='bias_report.pdf'):
    """Generate PDF report from results"""
    from matplotlib.backends.backend_pdf import PdfPages
    
    with PdfPages(filename) as pdf:
        # Page 1: Summary
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.axis('off')
        
        summary = f"""
        BIAS DETECTION REPORT
        {'='*50}
        
        Status: {'BIAS DETECTED' if results['overall_bias'] else 'NO BIAS DETECTED'}
        
        Indicators:
        - PSI: {results['psi']:.4f}
        - CCS: {results['ccs']:.4f}
        - ρ_PC: {results['rho_pc']:.4f}
        
        Interpretation:
        {results.get('interpretation', 'N/A')}
        """
        
        ax.text(0.1, 0.5, summary, fontsize=12, family='monospace', 
                verticalalignment='center')
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()
        
        # Page 2: Visualizations
        # (Add your charts here)
    
    print(f"✅ Report saved to {filename}")

# Usage
export_report(results)
```

### Export to JSON

```python
import json

def export_json(results, filename='results.json'):
    """Export results to JSON"""
    # Convert numpy types to Python types
    clean_results = {}
    for key, value in results.items():
        if isinstance(value, (np.integer, np.floating)):
            clean_results[key] = float(value)
        elif key != 'metadata':
            clean_results[key] = value
    
    with open(filename, 'w') as f:
        json.dump(clean_results, f, indent=2)
    
    print(f"✅ Results saved to {filename}")

export_json(results)
```

---

## 🔧 Troubleshooting

### Common Issues

**Issue 1: Module not found**
```python
# Solution: Add to path
import sys
sys.path.insert(0, '/path/to/circular-bias-detection')
```

**Issue 2: Import errors**
```python
# Solution: Install dependencies
!pip install numpy pandas scipy matplotlib seaborn
```

**Issue 3: Data format errors**
```python
# Solution: Validate your data
def validate_data(df):
    required_cols = ['time_period', 'algorithm', 'performance']
    missing = [col for col in required_cols if col not in df.columns]
    
    if missing:
        print(f"❌ Missing columns: {missing}")
        return False
    
    print("✅ Data format valid")
    return True

validate_data(df)
```

---

## 📚 Example Notebooks

Find complete examples in the repository:

1. **[quickstart_colab.ipynb](quickstart_colab.ipynb)** - 5-minute quick start
2. **[demo_notebook.ipynb](demo_notebook.ipynb)** - Comprehensive demo
3. **[llm_evaluation_example.py](llm_evaluation_example.py)** - LLM-specific examples
4. **[bootstrap_example.py](bootstrap_example.py)** - Statistical analysis

---

## 🤝 Contributing

Have a useful notebook pattern? Share it!

1. Fork the repository
2. Add your notebook to `examples/`
3. Submit a pull request

---

## 📖 Resources

- **Documentation**: [GitHub README](https://github.com/hongping-zh/circular-bias-detection#readme)
- **Web App**: [Try Online](https://hongping-zh.github.io/circular-bias-detection/)
- **Dataset**: [Zenodo](https://doi.org/10.5281/zenodo.17201032)
- **Issues**: [GitHub Issues](https://github.com/hongping-zh/circular-bias-detection/issues)

---

**Happy detecting! 🔍**
