"""
Advanced detection metrics for circular bias detection.

This module implements 5 new indicators:
- TDI: Temporal Dependency Index
- ICS: Information Criterion Score
- CBI: Cross-Benchmark Inconsistency
- ADS: Adaptive Drift Score
- MCI: Multi-Constraint Interaction
"""

import numpy as np
from scipy import stats
from typing import Tuple, Optional, Dict
import warnings


def compute_tdi(performance_matrix: np.ndarray, lag: int = 3) -> float:
    """
    Compute Temporal Dependency Index (TDI).
    
    Detects whether evaluation results abnormally depend on historical information.
    High TDI suggests "chasing trends" style parameter tuning.
    
    Parameters:
    -----------
    performance_matrix : np.ndarray, shape (T, K)
        Performance values across time and algorithms
    lag : int, default=3
        Historical window length to consider
        
    Returns:
    --------
    float
        TDI score in [0, 1], higher values indicate stronger temporal dependency
        
    Interpretation:
    ---------------
    - TDI < 0.3: Weak temporal dependency (good)
    - 0.3 ≤ TDI < 0.6: Moderate temporal dependency
    - TDI ≥ 0.6: Strong temporal dependency (potential bias)
    """
    T, K = performance_matrix.shape
    
    if T < lag + 2:
        warnings.warn(f"TDI requires at least {lag+2} time periods, got {T}")
        return 0.0
    
    try:
        from sklearn.feature_selection import mutual_info_regression
    except ImportError:
        warnings.warn("scikit-learn required for TDI computation")
        # Fallback: use autocorrelation
        return _compute_tdi_fallback(performance_matrix, lag)
    
    tdi_scores = []
    
    for k in range(K):
        perf_series = performance_matrix[:, k]
        
        # Build feature matrix: historical performance
        X_history = []
        y_current = []
        
        for t in range(lag, T):
            X_history.append(perf_series[t-lag:t])
            y_current.append(perf_series[t])
        
        X_history = np.array(X_history)
        y_current = np.array(y_current)
        
        # Compute mutual information
        mi_scores = mutual_info_regression(
            X_history, y_current, 
            random_state=42,
            n_neighbors=min(3, len(y_current)-1)
        )
        avg_mi = np.mean(mi_scores)
        
        # Normalize by entropy of current performance
        hist, _ = np.histogram(y_current, bins=min(10, len(y_current)//2), density=True)
        hist = hist[hist > 0]
        entropy = -np.sum(hist * np.log(hist + 1e-10))
        
        if entropy > 0:
            tdi_k = min(avg_mi / entropy, 1.0)
        else:
            tdi_k = 0.0
            
        tdi_scores.append(tdi_k)
    
    return np.mean(tdi_scores)


def _compute_tdi_fallback(performance_matrix: np.ndarray, lag: int) -> float:
    """Fallback TDI computation using autocorrelation."""
    T, K = performance_matrix.shape
    
    autocorr_scores = []
    for k in range(K):
        perf_series = performance_matrix[:, k]
        # Compute autocorrelation at lag
        autocorr = np.corrcoef(perf_series[:-lag], perf_series[lag:])[0, 1]
        autocorr_scores.append(abs(autocorr))
    
    return np.mean(autocorr_scores)


def compute_ics(performance_matrix: np.ndarray, 
                constraint_matrix: np.ndarray,
                model_complexity: Optional[np.ndarray] = None) -> float:
    """
    Compute Information Criterion Score (ICS).
    
    Evaluates whether model selection overfits the evaluation data.
    
    Parameters:
    -----------
    performance_matrix : np.ndarray, shape (T, K)
    constraint_matrix : np.ndarray, shape (T, p)
    model_complexity : np.ndarray, shape (T, K), optional
        Complexity measure for each algorithm at each time
        (e.g., number of parameters, layers)
        If None, uses constraint sum as proxy
        
    Returns:
    --------
    float
        ICS score. Positive = reasonable complexity growth,
        Negative = potential overfitting
        
    Interpretation:
    ---------------
    - ICS > 0: Complexity growth justified by performance
    - -0.5 ≤ ICS ≤ 0: Borderline
    - ICS < -0.5: Unreasonable complexity growth (potential bias)
    """
    T, K = performance_matrix.shape
    
    if model_complexity is None:
        # Proxy: use constraint sum as complexity measure
        complexity_proxy = np.sum(constraint_matrix, axis=1)
        model_complexity = np.tile(complexity_proxy.reshape(-1, 1), (1, K))
    
    ics_scores = []
    
    for k in range(K):
        perf = performance_matrix[:, k]
        complexity = model_complexity[:, k]
        
        # Compute AIC trend
        # AIC approximation: assuming Gaussian errors
        residuals = perf - np.mean(perf)
        sigma_sq = np.var(residuals)
        
        if sigma_sq < 1e-10:
            ics_scores.append(0.0)
            continue
        
        aic_trajectory = []
        for t in range(T):
            # AIC = 2k - 2ln(L)
            log_likelihood = -0.5 * np.log(2 * np.pi * sigma_sq) - 0.5 * residuals[t]**2 / sigma_sq
            aic_t = 2 * complexity[t] / T - 2 * log_likelihood
            aic_trajectory.append(aic_t)
        
        # Check AIC trend
        # Negative trend (AIC decreasing despite complexity increasing) = good
        # Positive trend = bad
        if len(aic_trajectory) > 1:
            aic_trend = np.polyfit(range(T), aic_trajectory, 1)[0]
            ics_scores.append(-aic_trend)  # Invert so high = good
        else:
            ics_scores.append(0.0)
    
    return np.mean(ics_scores)


def compute_cbi(performance_matrix: np.ndarray,
                benchmark_ids: np.ndarray) -> float:
    """
    Compute Cross-Benchmark Inconsistency (CBI).
    
    Detects abnormal inconsistency in algorithm rankings across different benchmarks.
    
    Parameters:
    -----------
    performance_matrix : np.ndarray, shape (T, K)
    benchmark_ids : np.ndarray, shape (T,)
        Benchmark identifier for each time period
        
    Returns:
    --------
    float
        CBI score in [0, 1]. Higher values indicate greater inconsistency.
        
    Interpretation:
    ---------------
    - CBI < 0.2: Consistent rankings (good)
    - 0.2 ≤ CBI < 0.4: Moderate inconsistency
    - CBI ≥ 0.4: High inconsistency (potential benchmark selection bias)
    
    Notes:
    ------
    Requires at least 2 different benchmarks to compute.
    """
    unique_benchmarks = np.unique(benchmark_ids)
    
    if len(unique_benchmarks) < 2:
        warnings.warn("CBI requires at least 2 different benchmarks")
        return 0.0
    
    from scipy.stats import kendalltau
    
    # Compute algorithm rankings for each benchmark
    rankings = {}
    for bm in unique_benchmarks:
        bm_mask = benchmark_ids == bm
        if np.sum(bm_mask) == 0:
            continue
        bm_perf = performance_matrix[bm_mask, :].mean(axis=0)
        # Ranking: higher performance = lower rank number
        rankings[bm] = np.argsort(np.argsort(-bm_perf))
    
    if len(rankings) < 2:
        return 0.0
    
    # Compute pairwise Kendall tau inconsistencies
    inconsistencies = []
    benchmarks_list = list(rankings.keys())
    
    for i in range(len(benchmarks_list)):
        for j in range(i+1, len(benchmarks_list)):
            bm_i = benchmarks_list[i]
            bm_j = benchmarks_list[j]
            
            try:
                tau, _ = kendalltau(rankings[bm_i], rankings[bm_j])
                # Convert correlation to inconsistency
                inconsistency = (1 - tau) / 2  # Map [-1,1] to [1,0]
                inconsistencies.append(inconsistency)
            except:
                continue
    
    if not inconsistencies:
        return 0.0
    
    return np.mean(inconsistencies)


def compute_ads(performance_matrix: np.ndarray,
                constraint_matrix: np.ndarray,
                justification_scores: Optional[np.ndarray] = None) -> float:
    """
    Compute Adaptive Drift Score (ADS).
    
    Distinguishes reasonable methodological progress from unreasonable
    performance chasing.
    
    Parameters:
    -----------
    performance_matrix : np.ndarray, shape (T, K)
    constraint_matrix : np.ndarray, shape (T, p)
    justification_scores : np.ndarray, shape (T,), optional
        Justification score (0-1) for each time period.
        Can be based on paper publications, methodological innovations, etc.
        If None, uses linear decay (early changes more justified)
        
    Returns:
    --------
    float
        ADS score. Higher values indicate unexplainable performance drift.
        
    Interpretation:
    ---------------
    - ADS < 0.15: Justifiable drift
    - 0.15 ≤ ADS < 0.3: Moderate drift
    - ADS ≥ 0.3: Unexplainable drift (potential "tuning to test set")
    """
    T, K = performance_matrix.shape
    
    if T < 2:
        return 0.0
    
    if justification_scores is None:
        # Default: earlier changes more justified
        justification_scores = np.linspace(1.0, 0.5, T)
    
    # Compute performance gains
    perf_mean = performance_matrix.mean(axis=1)
    perf_gains = np.diff(perf_mean)
    
    # Compute constraint changes
    constraint_changes = np.linalg.norm(np.diff(constraint_matrix, axis=0), axis=1)
    
    # Normalize constraint changes to [0, 1]
    if constraint_changes.max() > 0:
        constraint_changes = constraint_changes / constraint_changes.max()
    
    # Unjustified drift = positive gain × large constraint change × low justification
    ads_scores = []
    for t in range(len(perf_gains)):
        if perf_gains[t] > 0:  # Only consider performance improvements
            unjustified = (perf_gains[t] * 
                          constraint_changes[t] / 
                          (justification_scores[t+1] + 0.1))
            ads_scores.append(unjustified)
    
    return np.mean(ads_scores) if ads_scores else 0.0


def compute_mci(constraint_matrix: np.ndarray) -> Tuple[float, np.ndarray]:
    """
    Compute Multi-Constraint Interaction (MCI) index.
    
    Detects abnormal coordinated changes across multiple constraints.
    
    Parameters:
    -----------
    constraint_matrix : np.ndarray, shape (T, p)
        
    Returns:
    --------
    mci_score : float
        MCI score. Higher values indicate stronger constraint interactions.
    corr_matrix : np.ndarray, shape (p, p)
        Constraint correlation matrix
        
    Interpretation:
    ---------------
    - MCI < 0.5: Weak constraint interactions (good)
    - 0.5 ≤ MCI < 0.8: Moderate interactions
    - MCI ≥ 0.8: Strong interactions (potential compensatory manipulation)
    """
    T, p = constraint_matrix.shape
    
    if p < 2:
        return 0.0, np.eye(1)
    
    # Standardize constraints
    constraint_std = (constraint_matrix - constraint_matrix.mean(axis=0)) / \
                     (constraint_matrix.std(axis=0) + 1e-8)
    
    # Compute correlation matrix
    corr_matrix = np.corrcoef(constraint_std.T)
    
    # Remove diagonal
    corr_matrix_no_diag = corr_matrix.copy()
    np.fill_diagonal(corr_matrix_no_diag, 0)
    
    # Maximum absolute correlation
    max_corr = np.max(np.abs(corr_matrix_no_diag))
    
    # Count high correlation pairs
    high_corr_pairs = np.sum(np.abs(corr_matrix_no_diag) > 0.7) / 2
    
    # MCI score: combines max correlation and number of high-corr pairs
    mci_score = max_corr * (1 + np.log1p(high_corr_pairs))
    
    return mci_score, corr_matrix


def compute_all_advanced_metrics(performance_matrix: np.ndarray,
                                 constraint_matrix: np.ndarray,
                                 benchmark_ids: Optional[np.ndarray] = None,
                                 model_complexity: Optional[np.ndarray] = None,
                                 justification_scores: Optional[np.ndarray] = None) -> Dict:
    """
    Compute all advanced metrics in one call.
    
    Parameters:
    -----------
    performance_matrix : np.ndarray, shape (T, K)
    constraint_matrix : np.ndarray, shape (T, p)
    benchmark_ids : np.ndarray, shape (T,), optional
        Required for CBI computation
    model_complexity : np.ndarray, shape (T, K), optional
        For ICS computation
    justification_scores : np.ndarray, shape (T,), optional
        For ADS computation
        
    Returns:
    --------
    dict
        Dictionary containing all advanced metric scores
    """
    T = len(performance_matrix)
    
    results = {
        'tdi': compute_tdi(performance_matrix),
        'ics': compute_ics(performance_matrix, constraint_matrix, model_complexity),
        'ads': compute_ads(performance_matrix, constraint_matrix, justification_scores),
    }
    
    # MCI with correlation matrix
    mci_score, mci_corr = compute_mci(constraint_matrix)
    results['mci'] = mci_score
    results['mci_correlation_matrix'] = mci_corr
    
    # CBI if benchmark IDs provided
    if benchmark_ids is not None:
        results['cbi'] = compute_cbi(performance_matrix, benchmark_ids)
    else:
        results['cbi'] = None
    
    return results
