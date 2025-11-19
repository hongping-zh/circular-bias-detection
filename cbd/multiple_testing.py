"""Multiple testing correction utilities for batch circular bias detection."""
from typing import List, Dict, Literal
import numpy as np


def bonferroni_correction(p_values: List[float], alpha: float = 0.05) -> Dict:
    """Apply Bonferroni correction for multiple comparisons.
    
    Parameters:
    -----------
    p_values : list of float
        List of p-values from multiple tests
    alpha : float, default=0.05
        Family-wise error rate
    
    Returns:
    --------
    dict
        Dictionary with corrected alpha, rejected tests, and adjusted p-values
    
    Examples:
    ---------
    >>> p_values = [0.01, 0.03, 0.06, 0.001]
    >>> result = bonferroni_correction(p_values, alpha=0.05)
    >>> print(result['corrected_alpha'])  # 0.0125
    >>> print(result['rejected'])  # [True, False, False, True]
    """
    n_tests = len(p_values)
    corrected_alpha = alpha / n_tests
    rejected = [p <= corrected_alpha for p in p_values]
    adjusted_p_values = [min(p * n_tests, 1.0) for p in p_values]
    
    return {
        "method": "bonferroni",
        "n_tests": n_tests,
        "alpha": alpha,
        "corrected_alpha": corrected_alpha,
        "rejected": rejected,
        "adjusted_p_values": adjusted_p_values,
        "n_rejected": sum(rejected)
    }


def benjamini_hochberg_correction(
    p_values: List[float], 
    alpha: float = 0.05,
    return_critical_values: bool = False
) -> Dict:
    """Apply Benjamini-Hochberg FDR correction for multiple comparisons.
    
    The Benjamini-Hochberg procedure controls the False Discovery Rate (FDR),
    which is less conservative than Bonferroni.
    
    Parameters:
    -----------
    p_values : list of float
        List of p-values from multiple tests
    alpha : float, default=0.05
        False discovery rate
    return_critical_values : bool, default=False
        If True, return critical values for each test
    
    Returns:
    --------
    dict
        Dictionary with rejected tests, adjusted p-values, and critical values
    
    Examples:
    ---------
    >>> p_values = [0.01, 0.03, 0.06, 0.001]
    >>> result = benjamini_hochberg_correction(p_values, alpha=0.05)
    >>> print(result['rejected'])
    """
    n_tests = len(p_values)
    
    # Sort p-values and keep track of original indices
    sorted_indices = np.argsort(p_values)
    sorted_p_values = np.array(p_values)[sorted_indices]
    
    # Compute critical values: (i/m) * alpha
    ranks = np.arange(1, n_tests + 1)
    critical_values = (ranks / n_tests) * alpha
    
    # Find largest i where p(i) <= (i/m) * alpha
    comparisons = sorted_p_values <= critical_values
    if np.any(comparisons):
        max_idx = np.where(comparisons)[0][-1]
        # Reject all hypotheses up to max_idx
        rejected_sorted = np.zeros(n_tests, dtype=bool)
        rejected_sorted[:max_idx + 1] = True
    else:
        rejected_sorted = np.zeros(n_tests, dtype=bool)
    
    # Restore original order
    rejected = np.zeros(n_tests, dtype=bool)
    rejected[sorted_indices] = rejected_sorted
    
    # Compute adjusted p-values (q-values)
    adjusted_p_values = np.zeros(n_tests)
    adjusted_p_values[sorted_indices[-1]] = sorted_p_values[-1]
    for i in range(n_tests - 2, -1, -1):
        adjusted_p_values[sorted_indices[i]] = min(
            sorted_p_values[i] * n_tests / (i + 1),
            adjusted_p_values[sorted_indices[i + 1]]
        )
    adjusted_p_values = np.minimum(adjusted_p_values, 1.0)
    
    result = {
        "method": "benjamini_hochberg",
        "n_tests": n_tests,
        "alpha": alpha,
        "rejected": rejected.tolist(),
        "adjusted_p_values": adjusted_p_values.tolist(),
        "n_rejected": int(np.sum(rejected))
    }
    
    if return_critical_values:
        critical_values_original = np.zeros(n_tests)
        critical_values_original[sorted_indices] = critical_values
        result["critical_values"] = critical_values_original.tolist()
    
    return result


def holm_bonferroni_correction(p_values: List[float], alpha: float = 0.05) -> Dict:
    """Apply Holm-Bonferroni step-down correction for multiple comparisons.
    
    The Holm-Bonferroni method is uniformly more powerful than Bonferroni
    while still controlling family-wise error rate.
    
    Parameters:
    -----------
    p_values : list of float
        List of p-values from multiple tests
    alpha : float, default=0.05
        Family-wise error rate
    
    Returns:
    --------
    dict
        Dictionary with rejected tests and adjusted p-values
    
    Examples:
    ---------
    >>> p_values = [0.01, 0.03, 0.06, 0.001]
    >>> result = holm_bonferroni_correction(p_values, alpha=0.05)
    """
    n_tests = len(p_values)
    
    # Sort p-values and keep track of original indices
    sorted_indices = np.argsort(p_values)
    sorted_p_values = np.array(p_values)[sorted_indices]
    
    # Compute adjusted p-values
    adjusted_p_values_sorted = np.zeros(n_tests)
    for i in range(n_tests):
        adjusted_p_values_sorted[i] = sorted_p_values[i] * (n_tests - i)
    
    # Enforce monotonicity
    for i in range(1, n_tests):
        adjusted_p_values_sorted[i] = max(
            adjusted_p_values_sorted[i],
            adjusted_p_values_sorted[i - 1]
        )
    adjusted_p_values_sorted = np.minimum(adjusted_p_values_sorted, 1.0)
    
    # Restore original order
    adjusted_p_values = np.zeros(n_tests)
    adjusted_p_values[sorted_indices] = adjusted_p_values_sorted
    
    rejected = adjusted_p_values <= alpha
    
    return {
        "method": "holm_bonferroni",
        "n_tests": n_tests,
        "alpha": alpha,
        "rejected": rejected.tolist(),
        "adjusted_p_values": adjusted_p_values.tolist(),
        "n_rejected": int(np.sum(rejected))
    }


def correct_multiple_tests(
    p_values: List[float],
    alpha: float = 0.05,
    method: Literal["bonferroni", "benjamini_hochberg", "holm"] = "benjamini_hochberg"
) -> Dict:
    """Apply multiple testing correction.
    
    Convenience function that dispatches to specific correction methods.
    
    Parameters:
    -----------
    p_values : list of float
        List of p-values from multiple tests
    alpha : float, default=0.05
        Significance level (interpretation depends on method)
    method : {'bonferroni', 'benjamini_hochberg', 'holm'}, default='benjamini_hochberg'
        Correction method to use
    
    Returns:
    --------
    dict
        Dictionary with correction results
    
    Examples:
    ---------
    >>> # Test multiple models/metrics
    >>> results = [detect_bias(...) for ...]
    >>> p_values = [r['p_value'] for r in results]
    >>> correction = correct_multiple_tests(p_values, method='benjamini_hochberg')
    >>> for i, rejected in enumerate(correction['rejected']):
    ...     if rejected:
    ...         print(f"Test {i}: Significant after correction")
    """
    if method == "bonferroni":
        return bonferroni_correction(p_values, alpha)
    elif method == "benjamini_hochberg":
        return benjamini_hochberg_correction(p_values, alpha)
    elif method == "holm":
        return holm_bonferroni_correction(p_values, alpha)
    else:
        raise ValueError(
            f"Unknown method: {method}. "
            f"Choose from: 'bonferroni', 'benjamini_hochberg', 'holm'"
        )


def batch_detect_bias_with_correction(
    models_and_data: List[Dict],
    alpha: float = 0.05,
    correction_method: Literal["bonferroni", "benjamini_hochberg", "holm"] = "benjamini_hochberg",
    **detect_bias_kwargs
) -> Dict:
    """Run detect_bias on multiple models/datasets and apply multiple testing correction.
    
    Parameters:
    -----------
    models_and_data : list of dict
        Each dict should contain: {'model', 'X', 'y', 'metric', 'name' (optional)}
    alpha : float, default=0.05
        Significance level for multiple testing correction
    correction_method : str, default='benjamini_hochberg'
        Multiple testing correction method
    **detect_bias_kwargs
        Additional arguments passed to detect_bias()
    
    Returns:
    --------
    dict
        Dictionary with individual results and correction summary
    
    Examples:
    ---------
    >>> models_and_data = [
    ...     {'model': model1, 'X': X1, 'y': y1, 'metric': accuracy_score, 'name': 'Model 1'},
    ...     {'model': model2, 'X': X2, 'y': y2, 'metric': roc_auc_score, 'name': 'Model 2'},
    ... ]
    >>> batch_result = batch_detect_bias_with_correction(
    ...     models_and_data,
    ...     alpha=0.05,
    ...     correction_method='benjamini_hochberg',
    ...     n_permutations=1000
    ... )
    >>> print(batch_result['correction_summary'])
    """
    from cbd.api import detect_bias
    
    # Run detect_bias on each model/dataset
    individual_results = []
    p_values = []
    
    for i, data in enumerate(models_and_data):
        name = data.get('name', f'Test_{i}')
        result = detect_bias(
            model=data['model'],
            X=data['X'],
            y=data['y'],
            metric=data['metric'],
            alpha=alpha,  # Use same alpha for individual tests
            **detect_bias_kwargs
        )
        result['test_name'] = name
        individual_results.append(result)
        p_values.append(result['p_value'])
    
    # Apply multiple testing correction
    correction = correct_multiple_tests(p_values, alpha, correction_method)
    
    # Add rejection status to individual results
    for i, result in enumerate(individual_results):
        result['rejected_after_correction'] = correction['rejected'][i]
        result['adjusted_p_value'] = correction['adjusted_p_values'][i]
    
    return {
        "individual_results": individual_results,
        "correction_summary": correction,
        "n_tests": len(models_and_data),
        "n_significant_before_correction": sum(
            r['p_value'] <= alpha for r in individual_results
        ),
        "n_significant_after_correction": correction['n_rejected']
    }
