"""
Bootstrap methods for statistical inference in circular bias detection.

This module provides bootstrap resampling methods for computing confidence
intervals and p-values for PSI, CCS, and ρ_PC indicators.
"""

import numpy as np
from typing import Optional, Dict
from .metrics import compute_psi, compute_ccs, compute_rho_pc


def bootstrap_psi(performance_matrix: np.ndarray, 
                  algorithm_params: Optional[np.ndarray] = None,
                  n_bootstrap: int = 1000,
                  confidence_level: float = 0.95,
                  random_seed: Optional[int] = None) -> Dict:
    """
    Compute PSI with bootstrap confidence intervals and p-value.
    
    Uses bootstrap resampling to estimate the distribution of PSI scores
    and compute statistical significance.
    
    Parameters
    ----------
    performance_matrix : np.ndarray
        Shape (T, K) where T is time periods, K is algorithms
    algorithm_params : np.ndarray, optional
        Shape (T, K, p) where p is parameter dimensions
    n_bootstrap : int, default=1000
        Number of bootstrap samples
    confidence_level : float, default=0.95
        Confidence level for intervals (e.g., 0.95 for 95% CI)
    random_seed : int, optional
        Random seed for reproducibility
        
    Returns
    -------
    dict
        Bootstrap results with keys:
        - psi: Point estimate
        - ci_lower: Lower confidence bound
        - ci_upper: Upper confidence bound
        - p_value: P-value for H0: PSI=0
        - std_error: Bootstrap standard error
        - n_bootstrap: Number of bootstrap samples used
        
    Examples
    --------
    >>> perf = np.random.rand(10, 3)
    >>> results = bootstrap_psi(perf, n_bootstrap=1000, random_seed=42)
    >>> print(f"PSI: {results['psi']:.4f} [{results['ci_lower']:.4f}, {results['ci_upper']:.4f}]")
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
        'psi': float(psi_observed),
        'ci_lower': float(ci_lower),
        'ci_upper': float(ci_upper),
        'p_value': float(p_value),
        'std_error': float(std_error),
        'n_bootstrap': int(n_bootstrap)
    }


def bootstrap_ccs(constraint_matrix: np.ndarray,
                  n_bootstrap: int = 1000,
                  confidence_level: float = 0.95,
                  random_seed: Optional[int] = None) -> Dict:
    """
    Compute CCS with bootstrap confidence intervals and p-value.
    
    Parameters
    ----------
    constraint_matrix : np.ndarray
        Shape (T, p) where T is time periods, p is constraint types
    n_bootstrap : int, default=1000
        Number of bootstrap samples
    confidence_level : float, default=0.95
        Confidence level for intervals
    random_seed : int, optional
        Random seed for reproducibility
        
    Returns
    -------
    dict
        Bootstrap results with keys:
        - ccs: Point estimate
        - ci_lower: Lower confidence bound
        - ci_upper: Upper confidence bound
        - p_value: P-value for H0: CCS=1 (perfect consistency)
        - std_error: Bootstrap standard error
        - n_bootstrap: Number of bootstrap samples used
        
    Examples
    --------
    >>> const = np.random.rand(10, 2)
    >>> results = bootstrap_ccs(const, n_bootstrap=1000, random_seed=42)
    >>> print(f"CCS: {results['ccs']:.4f} (p={results['p_value']:.4f})")
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
        'ccs': float(ccs_observed),
        'ci_lower': float(ci_lower),
        'ci_upper': float(ci_upper),
        'p_value': float(p_value),
        'std_error': float(std_error),
        'n_bootstrap': int(n_bootstrap)
    }


def bootstrap_rho_pc(performance_matrix: np.ndarray,
                     constraint_matrix: np.ndarray,
                     n_bootstrap: int = 1000,
                     confidence_level: float = 0.95,
                     random_seed: Optional[int] = None) -> Dict:
    """
    Compute ρ_PC with bootstrap confidence intervals and p-value.
    
    Parameters
    ----------
    performance_matrix : np.ndarray
        Shape (T, K) where T is time periods, K is algorithms
    constraint_matrix : np.ndarray
        Shape (T, p) where T is time periods, p is constraint types
    n_bootstrap : int, default=1000
        Number of bootstrap samples
    confidence_level : float, default=0.95
        Confidence level for intervals
    random_seed : int, optional
        Random seed for reproducibility
        
    Returns
    -------
    dict
        Bootstrap results with keys:
        - rho_pc: Point estimate
        - ci_lower: Lower confidence bound
        - ci_upper: Upper confidence bound
        - p_value: P-value for H0: ρ_PC=0
        - std_error: Bootstrap standard error
        - n_bootstrap: Number of bootstrap samples used
        
    Examples
    --------
    >>> perf = np.random.rand(10, 3)
    >>> const = np.random.rand(10, 2)
    >>> results = bootstrap_rho_pc(perf, const, n_bootstrap=1000, random_seed=42)
    >>> print(f"ρ_PC: {results['rho_pc']:.4f} (95% CI: [{results['ci_lower']:.4f}, {results['ci_upper']:.4f}])")
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
        'rho_pc': float(rho_observed),
        'ci_lower': float(ci_lower),
        'ci_upper': float(ci_upper),
        'p_value': float(p_value),
        'std_error': float(std_error),
        'n_bootstrap': int(n_bootstrap)
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
    
    Parameters
    ----------
    performance_matrix : np.ndarray
        Shape (T, K) - observed performance data
    constraint_matrix : np.ndarray
        Shape (T, p) - observed constraint data
    quantile : float, default=0.95
        Quantile for threshold (e.g., 0.95 for 95% specificity)
    n_simulations : int, default=500
        Number of permutations for null distribution
    random_seed : int, optional
        Random seed for reproducibility
        
    Returns
    -------
    dict
        Adaptive thresholds with keys:
        - psi_threshold: Adaptive PSI threshold
        - ccs_threshold: Adaptive CCS threshold
        - rho_pc_threshold: Adaptive ρ_PC threshold
        - method: 'adaptive_quantile'
        - quantile: Quantile used
        - n_simulations: Number of simulations performed
        
    Examples
    --------
    >>> perf = np.random.rand(10, 3)
    >>> const = np.random.rand(10, 2)
    >>> thresholds = compute_adaptive_thresholds(perf, const, quantile=0.95)
    >>> print(f"Adaptive PSI threshold: {thresholds['psi_threshold']:.4f}")
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
        'psi_threshold': float(psi_threshold),
        'ccs_threshold': float(ccs_threshold),
        'rho_pc_threshold': float(rho_threshold),
        'method': 'adaptive_quantile',
        'quantile': float(quantile),
        'n_simulations': int(n_simulations)
    }
