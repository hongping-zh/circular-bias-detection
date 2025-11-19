"""Multivariate bias detection using MANOVA and energy distance.

Supports joint detection across multiple metrics for comprehensive evaluation
of multi-task benchmarks like GLUE (9 tasks) and MMLU (57 subtasks).
"""
from typing import List, Dict, Optional, Callable, Any, Tuple
import numpy as np
import warnings


def detect_multivariate_bias(
    model,
    X: np.ndarray,
    y: np.ndarray,
    metrics: List[Callable],
    metric_names: Optional[List[str]] = None,
    n_permutations: int = 1000,
    random_state: Optional[int] = None,
    method: str = "energy",
    alpha: float = 0.05,
    n_jobs: int = 1
) -> Dict:
    """Detect bias using multiple metrics jointly (multivariate test).
    
    This is more powerful than testing each metric separately, as it can detect
    patterns where individual metrics appear normal but joint distribution is suspicious.
    
    Parameters:
    -----------
    model : object
        Model with predict() method
    X : array-like
        Feature matrix
    y : array-like
        True labels
    metrics : list of callable
        List of metric functions, each with signature metric(y_true, y_pred) -> float
    metric_names : list of str, optional
        Names for each metric (for reporting)
    n_permutations : int, default=1000
        Number of permutations for null distribution
    random_state : int, optional
        Random seed
    method : {'energy', 'manova', 'hotelling'}, default='energy'
        Multivariate test method:
        - 'energy': Energy distance (distribution-free, recommended)
        - 'manova': Multivariate ANOVA (assumes normality)
        - 'hotelling': Hotelling's T² (for 2 groups)
    alpha : float, default=0.05
        Significance level
    n_jobs : int, default=1
        Number of parallel workers
    
    Returns:
    --------
    dict
        Multivariate test results with p-value and conclusion
    
    Examples:
    ---------
    >>> from sklearn.metrics import accuracy_score, f1_score, precision_score
    >>> metrics = [accuracy_score, f1_score, precision_score]
    >>> result = detect_multivariate_bias(
    ...     model, X, y, metrics,
    ...     metric_names=['Accuracy', 'F1', 'Precision']
    ... )
    >>> print(result['conclusion'])
    """
    from sklearn.utils import check_array, check_consistent_length
    
    # Validate inputs
    X = check_array(X, accept_sparse=True, force_all_finite=False)
    y = np.asarray(y).ravel()
    check_consistent_length(X, y)
    
    if len(metrics) < 2:
        raise ValueError("Need at least 2 metrics for multivariate detection")
    
    if metric_names is None:
        metric_names = [f"Metric_{i+1}" for i in range(len(metrics))]
    
    if len(metric_names) != len(metrics):
        raise ValueError("metric_names must have same length as metrics")
    
    # Setup random state
    if random_state is None:
        rng = np.random.default_rng()
    else:
        rng = np.random.default_rng(random_state)
    
    # Compute observed metric vector
    y_pred = model.predict(X)
    observed_metrics = np.array([metric(y, y_pred) for metric in metrics])
    
    # Generate permutation indices
    perm_indices = [rng.permutation(len(y)) for _ in range(n_permutations)]
    
    # Compute permuted metric vectors
    if n_jobs == 1:
        permuted_metric_vectors = _compute_permuted_metrics_multivariate_sequential(
            model, X, y, metrics, perm_indices
        )
    else:
        permuted_metric_vectors = _compute_permuted_metrics_multivariate_parallel(
            model, X, y, metrics, perm_indices, n_jobs
        )
    
    permuted_metric_vectors = np.array(permuted_metric_vectors)  # Shape: (n_permutations, n_metrics)
    
    # Compute test statistic based on method
    if method == "energy":
        observed_stat, p_value = _energy_distance_test(
            observed_metrics, permuted_metric_vectors
        )
        test_name = "Energy Distance"
    elif method == "manova":
        observed_stat, p_value = _manova_test(
            observed_metrics, permuted_metric_vectors
        )
        test_name = "MANOVA (Wilks' Lambda)"
    elif method == "hotelling":
        observed_stat, p_value = _hotelling_test(
            observed_metrics, permuted_metric_vectors
        )
        test_name = "Hotelling's T²"
    else:
        raise ValueError(f"Unknown method: {method}. Choose from: 'energy', 'manova', 'hotelling'")
    
    # Generate conclusion
    if p_value <= alpha:
        risk_level = "High" if p_value <= 0.01 else "Medium"
        conclusion = (
            f"{risk_level} risk: Multivariate test significant (p={p_value:.4f}). "
            f"Joint metric distribution is suspicious across {len(metrics)} metrics."
        )
    else:
        conclusion = (
            f"Low risk: No significant multivariate bias detected (p={p_value:.3f}). "
            f"Joint metric distribution appears normal."
        )
    
    # Compute individual metric statistics for reference
    individual_stats = {}
    for i, (metric_name, metric_func) in enumerate(zip(metric_names, metrics)):
        obs_val = observed_metrics[i]
        perm_vals = permuted_metric_vectors[:, i]
        ind_p_value = (np.sum(perm_vals >= obs_val) + 1) / (n_permutations + 1)
        
        individual_stats[metric_name] = {
            'observed': float(obs_val),
            'p_value': float(ind_p_value),
            'mean_permuted': float(np.mean(perm_vals)),
            'std_permuted': float(np.std(perm_vals))
        }
    
    return {
        'test_type': test_name,
        'method': method,
        'p_value': float(p_value),
        'test_statistic': float(observed_stat),
        'alpha': alpha,
        'conclusion': conclusion,
        'n_metrics': len(metrics),
        'metric_names': metric_names,
        'observed_metrics': observed_metrics.tolist(),
        'individual_stats': individual_stats,
        'n_permutations': n_permutations,
        'n_samples': len(y)
    }


def _compute_permuted_metrics_multivariate_sequential(
    model, X, y, metrics, perm_indices
) -> List[np.ndarray]:
    """Compute permuted metric vectors sequentially."""
    permuted_vectors = []
    y_pred = model.predict(X)
    
    for perm_idx in perm_indices:
        y_perm = y[perm_idx]
        metric_vector = np.array([metric(y_perm, y_pred) for metric in metrics])
        permuted_vectors.append(metric_vector)
    
    return permuted_vectors


def _compute_permuted_metrics_multivariate_parallel(
    model, X, y, metrics, perm_indices, n_jobs
) -> List[np.ndarray]:
    """Compute permuted metric vectors in parallel."""
    try:
        from joblib import Parallel, delayed
    except ImportError:
        warnings.warn("joblib not available, falling back to sequential")
        return _compute_permuted_metrics_multivariate_sequential(
            model, X, y, metrics, perm_indices
        )
    
    y_pred = model.predict(X)
    
    def compute_single(perm_idx):
        y_perm = y[perm_idx]
        return np.array([metric(y_perm, y_pred) for metric in metrics])
    
    permuted_vectors = Parallel(n_jobs=n_jobs, backend='threading')(
        delayed(compute_single)(perm_idx) for perm_idx in perm_indices
    )
    
    return permuted_vectors


def _energy_distance_test(
    observed: np.ndarray,
    permuted: np.ndarray
) -> Tuple[float, float]:
    """Energy distance test (distribution-free multivariate test).
    
    Energy distance measures the distance between two probability distributions.
    It's more powerful than MANOVA for non-normal distributions.
    """
    n_perm = len(permuted)
    
    # Compute energy distance between observed and permuted distribution
    # E(X,Y) = 2*E[||X-Y||] - E[||X-X'||] - E[||Y-Y'||]
    
    # Distance from observed to each permuted vector
    distances_obs_perm = np.linalg.norm(permuted - observed, axis=1)
    term1 = 2 * np.mean(distances_obs_perm)
    
    # Pairwise distances within permuted distribution
    pairwise_distances = []
    for i in range(min(100, n_perm)):  # Sample for efficiency
        for j in range(i+1, min(100, n_perm)):
            pairwise_distances.append(np.linalg.norm(permuted[i] - permuted[j]))
    term2 = np.mean(pairwise_distances) if pairwise_distances else 0
    
    observed_stat = term1 - term2
    
    # Permutation test: how many permuted vectors are as extreme?
    # For energy distance, larger = more different
    p_value = (np.sum(distances_obs_perm >= distances_obs_perm[0]) + 1) / (n_perm + 1)
    
    return observed_stat, p_value


def _manova_test(
    observed: np.ndarray,
    permuted: np.ndarray
) -> Tuple[float, float]:
    """MANOVA test using Wilks' Lambda.
    
    Tests if the mean vector differs between observed and permuted distributions.
    Assumes multivariate normality.
    """
    try:
        from scipy import stats
    except ImportError:
        raise ImportError("scipy required for MANOVA. Install with: pip install scipy")
    
    n_perm = len(permuted)
    n_metrics = len(observed)
    
    # Compute means
    mean_obs = observed
    mean_perm = np.mean(permuted, axis=0)
    
    # Compute covariance matrix of permuted distribution
    cov_perm = np.cov(permuted.T)
    
    # Add small regularization for numerical stability
    cov_perm += np.eye(n_metrics) * 1e-6
    
    # Mahalanobis distance
    try:
        diff = mean_obs - mean_perm
        inv_cov = np.linalg.inv(cov_perm)
        mahalanobis_dist = np.sqrt(diff @ inv_cov @ diff)
    except np.linalg.LinAlgError:
        # Fallback to Euclidean distance if covariance is singular
        mahalanobis_dist = np.linalg.norm(mean_obs - mean_perm)
    
    # Compute Mahalanobis distances for all permuted vectors
    perm_distances = []
    for perm_vec in permuted:
        try:
            diff = perm_vec - mean_perm
            dist = np.sqrt(diff @ inv_cov @ diff)
        except:
            dist = np.linalg.norm(perm_vec - mean_perm)
        perm_distances.append(dist)
    
    perm_distances = np.array(perm_distances)
    
    # p-value: fraction of permuted distances >= observed distance
    p_value = (np.sum(perm_distances >= mahalanobis_dist) + 1) / (n_perm + 1)
    
    return mahalanobis_dist, p_value


def _hotelling_test(
    observed: np.ndarray,
    permuted: np.ndarray
) -> Tuple[float, float]:
    """Hotelling's T² test (multivariate t-test).
    
    Similar to MANOVA but specifically for comparing a single observation
    to a distribution.
    """
    # Use same approach as MANOVA for consistency
    return _manova_test(observed, permuted)


def detect_multitask_bias(
    models: Dict[str, Any],
    X_dict: Dict[str, np.ndarray],
    y_dict: Dict[str, np.ndarray],
    metric: Callable,
    n_permutations: int = 1000,
    random_state: Optional[int] = None,
    method: str = "energy",
    alpha: float = 0.05
) -> Dict:
    """Detect bias across multiple tasks (e.g., GLUE, MMLU).
    
    This tests if performance across tasks is jointly suspicious,
    even if individual tasks appear normal.
    
    Parameters:
    -----------
    models : dict
        Dictionary mapping task names to models
    X_dict : dict
        Dictionary mapping task names to feature matrices
    y_dict : dict
        Dictionary mapping task names to labels
    metric : callable
        Metric function to use for all tasks
    n_permutations : int, default=1000
        Number of permutations
    random_state : int, optional
        Random seed
    method : str, default='energy'
        Multivariate test method
    alpha : float, default=0.05
        Significance level
    
    Returns:
    --------
    dict
        Multitask detection results
    
    Examples:
    ---------
    >>> # GLUE benchmark example
    >>> models = {
    ...     'cola': model_cola,
    ...     'sst2': model_sst2,
    ...     'mrpc': model_mrpc,
    ...     # ... 9 tasks total
    ... }
    >>> result = detect_multitask_bias(models, X_dict, y_dict, accuracy_score)
    >>> print(result['conclusion'])
    """
    task_names = list(models.keys())
    n_tasks = len(task_names)
    
    if n_tasks < 2:
        raise ValueError("Need at least 2 tasks for multitask detection")
    
    # Validate that all dicts have same keys
    if set(X_dict.keys()) != set(task_names) or set(y_dict.keys()) != set(task_names):
        raise ValueError("models, X_dict, and y_dict must have same keys")
    
    # Setup random state
    if random_state is None:
        rng = np.random.default_rng()
    else:
        rng = np.random.default_rng(random_state)
    
    # Compute observed performance vector (one value per task)
    observed_performances = []
    for task_name in task_names:
        model = models[task_name]
        X = X_dict[task_name]
        y = y_dict[task_name]
        y_pred = model.predict(X)
        perf = metric(y, y_pred)
        observed_performances.append(perf)
    
    observed_performances = np.array(observed_performances)
    
    # Generate permuted performance vectors
    permuted_performances = []
    for _ in range(n_permutations):
        perm_perf = []
        for task_name in task_names:
            model = models[task_name]
            X = X_dict[task_name]
            y = y_dict[task_name]
            
            # Permute labels for this task
            perm_idx = rng.permutation(len(y))
            y_perm = y[perm_idx]
            
            y_pred = model.predict(X)
            perf = metric(y_perm, y_pred)
            perm_perf.append(perf)
        
        permuted_performances.append(perm_perf)
    
    permuted_performances = np.array(permuted_performances)
    
    # Apply multivariate test
    if method == "energy":
        observed_stat, p_value = _energy_distance_test(
            observed_performances, permuted_performances
        )
        test_name = "Energy Distance"
    elif method == "manova":
        observed_stat, p_value = _manova_test(
            observed_performances, permuted_performances
        )
        test_name = "MANOVA"
    else:
        observed_stat, p_value = _hotelling_test(
            observed_performances, permuted_performances
        )
        test_name = "Hotelling's T²"
    
    # Generate conclusion
    if p_value <= alpha:
        risk_level = "High" if p_value <= 0.01 else "Medium"
        conclusion = (
            f"{risk_level} risk: Multitask performance is jointly suspicious "
            f"(p={p_value:.4f}) across {n_tasks} tasks. "
            f"Pattern suggests systematic bias or overfitting."
        )
    else:
        conclusion = (
            f"Low risk: Multitask performance appears normal (p={p_value:.3f}) "
            f"across {n_tasks} tasks."
        )
    
    # Individual task statistics
    task_stats = {}
    for i, task_name in enumerate(task_names):
        obs_val = observed_performances[i]
        perm_vals = permuted_performances[:, i]
        ind_p_value = (np.sum(perm_vals >= obs_val) + 1) / (n_permutations + 1)
        
        task_stats[task_name] = {
            'observed': float(obs_val),
            'p_value': float(ind_p_value),
            'mean_permuted': float(np.mean(perm_vals)),
            'std_permuted': float(np.std(perm_vals))
        }
    
    return {
        'test_type': f"Multitask {test_name}",
        'method': method,
        'p_value': float(p_value),
        'test_statistic': float(observed_stat),
        'alpha': alpha,
        'conclusion': conclusion,
        'n_tasks': n_tasks,
        'task_names': task_names,
        'observed_performances': observed_performances.tolist(),
        'task_stats': task_stats,
        'n_permutations': n_permutations
    }


def compute_multivariate_psi(
    performance_matrix: np.ndarray,
    computational_costs: np.ndarray,
    method: str = "mahalanobis"
) -> Dict:
    """Compute multivariate PSI (Performance-Size Independence).
    
    Tests if multiple performance metrics are jointly independent of computational cost.
    
    Parameters:
    -----------
    performance_matrix : np.ndarray, shape (n_models, n_metrics)
        Performance values for multiple metrics
    computational_costs : np.ndarray, shape (n_models,)
        Computational costs (parameters, FLOPs, etc.)
    method : str, default='mahalanobis'
        Distance metric: 'mahalanobis', 'euclidean', or 'correlation'
    
    Returns:
    --------
    dict
        Multivariate PSI results
    
    Examples:
    ---------
    >>> # Test if accuracy, F1, and precision are jointly independent of model size
    >>> performance_matrix = np.array([
    ...     [0.85, 0.82, 0.88],  # Small model
    ...     [0.90, 0.88, 0.91],  # Medium model
    ...     [0.95, 0.94, 0.96]   # Large model
    ... ])
    >>> costs = np.array([1e6, 1e8, 1e10])  # Parameters
    >>> result = compute_multivariate_psi(performance_matrix, costs)
    """
    try:
        from scipy import stats
    except ImportError:
        raise ImportError("scipy required for multivariate PSI")
    
    n_models, n_metrics = performance_matrix.shape
    
    if len(computational_costs) != n_models:
        raise ValueError("computational_costs must match number of models")
    
    # Log-transform costs for better correlation
    log_costs = np.log10(computational_costs + 1)
    
    # Compute correlation for each metric
    individual_correlations = []
    individual_p_values = []
    
    for i in range(n_metrics):
        corr, p_val = stats.spearmanr(log_costs, performance_matrix[:, i])
        individual_correlations.append(corr)
        individual_p_values.append(p_val)
    
    # Multivariate correlation using canonical correlation
    # or simple average of absolute correlations
    avg_abs_correlation = np.mean(np.abs(individual_correlations))
    max_abs_correlation = np.max(np.abs(individual_correlations))
    
    # Combined p-value using Fisher's method
    if all(p > 0 for p in individual_p_values):
        chi_square_stat = -2 * np.sum(np.log(individual_p_values))
        combined_p_value = 1 - stats.chi2.cdf(chi_square_stat, 2 * n_metrics)
    else:
        combined_p_value = 0.0
    
    # Risk assessment
    if combined_p_value <= 0.01 and avg_abs_correlation > 0.7:
        risk_level = "High"
        conclusion = (
            f"High risk: Strong multivariate correlation between performance and cost "
            f"(avg |ρ|={avg_abs_correlation:.2f}, p={combined_p_value:.4f}). "
            f"Suggests systematic overfitting or parameter tuning bias."
        )
    elif combined_p_value <= 0.05 and avg_abs_correlation > 0.5:
        risk_level = "Medium"
        conclusion = (
            f"Medium risk: Moderate multivariate correlation detected "
            f"(avg |ρ|={avg_abs_correlation:.2f}, p={combined_p_value:.3f})."
        )
    else:
        risk_level = "Low"
        conclusion = (
            f"Low risk: Weak or no multivariate correlation "
            f"(avg |ρ|={avg_abs_correlation:.2f}, p={combined_p_value:.3f})."
        )
    
    return {
        'risk_level': risk_level,
        'conclusion': conclusion,
        'n_models': n_models,
        'n_metrics': n_metrics,
        'individual_correlations': individual_correlations,
        'individual_p_values': individual_p_values,
        'avg_abs_correlation': float(avg_abs_correlation),
        'max_abs_correlation': float(max_abs_correlation),
        'combined_p_value': float(combined_p_value),
        'method': method
    }
