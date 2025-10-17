"""
Visualization utilities for circular bias detection.

This module provides enhanced visualization functions including:
- Heatmaps for performance and constraints
- Time series plots with statistical annotations
- Interactive Plotly charts
- Correlation matrices
"""

import numpy as np
import pandas as pd
from typing import Optional, Tuple, List
import warnings

try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    warnings.warn("matplotlib/seaborn not available. Install with: pip install matplotlib seaborn")

try:
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.subplots import make_subplots
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False
    warnings.warn("plotly not available. Install with: pip install plotly")


def plot_performance_heatmap(performance_matrix: np.ndarray,
                             algorithm_names: Optional[List[str]] = None,
                             time_labels: Optional[List] = None,
                             save_path: Optional[str] = None,
                             figsize: Tuple[int, int] = (10, 6),
                             annotate_pvalues: Optional[dict] = None) -> None:
    """
    Create heatmap of performance across time and algorithms.
    
    Parameters:
    -----------
    performance_matrix : np.ndarray
        Shape (T, K) - performance values
    algorithm_names : list, optional
        Algorithm names for x-axis
    time_labels : list, optional
        Time period labels for y-axis
    save_path : str, optional
        Path to save figure
    figsize : tuple
        Figure size (width, height)
    annotate_pvalues : dict, optional
        Bootstrap p-values to annotate cells
    """
    
    if not HAS_MATPLOTLIB:
        raise ImportError("matplotlib required for heatmaps")
    
    T, K = performance_matrix.shape
    
    if algorithm_names is None:
        algorithm_names = [f'Alg{i+1}' for i in range(K)]
    
    if time_labels is None:
        time_labels = [f'T{i+1}' for i in range(T)]
    
    fig, ax = plt.subplots(figsize=figsize)
    
    # Create heatmap
    im = ax.imshow(performance_matrix, cmap='YlOrRd', aspect='auto')
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Performance Score', rotation=270, labelpad=20)
    
    # Set ticks
    ax.set_xticks(np.arange(K))
    ax.set_yticks(np.arange(T))
    ax.set_xticklabels(algorithm_names, rotation=45, ha='right')
    ax.set_yticklabels(time_labels)
    
    # Labels
    ax.set_xlabel('Algorithms', fontsize=12, fontweight='bold')
    ax.set_ylabel('Time Periods', fontsize=12, fontweight='bold')
    ax.set_title('Performance Evolution Heatmap', fontsize=14, fontweight='bold', pad=20)
    
    # Annotate cells with values
    for i in range(T):
        for j in range(K):
            text = f'{performance_matrix[i, j]:.3f}'
            ax.text(j, i, text, ha='center', va='center', 
                   color='white' if performance_matrix[i, j] > 0.5 else 'black',
                   fontsize=9)
    
    # Add grid
    ax.set_xticks(np.arange(K+1)-.5, minor=True)
    ax.set_yticks(np.arange(T+1)-.5, minor=True)
    ax.grid(which="minor", color="white", linestyle='-', linewidth=2)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    else:
        plt.show()


def plot_constraint_heatmap(constraint_matrix: np.ndarray,
                            constraint_names: Optional[List[str]] = None,
                            time_labels: Optional[List] = None,
                            save_path: Optional[str] = None,
                            figsize: Tuple[int, int] = (10, 6)) -> None:
    """
    Create heatmap of constraints across time.
    
    Highlights hotspots where constraints changed significantly.
    """
    
    if not HAS_MATPLOTLIB:
        raise ImportError("matplotlib required for heatmaps")
    
    T, p = constraint_matrix.shape
    
    if constraint_names is None:
        constraint_names = [f'Constraint{i+1}' for i in range(p)]
    
    if time_labels is None:
        time_labels = [f'T{i+1}' for i in range(T)]
    
    # Normalize constraints for visualization
    constraint_normalized = (constraint_matrix - constraint_matrix.mean(axis=0)) / (constraint_matrix.std(axis=0) + 1e-8)
    
    fig, ax = plt.subplots(figsize=figsize)
    
    # Create heatmap
    im = ax.imshow(constraint_normalized, cmap='coolwarm', aspect='auto', vmin=-2, vmax=2)
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Normalized Value (std from mean)', rotation=270, labelpad=20)
    
    # Set ticks
    ax.set_xticks(np.arange(p))
    ax.set_yticks(np.arange(T))
    ax.set_xticklabels(constraint_names, rotation=45, ha='right')
    ax.set_yticklabels(time_labels)
    
    # Labels
    ax.set_xlabel('Constraints', fontsize=12, fontweight='bold')
    ax.set_ylabel('Time Periods', fontsize=12, fontweight='bold')
    ax.set_title('Constraint Variation Heatmap\n(Red=Above Mean, Blue=Below Mean)', 
                fontsize=14, fontweight='bold', pad=20)
    
    # Annotate cells
    for i in range(T):
        for j in range(p):
            text = f'{constraint_matrix[i, j]:.1f}'
            ax.text(j, i, text, ha='center', va='center', 
                   color='white' if abs(constraint_normalized[i, j]) > 1 else 'black',
                   fontsize=8)
    
    # Add grid
    ax.set_xticks(np.arange(p+1)-.5, minor=True)
    ax.set_yticks(np.arange(T+1)-.5, minor=True)
    ax.grid(which="minor", color="gray", linestyle='-', linewidth=1, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    else:
        plt.show()


def plot_interactive_dashboard(performance_matrix: np.ndarray,
                               constraint_matrix: np.ndarray,
                               results: dict,
                               algorithm_names: Optional[List[str]] = None,
                               save_html: Optional[str] = None) -> None:
    """
    Create interactive Plotly dashboard with hover information.
    
    Parameters:
    -----------
    performance_matrix : np.ndarray
        Shape (T, K)
    constraint_matrix : np.ndarray
        Shape (T, p)
    results : dict
        Detection results from BiasDetector
    algorithm_names : list, optional
        Algorithm names
    save_html : str, optional
        Path to save HTML file
    """
    
    if not HAS_PLOTLY:
        raise ImportError("plotly required for interactive visualizations")
    
    T, K = performance_matrix.shape
    _, p = constraint_matrix.shape
    
    if algorithm_names is None:
        algorithm_names = [f'Algorithm {i+1}' for i in range(K)]
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            'Performance Trajectories',
            'Indicator Scores',
            'Performance Heatmap',
            'Constraint Evolution'
        ),
        specs=[
            [{'type': 'scatter'}, {'type': 'bar'}],
            [{'type': 'heatmap'}, {'type': 'scatter'}]
        ]
    )
    
    # 1. Performance trajectories
    for k, alg_name in enumerate(algorithm_names):
        fig.add_trace(
            go.Scatter(
                x=list(range(1, T+1)),
                y=performance_matrix[:, k],
                mode='lines+markers',
                name=alg_name,
                hovertemplate=f'{alg_name}<br>Time: %{{x}}<br>Performance: %{{y:.4f}}<extra></extra>'
            ),
            row=1, col=1
        )
    
    # 2. Indicator scores with confidence intervals
    indicators = ['PSI', 'CCS', 'ρ_PC']
    scores = [results['psi_score'], results['ccs_score'], abs(results['rho_pc_score'])]
    
    if results.get('bootstrap_enabled', False):
        error_y = [
            results['psi_ci_upper'] - results['psi_score'],
            results['ccs_ci_upper'] - results['ccs_score'],
            abs(results['rho_pc_ci_upper']) - abs(results['rho_pc_score'])
        ]
        error_y_minus = [
            results['psi_score'] - results['psi_ci_lower'],
            results['ccs_score'] - results['ccs_ci_lower'],
            abs(results['rho_pc_score']) - abs(results['rho_pc_ci_lower'])
        ]
    else:
        error_y = None
        error_y_minus = None
    
    colors = ['red' if results.get(f'{ind.lower()}_bias', False) else 'green' 
             for ind in ['psi', 'ccs', 'rho_pc']]
    
    fig.add_trace(
        go.Bar(
            x=indicators,
            y=scores,
            error_y=dict(
                type='data',
                array=error_y,
                arrayminus=error_y_minus,
                visible=True
            ) if error_y else None,
            marker_color=colors,
            hovertemplate='%{x}: %{y:.4f}<extra></extra>'
        ),
        row=1, col=2
    )
    
    # 3. Performance heatmap
    fig.add_trace(
        go.Heatmap(
            z=performance_matrix,
            x=algorithm_names,
            y=[f'T{i+1}' for i in range(T)],
            colorscale='YlOrRd',
            hovertemplate='Algorithm: %{x}<br>Time: %{y}<br>Performance: %{z:.4f}<extra></extra>'
        ),
        row=2, col=1
    )
    
    # 4. Constraint evolution (aggregate)
    constraint_aggregate = constraint_matrix.mean(axis=1)
    
    fig.add_trace(
        go.Scatter(
            x=list(range(1, T+1)),
            y=constraint_aggregate,
            mode='lines+markers',
            name='Avg Constraint',
            line=dict(color='purple', width=3),
            hovertemplate='Time: %{x}<br>Avg Constraint: %{y:.2f}<extra></extra>'
        ),
        row=2, col=2
    )
    
    # Update layout
    fig.update_xaxes(title_text="Time Period", row=1, col=1)
    fig.update_yaxes(title_text="Performance", row=1, col=1)
    
    fig.update_xaxes(title_text="Indicator", row=1, col=2)
    fig.update_yaxes(title_text="Score", row=1, col=2)
    
    fig.update_xaxes(title_text="Algorithm", row=2, col=1)
    fig.update_yaxes(title_text="Time", row=2, col=1)
    
    fig.update_xaxes(title_text="Time Period", row=2, col=2)
    fig.update_yaxes(title_text="Constraint Value", row=2, col=2)
    
    fig.update_layout(
        title_text=f"Circular Bias Detection Dashboard - {'⚠️ BIAS DETECTED' if results['overall_bias'] else '✅ NO BIAS'}",
        showlegend=True,
        height=800,
        hovermode='closest'
    )
    
    if save_html:
        fig.write_html(save_html)
        print(f"✅ Interactive dashboard saved to: {save_html}")
    else:
        fig.show()


def plot_correlation_matrix(performance_matrix: np.ndarray,
                            constraint_matrix: np.ndarray,
                            algorithm_names: Optional[List[str]] = None,
                            constraint_names: Optional[List[str]] = None,
                            save_path: Optional[str] = None) -> None:
    """
    Plot correlation matrix between performance and constraints.
    
    Highlights performance-constraint dependencies.
    """
    
    if not HAS_MATPLOTLIB:
        raise ImportError("matplotlib required")
    
    T, K = performance_matrix.shape
    _, p = constraint_matrix.shape
    
    if algorithm_names is None:
        algorithm_names = [f'Perf_Alg{i+1}' for i in range(K)]
    
    if constraint_names is None:
        constraint_names = [f'Const{i+1}' for i in range(p)]
    
    # Aggregate performance and constraints
    perf_mean = performance_matrix.mean(axis=1)
    
    # Combine into DataFrame
    data = np.column_stack([perf_mean, constraint_matrix])
    df = pd.DataFrame(data, columns=['Avg_Performance'] + constraint_names)
    
    # Compute correlation
    corr_matrix = df.corr()
    
    # Plot
    fig, ax = plt.subplots(figsize=(8, 6))
    
    sns.heatmap(corr_matrix, annot=True, fmt='.3f', cmap='coolwarm',
                center=0, vmin=-1, vmax=1,
                square=True, linewidths=1, cbar_kws={"shrink": 0.8},
                ax=ax)
    
    ax.set_title('Performance-Constraint Correlation Matrix\n(Red=Positive, Blue=Negative)',
                fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    else:
        plt.show()


def plot_time_series_with_ci(performance_matrix: np.ndarray,
                             results: dict,
                             algorithm_names: Optional[List[str]] = None,
                             save_path: Optional[str] = None) -> None:
    """
    Plot performance time series with bootstrap confidence intervals.
    
    Only works if bootstrap results are available.
    """
    
    if not HAS_MATPLOTLIB:
        raise ImportError("matplotlib required")
    
    if not results.get('bootstrap_enabled', False):
        warnings.warn("Bootstrap not enabled - confidence intervals unavailable")
        return
    
    T, K = performance_matrix.shape
    
    if algorithm_names is None:
        algorithm_names = [f'Algorithm {i+1}' for i in range(K)]
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    time_points = np.arange(1, T+1)
    
    # Plot each algorithm
    for k, alg_name in enumerate(algorithm_names):
        ax.plot(time_points, performance_matrix[:, k], 
               marker='o', label=alg_name, linewidth=2)
    
    # Add statistical annotation
    psi_pval = results.get('psi_pvalue', None)
    rho_pval = results.get('rho_pc_pvalue', None)
    
    annotation_text = f"PSI p-value: {psi_pval:.3f}\nρ_PC p-value: {rho_pval:.3f}"
    
    ax.text(0.02, 0.98, annotation_text,
           transform=ax.transAxes,
           verticalalignment='top',
           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
           fontsize=10)
    
    ax.set_xlabel('Time Period', fontsize=12, fontweight='bold')
    ax.set_ylabel('Performance', fontsize=12, fontweight='bold')
    ax.set_title('Performance Trajectories with Statistical Annotations',
                fontsize=14, fontweight='bold')
    ax.legend(loc='best')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    else:
        plt.show()
