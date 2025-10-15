"""
CCS (Constraint-Consistency Score) Calculator

Measures the consistency of constraint specifications across evaluations.
Low variance in constraints indicates consistent evaluation conditions.

Formula:
    CCS = 1 - (1/p) Σⱼ₌₁ᵖ CV(cⱼ)

where:
    CV(cⱼ) = coefficient of variation for constraint j
           = σⱼ / μⱼ (std dev / mean)
    p = number of constraint columns

High CCS indicates:
    - Constraints remained consistent across evaluations
    - Evaluation conditions were stable
    - Low risk of circular bias

Low CCS indicates:
    - Constraints varied significantly
    - Evaluation conditions changed
    - Potential protocol manipulation
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple


def compute_ccs(data: pd.DataFrame) -> Dict:
    """
    Compute CCS score for evaluation data.
    
    Args:
        data: DataFrame with columns:
            - time_period: Sequential evaluation period
            - algorithm: Algorithm identifier
            - performance: Performance score
            - constraint_*: Constraint columns
    
    Returns:
        Dictionary containing:
            - ccs_score: Overall CCS value [0, 1]
            - cv_by_constraint: Coefficient of variation per constraint
            - constraint_stats: Mean and std for each constraint
            - interpretation: String interpretation
    
    Example:
        >>> df = pd.DataFrame({
        ...     'time_period': [1, 1, 2, 2],
        ...     'algorithm': ['A', 'B', 'A', 'B'],
        ...     'performance': [0.7, 0.6, 0.72, 0.65],
        ...     'constraint_compute': [100, 100, 100, 100]  # Consistent
        ... })
        >>> result = compute_ccs(df)
        >>> print(result['ccs_score'])  # Should be high (near 1.0)
    """
    
    # Validate input
    required_cols = ['time_period', 'algorithm', 'performance']
    for col in required_cols:
        if col not in data.columns:
            raise ValueError(f"Missing required column: {col}")
    
    # Get constraint columns
    constraint_cols = [col for col in data.columns if col.startswith('constraint_')]
    
    if not constraint_cols:
        raise ValueError("No constraint columns found. CCS requires at least one constraint column.")
    
    # Compute coefficient of variation for each constraint
    cv_values = {}
    constraint_stats = {}
    
    for col in constraint_cols:
        values = data[col].dropna()
        
        if len(values) == 0:
            continue
        
        mean_val = values.mean()
        std_val = values.std()
        
        constraint_stats[col] = {
            'mean': float(mean_val),
            'std': float(std_val),
            'min': float(values.min()),
            'max': float(values.max())
        }
        
        # Coefficient of Variation (CV)
        if mean_val != 0:
            cv = std_val / abs(mean_val)
        else:
            cv = 0.0 if std_val == 0 else float('inf')
        
        cv_values[col] = float(cv)
    
    # CCS = 1 - average CV
    if cv_values:
        avg_cv = np.mean(list(cv_values.values()))
        ccs_score = max(0.0, 1.0 - avg_cv)  # Ensure [0, 1] range
    else:
        ccs_score = 0.0
        avg_cv = 0.0
    
    # Interpretation
    interpretation = _interpret_ccs(ccs_score, len(constraint_cols), cv_values)
    
    return {
        'ccs_score': float(ccs_score),
        'avg_cv': float(avg_cv),
        'cv_by_constraint': cv_values,
        'constraint_stats': constraint_stats,
        'num_constraints': len(constraint_cols),
        'interpretation': interpretation,
        'threshold': 0.85,  # Default threshold
        'exceeds_threshold': ccs_score >= 0.85
    }


def _interpret_ccs(ccs_score: float, num_constraints: int, cv_values: Dict) -> str:
    """
    Generate human-readable interpretation of CCS score.
    
    Args:
        ccs_score: Computed CCS value
        num_constraints: Number of constraints analyzed
        cv_values: CV for each constraint
    
    Returns:
        Interpretation string
    """
    if ccs_score >= 0.90:
        level = "highly consistent"
        risk = "low"
        verdict = "Constraints show excellent stability across evaluations."
    elif ccs_score >= 0.85:
        level = "moderately consistent"
        risk = "moderate"
        verdict = "Constraints show acceptable consistency with minor variations."
    elif ccs_score >= 0.70:
        level = "inconsistent"
        risk = "high"
        verdict = "Constraints show significant variations, suggesting protocol changes."
    else:
        level = "highly inconsistent"
        risk = "very high"
        verdict = "Constraints show severe instability, strong indication of manipulation."
    
    # Identify most variable constraint
    if cv_values:
        most_variable = max(cv_values.items(), key=lambda x: x[1])
        most_stable = min(cv_values.items(), key=lambda x: x[1])
        
        detail = (f"\nMost variable: {most_variable[0]} (CV={most_variable[1]:.4f}). "
                 f"Most stable: {most_stable[0]} (CV={most_stable[1]:.4f}).")
    else:
        detail = ""
    
    return (
        f"CCS = {ccs_score:.4f} indicates {level} constraints ({risk} risk). "
        f"{verdict} "
        f"Analyzed {num_constraints} constraint(s).{detail}"
    )


def compute_ccs_by_period(data: pd.DataFrame) -> Dict:
    """
    Compute CCS for each time period separately.
    
    This detects if constraint consistency changed over time.
    
    Args:
        data: Same format as compute_ccs()
    
    Returns:
        Dictionary mapping time periods to their CCS results
    """
    periods = sorted(data['time_period'].unique())
    results = {}
    
    for period in periods:
        period_data = data[data['time_period'] == period].copy()
        try:
            results[period] = compute_ccs(period_data)
        except ValueError as e:
            results[period] = {'error': str(e)}
    
    return results


def detect_constraint_outliers(data: pd.DataFrame, z_threshold: float = 2.0) -> Dict:
    """
    Detect outlier constraint values that deviate significantly from mean.
    
    Uses Z-score to identify anomalous constraint specifications.
    
    Args:
        data: Evaluation data
        z_threshold: Z-score threshold (default 2.0 = 2 std devs)
    
    Returns:
        Dictionary with outlier information per constraint
    """
    constraint_cols = [col for col in data.columns if col.startswith('constraint_')]
    outliers = {}
    
    for col in constraint_cols:
        values = data[col].dropna()
        
        if len(values) < 3:
            continue
        
        mean = values.mean()
        std = values.std()
        
        if std == 0:
            continue
        
        # Compute Z-scores
        z_scores = np.abs((values - mean) / std)
        outlier_mask = z_scores > z_threshold
        
        if outlier_mask.any():
            outlier_indices = data[outlier_mask].index.tolist()
            outlier_values = values[outlier_mask].tolist()
            outlier_z_scores = z_scores[outlier_mask].tolist()
            
            outliers[col] = {
                'count': int(outlier_mask.sum()),
                'indices': outlier_indices,
                'values': outlier_values,
                'z_scores': outlier_z_scores,
                'mean': float(mean),
                'std': float(std)
            }
    
    return outliers


def normalize_ccs(ccs_score: float) -> float:
    """
    Normalize CCS score to [0, 1] range for CBS calculation.
    
    CCS is already in [0, 1], but this ensures bounds.
    
    Args:
        ccs_score: Raw CCS value
    
    Returns:
        Normalized score in [0, 1]
    """
    return max(0.0, min(ccs_score, 1.0))


# Example usage
if __name__ == "__main__":
    # Example data: stable vs unstable constraints
    
    print("=" * 70)
    print("CCS Calculator - Test Run")
    print("=" * 70)
    
    # Case 1: Stable constraints (high CCS expected)
    print("\n📊 Case 1: Stable Constraints")
    stable_data = pd.DataFrame({
        'time_period': [1, 1, 2, 2, 3, 3],
        'algorithm': ['A', 'B', 'A', 'B', 'A', 'B'],
        'performance': [0.7, 0.6, 0.72, 0.65, 0.74, 0.67],
        'constraint_compute': [100, 150, 100, 150, 100, 150],  # Consistent
        'constraint_memory': [8.0, 12.0, 8.0, 12.0, 8.0, 12.0]  # Consistent
    })
    
    result = compute_ccs(stable_data)
    print(f"CCS Score: {result['ccs_score']:.4f}")
    print(f"Status: {'✓ Consistent' if result['exceeds_threshold'] else '⚠️ Inconsistent'}")
    print(f"\nInterpretation:")
    print(result['interpretation'])
    
    # Case 2: Unstable constraints (low CCS expected)
    print("\n" + "=" * 70)
    print("📊 Case 2: Unstable Constraints")
    unstable_data = pd.DataFrame({
        'time_period': [1, 1, 2, 2, 3, 3],
        'algorithm': ['A', 'B', 'A', 'B', 'A', 'B'],
        'performance': [0.7, 0.6, 0.72, 0.65, 0.74, 0.67],
        'constraint_compute': [100, 150, 200, 250, 300, 350],  # Increasing
        'constraint_memory': [8.0, 12.0, 16.0, 20.0, 24.0, 28.0]  # Increasing
    })
    
    result = compute_ccs(unstable_data)
    print(f"CCS Score: {result['ccs_score']:.4f}")
    print(f"Status: {'✓ Consistent' if result['exceeds_threshold'] else '⚠️ Inconsistent'}")
    print(f"\nInterpretation:")
    print(result['interpretation'])
    
    print("\n" + "=" * 70)
    print("CV Values by Constraint:")
    for constraint, cv in result['cv_by_constraint'].items():
        print(f"  {constraint}: CV = {cv:.4f}")
    
    # Outlier detection
    print("\n" + "=" * 70)
    print("Outlier Detection:")
    outliers = detect_constraint_outliers(unstable_data)
    if outliers:
        for constraint, info in outliers.items():
            print(f"\n{constraint}:")
            print(f"  Outliers found: {info['count']}")
            print(f"  Values: {info['values']}")
    else:
        print("No outliers detected (with Z-threshold=2.0)")
