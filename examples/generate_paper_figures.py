#!/usr/bin/env python3
"""
Generate figures and visualizations from the paper.

This script reproduces the main figures showing:
1. Indicator distributions across scenarios
2. ROC curves for detection performance
3. Time-series plots of bias evolution
"""

import numpy as np
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from circular_bias_detector import BiasDetector
from circular_bias_detector.utils import create_synthetic_data

try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    HAS_PLOTTING = True
except ImportError:
    print("⚠️  Warning: matplotlib/seaborn not installed. Plotting unavailable.")
    HAS_PLOTTING = False


def figure_1_indicator_distributions():
    """
    Figure 1: Distribution of indicators across bias levels.
    """
    if not HAS_PLOTTING:
        print("Skipping Figure 1 (plotting libraries unavailable)")
        return
    
    print("Generating Figure 1: Indicator Distributions...")
    
    bias_levels = [0.0, 0.3, 0.6, 0.9]
    n_samples = 30
    
    psi_data = {level: [] for level in bias_levels}
    ccs_data = {level: [] for level in bias_levels}
    rho_pc_data = {level: [] for level in bias_levels}
    
    # Generate data
    for bias_level in bias_levels:
        for i in range(n_samples):
            perf, const = create_synthetic_data(
                n_time_periods=15,
                n_algorithms=4,
                n_constraints=3,
                bias_intensity=bias_level,
                random_seed=i
            )
            
            detector = BiasDetector()
            results = detector.detect_bias(perf, const)
            
            psi_data[bias_level].append(results['psi_score'])
            ccs_data[bias_level].append(results['ccs_score'])
            rho_pc_data[bias_level].append(abs(results['rho_pc_score']))
    
    # Create plot
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    
    # PSI
    for level in bias_levels:
        axes[0].hist(psi_data[level], alpha=0.6, label=f'Bias={level:.1f}', bins=10)
    axes[0].axvline(x=0.15, color='red', linestyle='--', label='Threshold')
    axes[0].set_xlabel('PSI Score')
    axes[0].set_ylabel('Frequency')
    axes[0].set_title('Performance-Structure Independence (PSI)')
    axes[0].legend()
    
    # CCS
    for level in bias_levels:
        axes[1].hist(ccs_data[level], alpha=0.6, label=f'Bias={level:.1f}', bins=10)
    axes[1].axvline(x=0.85, color='red', linestyle='--', label='Threshold')
    axes[1].set_xlabel('CCS Score')
    axes[1].set_ylabel('Frequency')
    axes[1].set_title('Constraint-Consistency Score (CCS)')
    axes[1].legend()
    
    # ρ_PC
    for level in bias_levels:
        axes[2].hist(rho_pc_data[level], alpha=0.6, label=f'Bias={level:.1f}', bins=10)
    axes[2].axvline(x=0.5, color='red', linestyle='--', label='Threshold')
    axes[2].set_xlabel('|ρ_PC| Score')
    axes[2].set_ylabel('Frequency')
    axes[2].set_title('Performance-Constraint Correlation')
    axes[2].legend()
    
    plt.tight_layout()
    plt.savefig('figure_1_indicator_distributions.png', dpi=300, bbox_inches='tight')
    print("✅ Saved: figure_1_indicator_distributions.png")
    plt.close()


def figure_2_detection_performance():
    """
    Figure 2: Detection rate vs. bias intensity.
    """
    if not HAS_PLOTTING:
        print("Skipping Figure 2 (plotting libraries unavailable)")
        return
    
    print("Generating Figure 2: Detection Performance Curve...")
    
    bias_levels = np.linspace(0, 1, 11)
    n_replications = 30
    
    detection_rates = []
    confidence_intervals = []
    
    for bias_level in bias_levels:
        detections = []
        
        for rep in range(n_replications):
            perf, const = create_synthetic_data(
                n_time_periods=15,
                n_algorithms=4,
                n_constraints=3,
                bias_intensity=bias_level,
                random_seed=rep
            )
            
            detector = BiasDetector()
            results = detector.detect_bias(perf, const)
            detections.append(results['overall_bias'])
        
        detection_rate = np.mean(detections)
        ci = 1.96 * np.std(detections) / np.sqrt(n_replications)
        
        detection_rates.append(detection_rate)
        confidence_intervals.append(ci)
    
    # Plot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.plot(bias_levels, detection_rates, 'o-', linewidth=2, markersize=8, label='Detection Rate')
    ax.fill_between(bias_levels, 
                     np.array(detection_rates) - np.array(confidence_intervals),
                     np.array(detection_rates) + np.array(confidence_intervals),
                     alpha=0.3, label='95% CI')
    
    ax.axhline(y=0.9, color='green', linestyle='--', alpha=0.5, label='90% Detection Target')
    ax.set_xlabel('Bias Intensity', fontsize=12)
    ax.set_ylabel('Detection Rate', fontsize=12)
    ax.set_title('Framework Detection Performance vs. Bias Intensity', fontsize=14)
    ax.grid(True, alpha=0.3)
    ax.legend()
    ax.set_ylim([-0.05, 1.05])
    
    plt.tight_layout()
    plt.savefig('figure_2_detection_performance.png', dpi=300, bbox_inches='tight')
    print("✅ Saved: figure_2_detection_performance.png")
    plt.close()


def figure_3_time_series_example():
    """
    Figure 3: Time-series visualization of biased vs. clean evaluation.
    """
    if not HAS_PLOTTING:
        print("Skipping Figure 3 (plotting libraries unavailable)")
        return
    
    print("Generating Figure 3: Time-Series Comparison...")
    
    # Generate clean and biased scenarios
    perf_clean, const_clean = create_synthetic_data(
        n_time_periods=20, n_algorithms=3, n_constraints=2,
        bias_intensity=0.0, random_seed=42
    )
    
    perf_biased, const_biased = create_synthetic_data(
        n_time_periods=20, n_algorithms=3, n_constraints=2,
        bias_intensity=0.8, random_seed=123
    )
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    time = np.arange(1, 21)
    
    # Clean: Performance
    for k in range(3):
        axes[0, 0].plot(time, perf_clean[:, k], 'o-', label=f'Algo {k+1}')
    axes[0, 0].set_title('Clean Evaluation: Algorithm Performance')
    axes[0, 0].set_xlabel('Time Period')
    axes[0, 0].set_ylabel('Performance')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # Clean: Constraints
    for j in range(2):
        axes[0, 1].plot(time, const_clean[:, j], 's-', label=f'Constraint {j+1}')
    axes[0, 1].set_title('Clean Evaluation: Constraints')
    axes[0, 1].set_xlabel('Time Period')
    axes[0, 1].set_ylabel('Constraint Value')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    # Biased: Performance
    for k in range(3):
        axes[1, 0].plot(time, perf_biased[:, k], 'o-', label=f'Algo {k+1}')
    axes[1, 0].set_title('Biased Evaluation: Algorithm Performance')
    axes[1, 0].set_xlabel('Time Period')
    axes[1, 0].set_ylabel('Performance')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)
    
    # Biased: Constraints
    for j in range(2):
        axes[1, 1].plot(time, const_biased[:, j], 's-', label=f'Constraint {j+1}')
    axes[1, 1].set_title('Biased Evaluation: Constraints')
    axes[1, 1].set_xlabel('Time Period')
    axes[1, 1].set_ylabel('Constraint Value')
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('figure_3_time_series_comparison.png', dpi=300, bbox_inches='tight')
    print("✅ Saved: figure_3_time_series_comparison.png")
    plt.close()


def figure_4_correlation_scatter():
    """
    Figure 4: Scatter plot showing performance-constraint correlation.
    """
    if not HAS_PLOTTING:
        print("Skipping Figure 4 (plotting libraries unavailable)")
        return
    
    print("Generating Figure 4: Correlation Visualization...")
    
    # Generate scenarios
    perf_clean, const_clean = create_synthetic_data(
        n_time_periods=25, n_algorithms=4, n_constraints=3,
        bias_intensity=0.0, random_seed=42
    )
    
    perf_biased, const_biased = create_synthetic_data(
        n_time_periods=25, n_algorithms=4, n_constraints=3,
        bias_intensity=0.85, random_seed=456
    )
    
    # Aggregate metrics
    avg_perf_clean = np.mean(perf_clean, axis=1)
    avg_const_clean = np.mean(const_clean, axis=1)
    
    avg_perf_biased = np.mean(perf_biased, axis=1)
    avg_const_biased = np.mean(const_biased, axis=1)
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # Clean scenario
    axes[0].scatter(avg_const_clean, avg_perf_clean, s=100, alpha=0.6)
    axes[0].set_xlabel('Average Constraint Value', fontsize=11)
    axes[0].set_ylabel('Average Performance', fontsize=11)
    axes[0].set_title('Clean Evaluation (ρ_PC ≈ 0)', fontsize=12)
    
    # Add trend line
    z = np.polyfit(avg_const_clean, avg_perf_clean, 1)
    p = np.poly1d(z)
    axes[0].plot(avg_const_clean, p(avg_const_clean), "r--", alpha=0.5)
    
    corr_clean = np.corrcoef(avg_const_clean, avg_perf_clean)[0, 1]
    axes[0].text(0.05, 0.95, f'ρ = {corr_clean:+.3f}', 
                transform=axes[0].transAxes, fontsize=11,
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    axes[0].grid(True, alpha=0.3)
    
    # Biased scenario
    axes[1].scatter(avg_const_biased, avg_perf_biased, s=100, alpha=0.6, color='red')
    axes[1].set_xlabel('Average Constraint Value', fontsize=11)
    axes[1].set_ylabel('Average Performance', fontsize=11)
    axes[1].set_title('Biased Evaluation (|ρ_PC| > 0.5)', fontsize=12)
    
    # Add trend line
    z = np.polyfit(avg_const_biased, avg_perf_biased, 1)
    p = np.poly1d(z)
    axes[1].plot(avg_const_biased, p(avg_const_biased), "r--", alpha=0.5)
    
    corr_biased = np.corrcoef(avg_const_biased, avg_perf_biased)[0, 1]
    axes[1].text(0.05, 0.95, f'ρ = {corr_biased:+.3f}', 
                transform=axes[1].transAxes, fontsize=11,
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('figure_4_correlation_scatter.png', dpi=300, bbox_inches='tight')
    print("✅ Saved: figure_4_correlation_scatter.png")
    plt.close()


def main():
    """Generate all paper figures."""
    print("=" * 70)
    print("GENERATING PAPER FIGURES")
    print("=" * 70)
    
    if not HAS_PLOTTING:
        print("\n❌ Error: matplotlib and seaborn are required for plotting.")
        print("Install with: pip install matplotlib seaborn")
        return
    
    print("\nGenerating figures (this may take 1-2 minutes)...\n")
    
    figure_1_indicator_distributions()
    figure_2_detection_performance()
    figure_3_time_series_example()
    figure_4_correlation_scatter()
    
    print("\n" + "=" * 70)
    print("FIGURE GENERATION COMPLETE")
    print("=" * 70)
    print("\nGenerated files:")
    print("• figure_1_indicator_distributions.png")
    print("• figure_2_detection_performance.png")
    print("• figure_3_time_series_comparison.png")
    print("• figure_4_correlation_scatter.png")
    print("\nThese figures can be used in publications, presentations,")
    print("or for validating the framework's detection capabilities.")


if __name__ == "__main__":
    main()
