"""
ρ_PC (Performance-Constraint Correlation) Calculator

Measures the correlation between performance scores and constraint values.
Strong correlation indicates constraints may have been adjusted based on performance.

Formula:
    ρ_PC = Pearson(P, C̄)

where:
    P = performance vector
    C̄ = mean constraint vector (average across all constraints)
    Pearson = Pearson correlation coefficient

High |ρ_PC| indicates:
    - Performance and constraints are correlated
    - Constraints may have been tuned for better results
    - Potential circular reasoning bias

Positive ρ_PC:
    - Higher performance → More resources
    - Could indicate: resources increased to improve scores

Negative ρ_PC:
    - Higher performance → Fewer resources
    - Strong red flag: suggests cherry-picking test conditions
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
from scipy.stats import pearsonr, spearmanr


def compute_rho_pc(data: pd.DataFrame) -> Dict:
    """
    Compute ρ_PC score for evaluation data.
    
    Args:
        data: DataFrame with columns:
            - time_period: Sequential evaluation period
            - algorithm: Algorithm identifier
            - performance: Performance score
            - constraint_*: Constraint columns
    
    Returns:
        Dictionary containing:
            - rho_pc: Pearson correlation coefficient [-1, 1]
            - p_value: Statistical significance (two-tailed)
            - spearman_rho: Spearman rank correlation (robust to outliers)
            - constraint_correlations: Individual correlation per constraint
            - interpretation: String interpretation
    
    Example:
        >>> df = pd.DataFrame({
        ...     'performance': [0.6, 0.7, 0.8, 0.9],
        ...     'constraint_compute': [100, 150, 200, 250]  # Positive correlation
        ... })
        >>> result = compute_rho_pc(df)
        >>> print(result['rho_pc'])  # Should be high positive
    """
    
    # Validate input
    required_cols = ['time_period', 'algorithm', 'performance']
    for col in required_cols:
        if col not in data.columns:
            raise ValueError(f"Missing required column: {col}")
    
    # Get constraint columns
    constraint_cols = [col for col in data.columns if col.startswith('constraint_')]
    
    if not constraint_cols:
        raise ValueError("No constraint columns found. ρ_PC requires at least one constraint column.")
    
    # Extract performance values
    performance = data['performance'].values
    
    if len(performance) < 3:
        return {
            'rho_pc': 0.0,
            'p_value': 1.0,
            'spearman_rho': 0.0,
            'constraint_correlations': {},
            'interpretation': 'Insufficient data points for correlation (need ≥3)',
            'warning': 'At least 3 data points required',
            'threshold': 0.5,
            'exceeds_threshold': False
        }
    
    # Compute mean constraint value for each data point
    mean_constraints = data[constraint_cols].mean(axis=1).values
    
    # Pearson correlation
    rho_pc, p_value = pearsonr(performance, mean_constraints)
    
    # Spearman rank correlation (more robust to outliers)
    spearman_rho, spearman_p = spearmanr(performance, mean_constraints)
    
    # Compute correlation for each individual constraint
    constraint_correlations = {}
    for col in constraint_cols:
        constraint_values = data[col].dropna().values
        if len(constraint_values) >= 3:
            perf_subset = data.loc[data[col].notna(), 'performance'].values
            corr, p_val = pearsonr(perf_subset, constraint_values)
            constraint_correlations[col] = {
                'correlation': float(corr),
                'p_value': float(p_val),
                'significant': p_val < 0.05
            }
    
    # Interpretation
    interpretation = _interpret_rho_pc(rho_pc, p_value, spearman_rho, len(performance))
    
    return {
        'rho_pc': float(rho_pc),
        'p_value': float(p_value),
        'spearman_rho': float(spearman_rho),
        'spearman_p_value': float(spearman_p),
        'constraint_correlations': constraint_correlations,
        'num_data_points': len(performance),
        'num_constraints': len(constraint_cols),
        'interpretation': interpretation,
        'threshold': 0.5,  # Default threshold
        'exceeds_threshold': abs(rho_pc) >= 0.5,
        'significant': p_value < 0.05
    }


def _interpret_rho_pc(rho_pc: float, p_value: float, spearman_rho: float, n: int) -> str:
    """
    Generate human-readable interpretation of ρ_PC score.
    
    Args:
        rho_pc: Pearson correlation
        p_value: Statistical significance
        spearman_rho: Spearman rank correlation
        n: Number of data points
    
    Returns:
        Interpretation string
    """
    abs_rho = abs(rho_pc)
    
    # Significance check
    if p_value >= 0.05:
        sig_note = f" (not statistically significant, p={p_value:.3f})"
        risk = "uncertain"
    else:
        sig_note = f" (statistically significant, p={p_value:.3f})"
        
        if abs_rho < 0.3:
            risk = "low"
        elif abs_rho < 0.5:
            risk = "moderate"
        elif abs_rho < 0.7:
            risk = "high"
        else:
            risk = "very high"
    
    # Direction interpretation
    if rho_pc > 0.5:
        direction = "strong positive"
        meaning = "Performance increases as constraints loosen (more resources → better scores)."
        flag = "⚠️ May indicate resources were increased to improve performance."
    elif rho_pc > 0.3:
        direction = "moderate positive"
        meaning = "Performance tends to increase with more resources."
        flag = "Could be natural or indicate optimization bias."
    elif rho_pc > -0.3:
        direction = "weak"
        meaning = "Performance and constraints show little relationship."
        flag = "✓ Good: constraints appear independent of performance."
    elif rho_pc > -0.5:
        direction = "moderate negative"
        meaning = "Performance increases as constraints tighten."
        flag = "🚩 Unusual pattern, investigate evaluation protocol."
    else:
        direction = "strong negative"
        meaning = "Performance strongly increases with fewer resources."
        flag = "🚨 RED FLAG: Likely cherry-picking or protocol gaming."
    
    # Robustness check
    if abs(rho_pc - spearman_rho) > 0.2:
        robust_note = f"\n⚠️ Large difference between Pearson ({rho_pc:.3f}) and Spearman ({spearman_rho:.3f}) suggests outliers or non-linear relationship."
    else:
        robust_note = ""
    
    return (
        f"ρ_PC = {rho_pc:.4f} indicates {direction} correlation ({risk} risk){sig_note}. "
        f"{meaning} {flag} "
        f"Analyzed {n} data points.{robust_note}"
    )


def compute_rho_pc_by_algorithm(data: pd.DataFrame) -> Dict:
    """
    Compute ρ_PC separately for each algorithm.
    
    Detects if specific algorithms had their constraints adjusted
    differently than others.
    
    Args:
        data: Same format as compute_rho_pc()
    
    Returns:
        Dictionary mapping algorithm names to their ρ_PC results
    """
    algorithms = data['algorithm'].unique()
    results = {}
    
    for algo in algorithms:
        algo_data = data[data['algorithm'] == algo].copy()
        try:
            results[algo] = compute_rho_pc(algo_data)
        except ValueError as e:
            results[algo] = {'error': str(e)}
    
    return results


def compute_partial_correlations(data: pd.DataFrame) -> Dict:
    """
    Compute partial correlations controlling for time_period.
    
    This removes the confounding effect of temporal trends.
    
    Args:
        data: Evaluation data
    
    Returns:
        Dictionary with partial correlation results
    """
    from scipy.stats import pearsonr
    
    constraint_cols = [col for col in data.columns if col.startswith('constraint_')]
    
    if not constraint_cols or 'performance' not in data.columns or 'time_period' not in data.columns:
        return {'error': 'Missing required columns'}
    
    # Simple partial correlation: residualize both variables by time
    performance = data['performance'].values
    time_period = data['time_period'].values
    mean_constraints = data[constraint_cols].mean(axis=1).values
    
    # Remove linear trend with time
    from numpy.polynomial import Polynomial
    
    # Fit linear models
    p_model = Polynomial.fit(time_period, performance, deg=1)
    c_model = Polynomial.fit(time_period, mean_constraints, deg=1)
    
    # Compute residuals
    perf_residuals = performance - p_model(time_period)
    const_residuals = mean_constraints - c_model(time_period)
    
    # Correlation of residuals = partial correlation
    if len(perf_residuals) >= 3:
        partial_rho, partial_p = pearsonr(perf_residuals, const_residuals)
    else:
        partial_rho, partial_p = 0.0, 1.0
    
    return {
        'partial_rho_pc': float(partial_rho),
        'partial_p_value': float(partial_p),
        'interpretation': f"Partial correlation (controlling for time) = {partial_rho:.4f}"
    }


def normalize_rho_pc(rho_pc: float) -> float:
    """
    Normalize ρ_PC to [0, 1] range for CBS calculation.
    
    Uses absolute value since both positive and negative
    correlations indicate potential bias.
    
    Args:
        rho_pc: Raw ρ_PC value in [-1, 1]
    
    Returns:
        Normalized score in [0, 1]
    """
    return abs(rho_pc)


# Example usage
if __name__ == "__main__":
    print("=" * 70)
    print("ρ_PC Calculator - Test Run")
    print("=" * 70)
    
    # Case 1: Strong positive correlation (red flag)
    print("\n📊 Case 1: Strong Positive Correlation")
    positive_data = pd.DataFrame({
        'time_period': [1, 1, 2, 2, 3, 3, 4, 4],
        'algorithm': ['A', 'B'] * 4,
        'performance': [0.6, 0.55, 0.7, 0.65, 0.8, 0.75, 0.9, 0.85],
        'constraint_compute': [100, 90, 150, 140, 200, 190, 250, 240],
        'constraint_memory': [8, 7, 12, 11, 16, 15, 20, 19]
    })
    
    result = compute_rho_pc(positive_data)
    print(f"ρ_PC: {result['rho_pc']:.4f}")
    print(f"P-value: {result['p_value']:.4f}")
    print(f"Status: {'⚠️ HIGH CORRELATION' if result['exceeds_threshold'] else '✓ Low correlation'}")
    print(f"\nInterpretation:")
    print(result['interpretation'])
    
    # Case 2: Weak correlation (good)
    print("\n" + "=" * 70)
    print("📊 Case 2: Weak Correlation (Good)")
    weak_data = pd.DataFrame({
        'time_period': [1, 1, 2, 2, 3, 3, 4, 4],
        'algorithm': ['A', 'B'] * 4,
        'performance': [0.6, 0.7, 0.65, 0.75, 0.8, 0.7, 0.75, 0.85],  # Variable
        'constraint_compute': [100, 100, 100, 100, 100, 100, 100, 100],  # Constant
        'constraint_memory': [8, 8, 8, 8, 8, 8, 8, 8]  # Constant
    })
    
    result = compute_rho_pc(weak_data)
    print(f"ρ_PC: {result['rho_pc']:.4f}")
    print(f"P-value: {result['p_value']:.4f}")
    print(f"Status: {'⚠️ HIGH CORRELATION' if result['exceeds_threshold'] else '✓ Low correlation'}")
    print(f"\nInterpretation:")
    print(result['interpretation'])
    
    # Case 3: Strong negative correlation (major red flag)
    print("\n" + "=" * 70)
    print("📊 Case 3: Strong Negative Correlation (RED FLAG)")
    negative_data = pd.DataFrame({
        'time_period': [1, 1, 2, 2, 3, 3, 4, 4],
        'algorithm': ['A', 'B'] * 4,
        'performance': [0.6, 0.55, 0.7, 0.65, 0.8, 0.75, 0.9, 0.85],  # Increasing
        'constraint_compute': [250, 240, 200, 190, 150, 140, 100, 90],  # Decreasing!
        'constraint_memory': [20, 19, 16, 15, 12, 11, 8, 7]  # Decreasing!
    })
    
    result = compute_rho_pc(negative_data)
    print(f"ρ_PC: {result['rho_pc']:.4f}")
    print(f"P-value: {result['p_value']:.4f}")
    print(f"Status: {'🚨 HIGH CORRELATION' if result['exceeds_threshold'] else '✓ Low correlation'}")
    print(f"\nInterpretation:")
    print(result['interpretation'])
    
    # Per-algorithm analysis
    print("\n" + "=" * 70)
    print("Per-Algorithm ρ_PC:")
    per_algo = compute_rho_pc_by_algorithm(positive_data)
    for algo, res in per_algo.items():
        if 'error' in res:
            print(f"\n{algo}: ✗ {res['error']}")
        else:
            print(f"\n{algo}: ρ_PC = {res['rho_pc']:.4f} (p={res['p_value']:.3f})")
