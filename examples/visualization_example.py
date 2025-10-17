"""
Visualization Example for Circular Bias Detection

Demonstrates enhanced visualization features including:
- Performance heatmaps
- Constraint evolution heatmaps
- Interactive Plotly dashboards
- Correlation matrices
- Time series with statistical annotations
"""

import numpy as np
import pandas as pd
from circular_bias_detector import BiasDetector
from circular_bias_detector.visualization import (
    plot_performance_heatmap,
    plot_constraint_heatmap,
    plot_interactive_dashboard,
    plot_correlation_matrix,
    plot_time_series_with_ci
)

print("=" * 60)
print("ENHANCED VISUALIZATION EXAMPLE")
print("=" * 60)

# Load LLM evaluation data
df = pd.read_csv('data/llm_eval_sample.csv')

# Prepare matrices
performance_matrix = df.pivot(
    index='time_period',
    columns='algorithm',
    values='performance'
).values

algorithms = df['algorithm'].unique().tolist()

constraint_columns = [
    'constraint_compute',
    'constraint_memory',
    'constraint_dataset_size',
    'max_tokens',
    'temperature'
]

constraint_matrix = df.groupby('time_period')[constraint_columns].first().values

# Run detection with bootstrap
print("\nRunning bias detection with bootstrap (n=1000)...")
detector = BiasDetector()
results = detector.detect_bias(
    performance_matrix=performance_matrix,
    constraint_matrix=constraint_matrix,
    algorithm_names=algorithms,
    enable_bootstrap=True,
    n_bootstrap=1000
)

print(f"PSI:  {results['psi_score']:.4f} (p={results['psi_pvalue']:.3f})")
print(f"CCS:  {results['ccs_score']:.4f} (p={results['ccs_pvalue']:.3f})")
print(f"ρ_PC: {results['rho_pc_score']:+.4f} (p={results['rho_pc_pvalue']:.3f})")

# 1. Performance Heatmap
print("\n1. Generating performance heatmap...")
try:
    plot_performance_heatmap(
        performance_matrix=performance_matrix,
        algorithm_names=algorithms,
        time_labels=[f'Period {i}' for i in range(1, len(performance_matrix)+1)],
        save_path='visualizations/performance_heatmap.png'
    )
    print("   ✅ Saved to: visualizations/performance_heatmap.png")
except Exception as e:
    print(f"   ⚠️  {e}")

# 2. Constraint Heatmap
print("\n2. Generating constraint heatmap...")
try:
    plot_constraint_heatmap(
        constraint_matrix=constraint_matrix,
        constraint_names=constraint_columns,
        time_labels=[f'Period {i}' for i in range(1, len(constraint_matrix)+1)],
        save_path='visualizations/constraint_heatmap.png'
    )
    print("   ✅ Saved to: visualizations/constraint_heatmap.png")
except Exception as e:
    print(f"   ⚠️  {e}")

# 3. Interactive Dashboard (Plotly)
print("\n3. Generating interactive dashboard...")
try:
    plot_interactive_dashboard(
        performance_matrix=performance_matrix,
        constraint_matrix=constraint_matrix,
        results=results,
        algorithm_names=algorithms,
        save_html='visualizations/interactive_dashboard.html'
    )
    print("   ✅ Saved to: visualizations/interactive_dashboard.html")
    print("   💡 Open in browser for interactive features")
except Exception as e:
    print(f"   ⚠️  {e}")

# 4. Correlation Matrix
print("\n4. Generating correlation matrix...")
try:
    plot_correlation_matrix(
        performance_matrix=performance_matrix,
        constraint_matrix=constraint_matrix,
        algorithm_names=algorithms,
        constraint_names=constraint_columns,
        save_path='visualizations/correlation_matrix.png'
    )
    print("   ✅ Saved to: visualizations/correlation_matrix.png")
except Exception as e:
    print(f"   ⚠️  {e}")

# 5. Time Series with Confidence Intervals
print("\n5. Generating time series with statistical annotations...")
try:
    plot_time_series_with_ci(
        performance_matrix=performance_matrix,
        results=results,
        algorithm_names=algorithms,
        save_path='visualizations/time_series_ci.png'
    )
    print("   ✅ Saved to: visualizations/time_series_ci.png")
except Exception as e:
    print(f"   ⚠️  {e}")

print("\n" + "=" * 60)
print("VISUALIZATION COMPLETE")
print("=" * 60)
print("\n📁 All visualizations saved to: visualizations/")
print("\nGenerated files:")
print("  - performance_heatmap.png: Color-coded performance evolution")
print("  - constraint_heatmap.png: Constraint changes over time")
print("  - interactive_dashboard.html: Interactive Plotly dashboard")
print("  - correlation_matrix.png: Performance-constraint correlations")
print("  - time_series_ci.png: Trajectories with p-values")
print("\n💡 TIP: Open interactive_dashboard.html in a browser for")
print("         hover tooltips and zoom functionality!")
print("=" * 60)
