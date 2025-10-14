"""
Core algorithms for circular reasoning bias detection.

This module implements the three main indicators:
- PSI (Performance-Structure Independence)
- CCS (Constraint-Consistency Score)  
- ρ_PC (Performance-Constraint Correlation)
"""

import numpy as np
from scipy import stats
from typing import Tuple, Optional, Dict
import warnings

def compute_psi(performance_matrix: np.ndarray, 
                algorithm_params: Optional[np.ndarray] = None) -> float:
    """
    Compute Performance-Structure Independence (PSI) score.
    
    PSI measures parameter stability across evaluation periods by computing
    the average parameter difference between consecutive time steps.
    
    Parameters:
    -----------
    performance_matrix : np.ndarray
        Shape (T, K) where T is time periods, K is algorithms
    algorithm_params : np.ndarray, optional
        Shape (T, K, p) where p is parameter dimensions
        If None, uses performance as proxy for parameters
        
    Returns:
    --------
    float
        PSI score (higher values indicate more instability/bias)
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
    return np.mean(psi_scores)

def compute_ccs(constraint_matrix: np.ndarray) -> float:
    """
    Compute Constraint-Consistency Score (CCS).
    
    CCS measures the consistency of constraint specifications across
    evaluation periods using coefficient of variation.
    
    Parameters:
    -----------
    constraint_matrix : np.ndarray
        Shape (T, p) where T is time periods, p is constraint types
        
    Returns:
    --------
    float
        CCS score (higher values indicate more consistency)
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
    return np.mean(consistency_scores)

def compute_rho_pc(performance_matrix: np.ndarray, 
                   constraint_matrix: np.ndarray) -> float:
    """
    Compute Performance-Constraint correlation coefficient (ρ_PC).
    
    ρ_PC measures the correlation between performance trajectories
    and constraint specification changes.
    
    Parameters:
    -----------
    performance_matrix : np.ndarray
        Shape (T, K) where T is time periods, K is algorithms
    constraint_matrix : np.ndarray
        Shape (T, p) where T is time periods, p is constraint types
        
    Returns:
    --------
    float
        ρ_PC correlation coefficient (-1 to 1)
    """
    T, K = performance_matrix.shape
    T_c, p = constraint_matrix.shape
    
    if T != T_c:
        raise ValueError("Performance and constraint matrices must have same time dimension")
    
    if T < 3:
        warnings.warn("ρ_PC requires at least 3 time periods for reliable correlation")
        return 0.0
    
    # Aggregate performance across algorithms (mean)
    perf_trajectory = np.mean(performance_matrix, axis=1)
    
    # Aggregate constraints (weighted by variance to emphasize changing constraints)
    constraint_weights = np.var(constraint_matrix, axis=0)
    
    # Avoid division by zero
    constraint_weights = constraint_weights / (np.sum(constraint_weights) + 1e-10)
    
    constraint_trajectory = np.average(constraint_matrix, axis=1, weights=constraint_weights)
    
    # Compute Pearson correlation
    try:
        correlation, p_value = stats.pearsonr(perf_trajectory, constraint_trajectory)
        
        # Handle NaN correlations
        if np.isnan(correlation):
            return 0.0
            
        return correlation
        
    except Exception as e:
        warnings.warn(f"Error computing correlation: {e}")
        return 0.0

def detect_bias_threshold(psi_score: float, 
                         ccs_score: float, 
                         rho_pc_score: float,
                         psi_threshold: float = 0.1,
                         ccs_threshold: float = 0.8,
                         rho_pc_threshold: float = 0.3) -> dict:
    """
    Apply threshold-based bias detection using all three indicators.
    
    Parameters:
    -----------
    psi_score, ccs_score, rho_pc_score : float
        Computed indicator scores
    psi_threshold : float
        PSI threshold (bias if > threshold)
    ccs_threshold : float  
        CCS threshold (bias if < threshold)
    rho_pc_threshold : float
        |ρ_PC| threshold (bias if > threshold)
        
    Returns:
    --------
    dict
        Detection results with individual and combined decisions
    """
    
    # Individual indicator decisions
    psi_bias = psi_score > psi_threshold
    ccs_bias = ccs_score < ccs_threshold
    rho_pc_bias = abs(rho_pc_score) > rho_pc_threshold
    
    # Combined decision (majority vote)
    bias_votes = sum([psi_bias, ccs_bias, rho_pc_bias])
    overall_bias = bias_votes >= 2
    
    return {
        'psi_bias': psi_bias,
        'ccs_bias': ccs_bias, 
        'rho_pc_bias': rho_pc_bias,
        'overall_bias': overall_bias,
        'bias_votes': bias_votes,
        'confidence': bias_votes / 3.0
    }

def compute_all_indicators(performance_matrix: np.ndarray,
                          constraint_matrix: np.ndarray,
                          algorithm_params: Optional[np.ndarray] = None) -> dict:
    """
    Compute all three bias detection indicators.
    
    Parameters:
    -----------
    performance_matrix : np.ndarray
        Shape (T, K) - performance across time and algorithms
    constraint_matrix : np.ndarray
        Shape (T, p) - constraints across time
    algorithm_params : np.ndarray, optional
        Shape (T, K, p) - algorithm parameters across time
        
    Returns:
    --------
    dict
        All computed indicators and bias detection results
    """
    
    # Compute individual indicators
    psi = compute_psi(performance_matrix, algorithm_params)
    ccs = compute_ccs(constraint_matrix)
    rho_pc = compute_rho_pc(performance_matrix, constraint_matrix)
    
    # Apply bias detection
    bias_results = detect_bias_threshold(psi, ccs, rho_pc)
    
    return {
        'psi_score': psi,
        'ccs_score': ccs,
        'rho_pc_score': rho_pc,
        **bias_results
    }


def bootstrap_psi(performance_matrix: np.ndarray, 
                  algorithm_params: Optional[np.ndarray] = None,
                  n_bootstrap: int = 1000,
                  confidence_level: float = 0.95,
                  random_seed: Optional[int] = None) -> Dict:
    """
    Compute PSI with bootstrap confidence intervals and p-value.
    
    Uses bootstrap resampling to estimate the distribution of PSI scores
    and compute statistical significance.
    
    Parameters:
    -----------
    performance_matrix : np.ndarray
        Shape (T, K) where T is time periods, K is algorithms
    algorithm_params : np.ndarray, optional
        Shape (T, K, p) where p is parameter dimensions
    n_bootstrap : int
        Number of bootstrap samples (default: 1000)
    confidence_level : float
        Confidence level for intervals (default: 0.95)
    random_seed : int, optional
        Random seed for reproducibility
        
    Returns:
    --------
    dict
        - 'psi': Point estimate
        - 'ci_lower': Lower confidence bound
        - 'ci_upper': Upper confidence bound
        - 'p_value': P-value for H0: PSI=0
        - 'std_error': Bootstrap standard error
    """
    if random_seed is not None:
        np.random.seed(random_seed)
    
    T, K = performance_matrix.shape
    
    # Compute point estimate
    psi_observed = compute_psi(performance_matrix, algorithm_params)
    
    # Bootstrap resampling
    bootstrap_psis = []
    
    for _ in range(n_bootstrap):
        # Resample time periods with replacement
        indices = np.random.choice(T, size=T, replace=True)
        
        perf_boot = performance_matrix[indices, :]
        
        if algorithm_params is not None:
            params_boot = algorithm_params[indices, :, :]
        else:
            params_boot = None
        
        try:
            psi_boot = compute_psi(perf_boot, params_boot)
            bootstrap_psis.append(psi_boot)
        except:
            continue
    
    bootstrap_psis = np.array(bootstrap_psis)
    
    # Compute confidence interval
    alpha = 1 - confidence_level
    ci_lower = np.percentile(bootstrap_psis, 100 * alpha / 2)
    ci_upper = np.percentile(bootstrap_psis, 100 * (1 - alpha / 2))
    
    # Compute p-value (two-tailed test for H0: PSI = 0)
    # P-value = proportion of bootstrap samples more extreme than observed
    p_value = np.mean(np.abs(bootstrap_psis - np.mean(bootstrap_psis)) >= 
                      np.abs(psi_observed - np.mean(bootstrap_psis)))
    
    # Standard error
    std_error = np.std(bootstrap_psis)
    
    return {
        'psi': psi_observed,
        'ci_lower': ci_lower,
        'ci_upper': ci_upper,
        'p_value': p_value,
        'std_error': std_error,
        'n_bootstrap': n_bootstrap
    }


def bootstrap_ccs(constraint_matrix: np.ndarray,
                  n_bootstrap: int = 1000,
                  confidence_level: float = 0.95,
                  random_seed: Optional[int] = None) -> Dict:
    """
    Compute CCS with bootstrap confidence intervals and p-value.
    
    Parameters:
    -----------
    constraint_matrix : np.ndarray
        Shape (T, p) where T is time periods, p is constraint types
    n_bootstrap : int
        Number of bootstrap samples
    confidence_level : float
        Confidence level for intervals
    random_seed : int, optional
        Random seed for reproducibility
        
    Returns:
    --------
    dict
        - 'ccs': Point estimate
        - 'ci_lower': Lower confidence bound
        - 'ci_upper': Upper confidence bound
        - 'p_value': P-value for H0: CCS=1 (perfect consistency)
        - 'std_error': Bootstrap standard error
    """
    if random_seed is not None:
        np.random.seed(random_seed)
    
    T, p = constraint_matrix.shape
    
    # Compute point estimate
    ccs_observed = compute_ccs(constraint_matrix)
    
    # Bootstrap resampling
    bootstrap_ccss = []
    
    for _ in range(n_bootstrap):
        indices = np.random.choice(T, size=T, replace=True)
        const_boot = constraint_matrix[indices, :]
        
        try:
            ccs_boot = compute_ccs(const_boot)
            bootstrap_ccss.append(ccs_boot)
        except:
            continue
    
    bootstrap_ccss = np.array(bootstrap_ccss)
    
    # Confidence interval
    alpha = 1 - confidence_level
    ci_lower = np.percentile(bootstrap_ccss, 100 * alpha / 2)
    ci_upper = np.percentile(bootstrap_ccss, 100 * (1 - alpha / 2))
    
    # P-value for H0: CCS = 1 (perfect consistency)
    p_value = np.mean(np.abs(bootstrap_ccss - 1.0) >= np.abs(ccs_observed - 1.0))
    
    std_error = np.std(bootstrap_ccss)
    
    return {
        'ccs': ccs_observed,
        'ci_lower': ci_lower,
        'ci_upper': ci_upper,
        'p_value': p_value,
        'std_error': std_error,
        'n_bootstrap': n_bootstrap
    }


def bootstrap_rho_pc(performance_matrix: np.ndarray,
                     constraint_matrix: np.ndarray,
                     n_bootstrap: int = 1000,
                     confidence_level: float = 0.95,
                     random_seed: Optional[int] = None) -> Dict:
    """
    Compute ρ_PC with bootstrap confidence intervals and p-value.
    
    Parameters:
    -----------
    performance_matrix : np.ndarray
        Shape (T, K) where T is time periods, K is algorithms
    constraint_matrix : np.ndarray
        Shape (T, p) where T is time periods, p is constraint types
    n_bootstrap : int
        Number of bootstrap samples
    confidence_level : float
        Confidence level for intervals
    random_seed : int, optional
        Random seed for reproducibility
        
    Returns:
    --------
    dict
        - 'rho_pc': Point estimate
        - 'ci_lower': Lower confidence bound
        - 'ci_upper': Upper confidence bound
        - 'p_value': P-value for H0: ρ_PC=0
        - 'std_error': Bootstrap standard error
    """
    if random_seed is not None:
        np.random.seed(random_seed)
    
    T, K = performance_matrix.shape
    
    # Compute point estimate
    rho_observed = compute_rho_pc(performance_matrix, constraint_matrix)
    
    # Bootstrap resampling
    bootstrap_rhos = []
    
    for _ in range(n_bootstrap):
        indices = np.random.choice(T, size=T, replace=True)
        
        perf_boot = performance_matrix[indices, :]
        const_boot = constraint_matrix[indices, :]
        
        try:
            rho_boot = compute_rho_pc(perf_boot, const_boot)
            bootstrap_rhos.append(rho_boot)
        except:
            continue
    
    bootstrap_rhos = np.array(bootstrap_rhos)
    
    # Confidence interval
    alpha = 1 - confidence_level
    ci_lower = np.percentile(bootstrap_rhos, 100 * alpha / 2)
    ci_upper = np.percentile(bootstrap_rhos, 100 * (1 - alpha / 2))
    
    # P-value for H0: ρ_PC = 0
    p_value = np.mean(np.abs(bootstrap_rhos) >= np.abs(rho_observed))
    
    std_error = np.std(bootstrap_rhos)
    
    return {
        'rho_pc': rho_observed,
        'ci_lower': ci_lower,
        'ci_upper': ci_upper,
        'p_value': p_value,
        'std_error': std_error,
        'n_bootstrap': n_bootstrap
    }


def compute_adaptive_thresholds(performance_matrix: np.ndarray,
                               constraint_matrix: np.ndarray,
                               quantile: float = 0.95,
                               n_simulations: int = 500,
                               random_seed: Optional[int] = None) -> Dict:
    """
    Compute data-adaptive thresholds based on null distribution.
    
    Uses permutation tests to estimate null distributions under H0 (no bias)
    and sets thresholds at specified quantiles.
    
    Parameters:
    -----------
    performance_matrix : np.ndarray
        Shape (T, K) - observed performance data
    constraint_matrix : np.ndarray
        Shape (T, p) - observed constraint data
    quantile : float
        Quantile for threshold (default: 0.95 for 95% specificity)
    n_simulations : int
        Number of permutations for null distribution
    random_seed : int, optional
        Random seed for reproducibility
        
    Returns:
    --------
    dict
        - 'psi_threshold': Adaptive PSI threshold
        - 'ccs_threshold': Adaptive CCS threshold
        - 'rho_pc_threshold': Adaptive ρ_PC threshold
        - 'method': 'adaptive_quantile'
    """
    if random_seed is not None:
        np.random.seed(random_seed)
    
    T, K = performance_matrix.shape
    _, p = constraint_matrix.shape
    
    null_psis = []
    null_ccss = []
    null_rhos = []
    
    for _ in range(n_simulations):
        # Permute time order to break temporal structure (H0: no bias)
        perm_indices = np.random.permutation(T)
        
        perf_perm = performance_matrix[perm_indices, :]
        const_perm = constraint_matrix[perm_indices, :]
        
        try:
            psi_null = compute_psi(perf_perm)
            ccs_null = compute_ccs(const_perm)
            rho_null = compute_rho_pc(perf_perm, const_perm)
            
            null_psis.append(psi_null)
            null_ccss.append(ccs_null)
            null_rhos.append(np.abs(rho_null))  # Use absolute value
        except:
            continue
    
    null_psis = np.array(null_psis)
    null_ccss = np.array(null_ccss)
    null_rhos = np.array(null_rhos)
    
    # Compute adaptive thresholds
    psi_threshold = np.percentile(null_psis, quantile * 100)
    ccs_threshold = np.percentile(null_ccss, (1 - quantile) * 100)  # Lower tail
    rho_threshold = np.percentile(null_rhos, quantile * 100)
    
    return {
        'psi_threshold': psi_threshold,
        'ccs_threshold': ccs_threshold,
        'rho_pc_threshold': rho_threshold,
        'method': 'adaptive_quantile',
        'quantile': quantile,
        'n_simulations': n_simulations
    }
