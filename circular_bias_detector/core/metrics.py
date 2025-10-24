"""
Core metrics computation for circular bias detection.

This module implements the three main indicators:
- PSI (Performance-Structure Independence)
- CCS (Constraint-Consistency Score)  
- ρ_PC (Performance-Constraint Correlation)
"""

import numpy as np
from scipy import stats
from typing import Optional, Dict
import warnings


def compute_psi(performance_matrix: np.ndarray, 
                algorithm_params: Optional[np.ndarray] = None) -> float:
    """
    Compute Performance-Structure Independence (PSI) score.
    
    PSI measures parameter stability across evaluation periods by computing
    the average parameter difference between consecutive time steps.
    
    Parameters
    ----------
    performance_matrix : np.ndarray
        Shape (T, K) where T is time periods, K is algorithms
    algorithm_params : np.ndarray, optional
        Shape (T, K, p) where p is parameter dimensions
        If None, uses performance as proxy for parameters
        
    Returns
    -------
    float
        PSI score (higher values indicate more instability/bias)
        
    Examples
    --------
    >>> perf_matrix = np.array([[0.8, 0.75], [0.82, 0.78], [0.79, 0.77]])
    >>> psi = compute_psi(perf_matrix)
    >>> print(f"PSI: {psi:.4f}")
    """
    if algorithm_params is None:
        # Use performance matrix as parameter proxy
        theta_matrix = performance_matrix
    else:
        # Average across parameter dimensions
        theta_matrix = np.mean(algorithm_params, axis=2)
    
    T, K = theta_matrix.shape
    
    if T < 2:
        warnings.warn("PSI requires at least 2 time periods")
        return 0.0
    
    psi_scores = []
    
    for k in range(K):
        # Compute parameter differences across time
        param_series = theta_matrix[:, k]
        differences = np.diff(param_series)
        
        # L2 norm of differences (as in paper)
        psi_k = np.mean(np.abs(differences))
        psi_scores.append(psi_k)
    
    # Average across algorithms
    return float(np.mean(psi_scores))


def compute_ccs(constraint_matrix: np.ndarray) -> float:
    """
    Compute Constraint-Consistency Score (CCS).
    
    CCS measures the consistency of constraint specifications across
    evaluation periods using coefficient of variation.
    
    Parameters
    ----------
    constraint_matrix : np.ndarray
        Shape (T, p) where T is time periods, p is constraint types
        
    Returns
    -------
    float
        CCS score (higher values indicate more consistency, range [0, 1])
        
    Examples
    --------
    >>> const_matrix = np.array([[0.7, 100], [0.7, 100], [0.7, 100]])
    >>> ccs = compute_ccs(const_matrix)
    >>> print(f"CCS: {ccs:.4f}")  # Should be close to 1.0 (perfect consistency)
    """
    T, p = constraint_matrix.shape
    
    if T < 2:
        warnings.warn("CCS requires at least 2 time periods")
        return 1.0
    
    consistency_scores = []
    
    for j in range(p):
        constraint_series = constraint_matrix[:, j]
        
        # Handle constant constraints
        if np.std(constraint_series) == 0:
            consistency_scores.append(1.0)
            continue
            
        # Coefficient of variation
        mean_val = np.mean(constraint_series)
        
        if mean_val == 0:
            warnings.warn(f"Zero mean constraint detected for constraint {j}")
            consistency_scores.append(0.0)
            continue
            
        cv = np.std(constraint_series) / np.abs(mean_val)
        
        # Transform to consistency score (lower CV = higher consistency)
        consistency_j = 1 / (1 + cv)
        consistency_scores.append(consistency_j)
    
    # Average across constraint types
    return float(np.mean(consistency_scores))


def compute_rho_pc(performance_matrix: np.ndarray, 
                   constraint_matrix: np.ndarray) -> float:
    """
    Compute Performance-Constraint correlation coefficient (ρ_PC).
    
    ρ_PC measures the correlation between performance trajectories
    and constraint specification changes.
    
    Parameters
    ----------
    performance_matrix : np.ndarray
        Shape (T, K) where T is time periods, K is algorithms
    constraint_matrix : np.ndarray
        Shape (T, p) where T is time periods, p is constraint types
        
    Returns
    -------
    float
        ρ_PC correlation coefficient (-1 to 1)
        
    Raises
    ------
    ValueError
        If matrices have incompatible time dimensions
        
    Examples
    --------
    >>> perf_matrix = np.array([[0.8, 0.75], [0.82, 0.78], [0.79, 0.77]])
    >>> const_matrix = np.array([[0.7, 100], [0.75, 120], [0.72, 110]])
    >>> rho = compute_rho_pc(perf_matrix, const_matrix)
    >>> print(f"ρ_PC: {rho:.4f}")
    """
    T, K = performance_matrix.shape
    T_c, p = constraint_matrix.shape
    
    if T != T_c:
        raise ValueError(
            f"Performance and constraint matrices must have same time dimension. "
            f"Got T={T} and T_c={T_c}"
        )
    
    if T < 3:
        warnings.warn("ρ_PC requires at least 3 time periods for reliable correlation")
        return 0.0
    
    # Aggregate performance across algorithms (mean)
    perf_trajectory = np.mean(performance_matrix, axis=1)
    
    # Aggregate constraints (weighted by variance to emphasize changing constraints)
    constraint_weights = np.var(constraint_matrix, axis=0)
    
    # Handle case where all constraints are constant (all weights are zero)
    weight_sum = np.sum(constraint_weights)
    if weight_sum < 1e-10:
        # All constraints are constant, use equal weights
        constraint_trajectory = np.mean(constraint_matrix, axis=1)
    else:
        # Normalize weights and compute weighted average
        constraint_weights = constraint_weights / weight_sum
        constraint_trajectory = np.average(constraint_matrix, axis=1, weights=constraint_weights)
    
    # Compute Pearson correlation
    try:
        correlation, p_value = stats.pearsonr(perf_trajectory, constraint_trajectory)
        
        # Handle NaN correlations
        if np.isnan(correlation):
            return 0.0
            
        return float(correlation)
        
    except Exception as e:
        warnings.warn(f"Error computing correlation: {e}")
        return 0.0


def detect_bias_threshold(psi_score: float, 
                         ccs_score: float, 
                         rho_pc_score: float,
                         psi_threshold: float = 0.1,
                         ccs_threshold: float = 0.8,
                         rho_pc_threshold: float = 0.3) -> Dict:
    """
    Apply threshold-based bias detection using all three indicators.
    
    Uses a majority voting scheme: bias is detected if at least 2 out of 3
    indicators exceed their thresholds.
    
    Parameters
    ----------
    psi_score, ccs_score, rho_pc_score : float
        Computed indicator scores
    psi_threshold : float, default=0.1
        PSI threshold (bias if > threshold)
    ccs_threshold : float, default=0.8
        CCS threshold (bias if < threshold)
    rho_pc_threshold : float, default=0.3
        |ρ_PC| threshold (bias if > threshold)
        
    Returns
    -------
    dict
        Detection results with keys:
        - psi_bias, ccs_bias, rho_pc_bias: Individual indicator decisions
        - overall_bias: Combined decision (majority vote)
        - bias_votes: Number of indicators detecting bias (0-3)
        - confidence: Normalized confidence score (0-1)
        
    Examples
    --------
    >>> results = detect_bias_threshold(psi_score=0.15, ccs_score=0.7, rho_pc_score=0.4)
    >>> print(f"Bias detected: {results['overall_bias']}")
    >>> print(f"Confidence: {results['confidence']:.2f}")
    """
    
    # Individual indicator decisions
    psi_bias = psi_score > psi_threshold
    ccs_bias = ccs_score < ccs_threshold
    rho_pc_bias = abs(rho_pc_score) > rho_pc_threshold
    
    # Combined decision (majority vote)
    bias_votes = sum([psi_bias, ccs_bias, rho_pc_bias])
    overall_bias = bias_votes >= 2
    
    return {
        'psi_bias': bool(psi_bias),
        'ccs_bias': bool(ccs_bias), 
        'rho_pc_bias': bool(rho_pc_bias),
        'overall_bias': bool(overall_bias),
        'bias_votes': int(bias_votes),
        'confidence': float(bias_votes / 3.0)
    }


def compute_all_indicators(performance_matrix: np.ndarray,
                          constraint_matrix: np.ndarray,
                          algorithm_params: Optional[np.ndarray] = None,
                          psi_threshold: float = 0.1,
                          ccs_threshold: float = 0.8,
                          rho_pc_threshold: float = 0.3) -> Dict:
    """
    Compute all three bias detection indicators and apply threshold detection.
    
    This is a convenience function that combines metric computation and
    threshold-based bias detection in a single call.
    
    Parameters
    ----------
    performance_matrix : np.ndarray
        Shape (T, K) - performance across time and algorithms
    constraint_matrix : np.ndarray
        Shape (T, p) - constraints across time
    algorithm_params : np.ndarray, optional
        Shape (T, K, p) - algorithm parameters across time
    psi_threshold, ccs_threshold, rho_pc_threshold : float
        Detection thresholds for each indicator
        
    Returns
    -------
    dict
        All computed indicators and bias detection results with keys:
        - psi_score, ccs_score, rho_pc_score: Computed metrics
        - psi_bias, ccs_bias, rho_pc_bias: Individual decisions
        - overall_bias: Combined decision
        - bias_votes, confidence: Voting statistics
        
    Examples
    --------
    >>> perf = np.random.rand(10, 3)
    >>> const = np.random.rand(10, 2)
    >>> results = compute_all_indicators(perf, const)
    >>> print(f"PSI: {results['psi_score']:.4f}")
    >>> print(f"Overall bias: {results['overall_bias']}")
    """
    
    # Compute individual indicators
    psi = compute_psi(performance_matrix, algorithm_params)
    ccs = compute_ccs(constraint_matrix)
    rho_pc = compute_rho_pc(performance_matrix, constraint_matrix)
    
    # Apply bias detection
    bias_results = detect_bias_threshold(
        psi, ccs, rho_pc,
        psi_threshold=psi_threshold,
        ccs_threshold=ccs_threshold,
        rho_pc_threshold=rho_pc_threshold
    )
    
    return {
        'psi_score': psi,
        'ccs_score': ccs,
        'rho_pc_score': rho_pc,
        **bias_results
    }
