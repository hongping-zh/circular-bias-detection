"""
PSI (Performance-Structure Independence) Calculator

Measures parameter stability over time by computing the L2 distance
between parameter vectors in consecutive time periods.

Formula:
    PSI = (1/T) Σᵢ₌₁ᵀ ||θᵢ - θᵢ₋₁||₂

where:
    θᵢ = parameter vector at time period i
    T = total number of time periods
    ||·||₂ = L2 norm (Euclidean distance)

High PSI indicates:
    - Parameters were adjusted between evaluations
    - Iterative tuning based on preliminary results
    - Potential circular reasoning bias
"""

import numpy as np
import pandas as pd
from typing import Tuple, List, Dict
from scipy.spatial.distance import euclidean


def compute_psi(data: pd.DataFrame) -> Dict:
    """
    Compute PSI score for evaluation data.
    
    Args:
        data: DataFrame with columns:
            - time_period: Sequential evaluation period (1, 2, 3, ...)
            - algorithm: Algorithm identifier
            - performance: Performance score [0, 1]
            - constraint_*: Constraint columns (e.g., constraint_compute)
    
    Returns:
        Dictionary containing:
            - psi_score: Overall PSI value
            - psi_by_period: List of distances between consecutive periods
            - parameter_vectors: List of parameter vectors per period
            - interpretation: String interpretation
    
    Example:
        >>> df = pd.DataFrame({
        ...     'time_period': [1, 1, 2, 2],
        ...     'algorithm': ['A', 'B', 'A', 'B'],
        ...     'performance': [0.7, 0.6, 0.72, 0.65],
        ...     'constraint_compute': [100, 150, 105, 155]
        ... })
        >>> result = compute_psi(df)
        >>> print(result['psi_score'])
    """
    
    # Validate input
    required_cols = ['time_period', 'algorithm', 'performance']
    for col in required_cols:
        if col not in data.columns:
            raise ValueError(f"Missing required column: {col}")
    
    # Get constraint columns (parameters)
    constraint_cols = [col for col in data.columns if col.startswith('constraint_')]
    
    if not constraint_cols:
        raise ValueError("No constraint columns found. PSI requires at least one constraint column.")
    
    # Sort by time period
    data = data.sort_values('time_period').reset_index(drop=True)
    periods = sorted(data['time_period'].unique())
    
    if len(periods) < 2:
        return {
            'psi_score': 0.0,
            'psi_by_period': [],
            'parameter_vectors': [],
            'interpretation': 'Insufficient time periods for PSI calculation (need ≥2)',
            'warning': 'At least 2 time periods required'
        }
    
    # Extract parameter vectors for each period
    parameter_vectors = []
    for period in periods:
        period_data = data[data['time_period'] == period]
        
        # Aggregate constraint values (mean across algorithms in this period)
        param_vector = period_data[constraint_cols].mean().values
        parameter_vectors.append(param_vector)
    
    # Compute L2 distances between consecutive periods
    distances = []
    for i in range(1, len(parameter_vectors)):
        dist = euclidean(parameter_vectors[i], parameter_vectors[i-1])
        distances.append(dist)
    
    # PSI = average distance
    psi_score = np.mean(distances) if distances else 0.0
    
    # Interpretation
    interpretation = _interpret_psi(psi_score, len(periods))
    
    return {
        'psi_score': float(psi_score),
        'psi_by_period': [float(d) for d in distances],
        'parameter_vectors': [vec.tolist() for vec in parameter_vectors],
        'num_periods': len(periods),
        'num_constraints': len(constraint_cols),
        'interpretation': interpretation,
        'threshold': 0.15,  # Default threshold
        'exceeds_threshold': psi_score >= 0.15
    }


def _interpret_psi(psi_score: float, num_periods: int) -> str:
    """
    Generate human-readable interpretation of PSI score.
    
    Args:
        psi_score: Computed PSI value
        num_periods: Number of time periods analyzed
    
    Returns:
        Interpretation string
    """
    if psi_score < 0.10:
        level = "very stable"
        risk = "low"
        verdict = "Parameters show excellent stability across time periods."
    elif psi_score < 0.15:
        level = "moderately stable"
        risk = "moderate"
        verdict = "Parameters show acceptable stability with minor variations."
    elif psi_score < 0.25:
        level = "unstable"
        risk = "high"
        verdict = "Parameters show significant drift, suggesting iterative tuning."
    else:
        level = "highly unstable"
        risk = "very high"
        verdict = "Parameters show severe instability, strong indication of circular bias."
    
    return (
        f"PSI = {psi_score:.4f} indicates {level} parameters ({risk} risk). "
        f"{verdict} "
        f"Analyzed {num_periods} time periods."
    )


def compute_psi_per_algorithm(data: pd.DataFrame) -> Dict:
    """
    Compute PSI separately for each algorithm.
    
    This allows detecting if specific algorithms had their parameters
    adjusted more than others.
    
    Args:
        data: Same format as compute_psi()
    
    Returns:
        Dictionary mapping algorithm names to their PSI results
    """
    algorithms = data['algorithm'].unique()
    results = {}
    
    for algo in algorithms:
        algo_data = data[data['algorithm'] == algo].copy()
        try:
            results[algo] = compute_psi(algo_data)
        except ValueError as e:
            results[algo] = {'error': str(e)}
    
    return results


def normalize_psi(psi_score: float, max_distance: float = 1.0) -> float:
    """
    Normalize PSI score to [0, 1] range for CBS calculation.
    
    Args:
        psi_score: Raw PSI value
        max_distance: Maximum expected distance (for normalization)
    
    Returns:
        Normalized score in [0, 1]
    """
    return min(psi_score / max_distance, 1.0)


# Example usage
if __name__ == "__main__":
    # Example data: 3 algorithms evaluated over 4 time periods
    sample_data = pd.DataFrame({
        'time_period': [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4],
        'algorithm': ['ResNet', 'VGG', 'DenseNet'] * 4,
        'performance': [0.72, 0.68, 0.75, 0.74, 0.70, 0.77, 0.76, 0.72, 0.79, 0.78, 0.74, 0.81],
        'constraint_compute': [300, 450, 280, 305, 455, 285, 310, 460, 290, 315, 465, 295],
        'constraint_memory': [8.0, 12.0, 9.0, 8.2, 12.1, 9.1, 8.5, 12.3, 9.3, 8.7, 12.5, 9.5]
    })
    
    print("=" * 60)
    print("PSI Calculator - Test Run")
    print("=" * 60)
    
    result = compute_psi(sample_data)
    
    print(f"\nPSI Score: {result['psi_score']:.4f}")
    print(f"Threshold: {result['threshold']}")
    print(f"Exceeds Threshold: {result['exceeds_threshold']}")
    print(f"\nInterpretation:")
    print(result['interpretation'])
    
    print(f"\nPer-Period Distances:")
    for i, dist in enumerate(result['psi_by_period'], 1):
        print(f"  Period {i} → {i+1}: {dist:.4f}")
    
    print("\n" + "=" * 60)
    print("Per-Algorithm PSI")
    print("=" * 60)
    
    per_algo = compute_psi_per_algorithm(sample_data)
    for algo, res in per_algo.items():
        if 'error' in res:
            print(f"\n{algo}: {res['error']}")
        else:
            print(f"\n{algo}: PSI = {res['psi_score']:.4f}")
