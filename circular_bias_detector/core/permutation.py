"""
Enhanced permutation testing with parallel processing and proper RNG handling.

This module provides permutation-based statistical testing with:
- Configurable parallel backends (threads/processes)
- Proper random number generation for reproducibility
- Optional retrain-null mode for conservative testing
- Support for probability-based metrics (AUC, logloss)
"""

import numpy as np
from typing import Optional, Dict, Callable, Union, Literal, Any, List
import warnings
from joblib import Parallel, delayed
from functools import partial


def _permutation_worker(
    seed: int,
    performance_matrix: np.ndarray,
    constraint_matrix: np.ndarray,
    metric_func: Callable,
    **metric_kwargs
) -> float:
    """
    Worker function for parallel permutation testing.
    
    Parameters
    ----------
    seed : int
        Random seed for this permutation
    performance_matrix : np.ndarray
        Original performance matrix
    constraint_matrix : np.ndarray
        Original constraint matrix
    metric_func : callable
        Metric computation function
    **metric_kwargs
        Additional arguments for metric function
        
    Returns
    -------
    float
        Computed metric value for this permutation
    """
    # Create independent RNG for this worker
    rng = np.random.RandomState(seed)
    
    T = performance_matrix.shape[0]
    perm_indices = rng.permutation(T)
    
    perf_perm = performance_matrix[perm_indices, :]
    const_perm = constraint_matrix[perm_indices, :] if constraint_matrix is not None else None
    
    try:
        # Check function signature to determine how to call it
        import inspect
        sig = inspect.signature(metric_func)
        params = list(sig.parameters.keys())
        
        # If function takes 2+ positional args, pass both matrices
        if len(params) >= 2 and const_perm is not None:
            return metric_func(perf_perm, const_perm, **metric_kwargs)
        else:
            # Otherwise just pass performance matrix
            return metric_func(perf_perm, **metric_kwargs)
    except Exception as e:
        warnings.warn(f"Permutation failed with seed {seed}: {e}")
        return np.nan


def permutation_test(
    performance_matrix: np.ndarray,
    constraint_matrix: np.ndarray,
    metric_func: Callable,
    n_permutations: int = 1000,
    random_seed: Optional[int] = None,
    n_jobs: int = 1,
    backend: Literal['threads', 'processes'] = 'threads',
    verbose: int = 0,
    **metric_kwargs
) -> Dict[str, Any]:
    """
    Perform permutation test with parallel processing support.
    
    Parameters
    ----------
    performance_matrix : np.ndarray
        Shape (T, K) where T is time periods, K is algorithms
    constraint_matrix : np.ndarray
        Shape (T, p) where T is time periods, p is constraint types
    metric_func : callable
        Function to compute metric, signature: func(perf, const, **kwargs) -> float
    n_permutations : int, default=1000
        Number of permutations
    random_seed : int, optional
        Random seed for reproducibility
    n_jobs : int, default=1
        Number of parallel jobs. -1 uses all processors
    backend : {'threads', 'processes'}, default='threads'
        Parallel backend:
        - 'threads': Thread-based parallelism (good for GIL-releasing operations)
        - 'processes': Process-based parallelism (better for pure Python, requires picklable objects)
    verbose : int, default=0
        Verbosity level for joblib
    **metric_kwargs
        Additional arguments passed to metric_func
        
    Returns
    -------
    dict
        Results with keys:
        - observed: Observed metric value
        - permuted_values: Array of permuted metric values
        - p_value: Two-tailed p-value
        - ci_lower: Lower confidence bound (2.5th percentile)
        - ci_upper: Upper confidence bound (97.5th percentile)
        - n_permutations: Number of successful permutations
        
    Examples
    --------
    >>> from circular_bias_detector.core.metrics import compute_psi
    >>> perf = np.random.rand(10, 3)
    >>> const = np.random.rand(10, 2)
    >>> results = permutation_test(perf, const, compute_psi, n_permutations=1000)
    >>> print(f"p-value: {results['p_value']:.4f}")
    
    Notes
    -----
    - Thread backend is recommended for most cases (default)
    - Process backend requires metric_func and data to be picklable
    - Random seeds are pre-generated to ensure reproducibility across backends
    """
    # Compute observed metric
    # Check function signature to determine how to call it
    import inspect
    sig = inspect.signature(metric_func)
    params = list(sig.parameters.keys())
    
    # If function takes 2+ positional args, pass both matrices
    if len(params) >= 2 and constraint_matrix is not None:
        observed = metric_func(performance_matrix, constraint_matrix, **metric_kwargs)
    else:
        # Otherwise just pass performance matrix
        observed = metric_func(performance_matrix, **metric_kwargs)
    
    # Generate all random seeds upfront for reproducibility
    if random_seed is not None:
        master_rng = np.random.RandomState(random_seed)
    else:
        master_rng = np.random.RandomState()
    
    # Generate unique seeds for each permutation
    seeds = master_rng.randint(0, 2**31 - 1, size=n_permutations)
    
    # Parallel execution
    if n_jobs == 1:
        # Sequential execution (no parallelism)
        permuted_values = []
        for seed in seeds:
            val = _permutation_worker(
                seed, performance_matrix, constraint_matrix, 
                metric_func, **metric_kwargs
            )
            permuted_values.append(val)
    else:
        # Parallel execution
        joblib_backend = 'loky' if backend == 'processes' else 'threading'
        
        permuted_values = Parallel(n_jobs=n_jobs, backend=joblib_backend, verbose=verbose)(
            delayed(_permutation_worker)(
                seed, performance_matrix, constraint_matrix,
                metric_func, **metric_kwargs
            )
            for seed in seeds
        )
    
    # Filter out NaN values
    permuted_values = np.array([v for v in permuted_values if not np.isnan(v)])
    
    if len(permuted_values) == 0:
        raise ValueError("All permutations failed. Check metric_func and data.")
    
    # Compute p-value (two-tailed)
    p_value = np.mean(np.abs(permuted_values - np.mean(permuted_values)) >= 
                      np.abs(observed - np.mean(permuted_values)))
    
    # Confidence intervals
    ci_lower = np.percentile(permuted_values, 2.5)
    ci_upper = np.percentile(permuted_values, 97.5)
    
    return {
        'observed': float(observed),
        'permuted_values': permuted_values,
        'p_value': float(p_value),
        'ci_lower': float(ci_lower),
        'ci_upper': float(ci_upper),
        'n_permutations': len(permuted_values),
        'n_failed': n_permutations - len(permuted_values)
    }


def _retrain_permutation_worker(
    seed: int,
    X_train: np.ndarray,
    y_train: np.ndarray,
    X_test: np.ndarray,
    y_test: np.ndarray,
    model_factory: Callable,
    metric_func: Callable,
    stratify_groups: Optional[np.ndarray] = None
) -> float:
    """
    Worker for retrain-null permutation testing.
    
    Parameters
    ----------
    seed : int
        Random seed for this permutation
    X_train, y_train : np.ndarray
        Training data
    X_test, y_test : np.ndarray
        Test data
    model_factory : callable
        Function that returns a new model instance
    metric_func : callable
        Metric function: func(y_true, y_pred) -> float
    stratify_groups : np.ndarray, optional
        Groups for stratified permutation
        
    Returns
    -------
    float
        Metric value after retraining on permuted labels
    """
    rng = np.random.RandomState(seed)
    
    # Permute training labels
    if stratify_groups is not None:
        # Stratified permutation within groups
        y_perm = y_train.copy()
        for group in np.unique(stratify_groups):
            mask = stratify_groups == group
            indices = np.where(mask)[0]
            y_perm[indices] = rng.permutation(y_train[indices])
    else:
        # Simple permutation
        y_perm = rng.permutation(y_train)
    
    try:
        # Train model on permuted data
        model = model_factory()
        model.fit(X_train, y_perm)
        
        # Evaluate on test set
        y_pred = model.predict(X_test)
        
        return metric_func(y_test, y_pred)
    except Exception as e:
        warnings.warn(f"Retrain permutation failed with seed {seed}: {e}")
        return np.nan


def retrain_null_test(
    X_train: np.ndarray,
    y_train: np.ndarray,
    X_test: np.ndarray,
    y_test: np.ndarray,
    model_factory: Callable,
    metric_func: Callable,
    n_permutations: int = 100,
    random_seed: Optional[int] = None,
    n_jobs: int = 1,
    backend: Literal['threads', 'processes'] = 'processes',
    stratify_groups: Optional[np.ndarray] = None,
    verbose: int = 0
) -> Dict[str, Any]:
    """
    Perform retrain-null permutation test (conservative, computationally expensive).
    
    This method retrains the model on each permutation of the training labels,
    providing a more conservative null distribution but at much higher computational cost.
    
    Parameters
    ----------
    X_train, y_train : np.ndarray
        Training data and labels
    X_test, y_test : np.ndarray
        Test data and labels
    model_factory : callable
        Function that returns a new untrained model instance
        Example: lambda: RandomForestClassifier(n_estimators=100)
    metric_func : callable
        Metric function with signature: func(y_true, y_pred) -> float
        Example: sklearn.metrics.accuracy_score
    n_permutations : int, default=100
        Number of permutations (keep low due to computational cost)
    random_seed : int, optional
        Random seed for reproducibility
    n_jobs : int, default=1
        Number of parallel jobs
    backend : {'threads', 'processes'}, default='processes'
        Parallel backend (processes recommended for model training)
    stratify_groups : np.ndarray, optional
        Group labels for stratified permutation
    verbose : int, default=0
        Verbosity level
        
    Returns
    -------
    dict
        Results with keys:
        - observed: Observed metric on original data
        - permuted_values: Array of metrics from permuted retraining
        - p_value: One-tailed p-value (proportion of null >= observed)
        - ci_lower, ci_upper: Confidence bounds
        - n_permutations: Number of successful permutations
        
    Examples
    --------
    >>> from sklearn.ensemble import RandomForestClassifier
    >>> from sklearn.metrics import accuracy_score
    >>> model_factory = lambda: RandomForestClassifier(n_estimators=50, random_state=42)
    >>> results = retrain_null_test(
    ...     X_train, y_train, X_test, y_test,
    ...     model_factory, accuracy_score,
    ...     n_permutations=100, n_jobs=-1
    ... )
    
    Warnings
    --------
    This method is computationally expensive. For n_permutations=100 and a model
    that takes 1 second to train, this will take ~100 seconds (or less with parallelism).
    Consider using the standard permutation_test for faster results.
    """
    # Compute observed metric
    model_obs = model_factory()
    model_obs.fit(X_train, y_train)
    y_pred_obs = model_obs.predict(X_test)
    observed = metric_func(y_test, y_pred_obs)
    
    # Generate random seeds
    if random_seed is not None:
        master_rng = np.random.RandomState(random_seed)
    else:
        master_rng = np.random.RandomState()
    
    seeds = master_rng.randint(0, 2**31 - 1, size=n_permutations)
    
    # Parallel execution
    if n_jobs == 1:
        permuted_values = []
        for seed in seeds:
            val = _retrain_permutation_worker(
                seed, X_train, y_train, X_test, y_test,
                model_factory, metric_func, stratify_groups
            )
            permuted_values.append(val)
    else:
        joblib_backend = 'loky' if backend == 'processes' else 'threading'
        
        permuted_values = Parallel(n_jobs=n_jobs, backend=joblib_backend, verbose=verbose)(
            delayed(_retrain_permutation_worker)(
                seed, X_train, y_train, X_test, y_test,
                model_factory, metric_func, stratify_groups
            )
            for seed in seeds
        )
    
    # Filter NaN values
    permuted_values = np.array([v for v in permuted_values if not np.isnan(v)])
    
    if len(permuted_values) == 0:
        raise ValueError("All retrain permutations failed.")
    
    # One-tailed p-value: proportion of null >= observed
    p_value = np.mean(permuted_values >= observed)
    
    # Confidence intervals
    ci_lower = np.percentile(permuted_values, 2.5)
    ci_upper = np.percentile(permuted_values, 97.5)
    
    return {
        'observed': float(observed),
        'permuted_values': permuted_values,
        'p_value': float(p_value),
        'ci_lower': float(ci_lower),
        'ci_upper': float(ci_upper),
        'n_permutations': len(permuted_values),
        'n_failed': n_permutations - len(permuted_values)
    }


def adaptive_permutation_test(
    performance_matrix: np.ndarray,
    constraint_matrix: np.ndarray,
    metric_func: Callable,
    max_permutations: int = 10000,
    min_permutations: int = 100,
    alpha: float = 0.05,
    precision: float = 0.01,
    random_seed: Optional[int] = None,
    n_jobs: int = 1,
    backend: Literal['threads', 'processes'] = 'threads',
    verbose: int = 0,
    **metric_kwargs
) -> Dict[str, Any]:
    """
    Adaptive permutation test that stops early when p-value is stable.
    
    This method performs permutations adaptively, stopping when the p-value
    estimate has converged within the specified precision. This can significantly
    reduce computation time for large datasets.
    
    Parameters
    ----------
    performance_matrix, constraint_matrix : np.ndarray
        Input matrices
    metric_func : callable
        Metric computation function
    max_permutations : int, default=10000
        Maximum number of permutations
    min_permutations : int, default=100
        Minimum permutations before checking convergence
    alpha : float, default=0.05
        Significance level for early stopping
    precision : float, default=0.01
        Required precision for p-value (stop when SE < precision)
    random_seed : int, optional
        Random seed
    n_jobs : int, default=1
        Number of parallel jobs
    backend : {'threads', 'processes'}, default='threads'
        Parallel backend
    verbose : int, default=0
        Verbosity level
    **metric_kwargs
        Additional arguments for metric_func
        
    Returns
    -------
    dict
        Results with additional key 'converged' indicating if test converged
        
    Notes
    -----
    Early stopping criteria:
    - Standard error of p-value < precision
    - Or max_permutations reached
    """
    # Check function signature to determine how to call it
    import inspect
    sig = inspect.signature(metric_func)
    params = list(sig.parameters.keys())
    
    # If function takes 2+ positional args, pass both matrices
    if len(params) >= 2 and constraint_matrix is not None:
        observed = metric_func(performance_matrix, constraint_matrix, **metric_kwargs)
    else:
        # Otherwise just pass performance matrix
        observed = metric_func(performance_matrix, **metric_kwargs)
    
    if random_seed is not None:
        master_rng = np.random.RandomState(random_seed)
    else:
        master_rng = np.random.RandomState()
    
    # Batch processing
    batch_size = min(min_permutations, 100)
    permuted_values = []
    n_done = 0
    converged = False
    
    while n_done < max_permutations:
        # Generate seeds for this batch
        n_batch = min(batch_size, max_permutations - n_done)
        seeds = master_rng.randint(0, 2**31 - 1, size=n_batch)
        
        # Execute batch
        if n_jobs == 1:
            batch_values = [
                _permutation_worker(seed, performance_matrix, constraint_matrix, 
                                   metric_func, **metric_kwargs)
                for seed in seeds
            ]
        else:
            joblib_backend = 'loky' if backend == 'processes' else 'threading'
            batch_values = Parallel(n_jobs=n_jobs, backend=joblib_backend, verbose=verbose)(
                delayed(_permutation_worker)(
                    seed, performance_matrix, constraint_matrix,
                    metric_func, **metric_kwargs
                )
                for seed in seeds
            )
        
        # Add to results
        permuted_values.extend([v for v in batch_values if not np.isnan(v)])
        n_done += n_batch
        
        # Check convergence after minimum permutations
        if n_done >= min_permutations:
            perm_array = np.array(permuted_values)
            p_current = np.mean(np.abs(perm_array - np.mean(perm_array)) >= 
                               np.abs(observed - np.mean(perm_array)))
            
            # Standard error of p-value
            se_p = np.sqrt(p_current * (1 - p_current) / len(permuted_values))
            
            if se_p < precision:
                converged = True
                if verbose > 0:
                    print(f"Converged after {n_done} permutations (SE={se_p:.4f})")
                break
    
    permuted_values = np.array(permuted_values)
    
    p_value = np.mean(np.abs(permuted_values - np.mean(permuted_values)) >= 
                      np.abs(observed - np.mean(permuted_values)))
    
    ci_lower = np.percentile(permuted_values, 2.5)
    ci_upper = np.percentile(permuted_values, 97.5)
    
    return {
        'observed': float(observed),
        'permuted_values': permuted_values,
        'p_value': float(p_value),
        'ci_lower': float(ci_lower),
        'ci_upper': float(ci_upper),
        'n_permutations': len(permuted_values),
        'converged': converged,
        'max_permutations': max_permutations
    }
