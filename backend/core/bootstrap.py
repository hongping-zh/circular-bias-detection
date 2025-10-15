"""
Bootstrap Confidence Intervals for Bias Indicators

Implements bootstrap resampling to compute confidence intervals
and statistical significance for PSI, CCS, and ρ_PC.

Bootstrap Method:
1. Resample data with replacement (n_iterations times)
2. Compute indicator for each resample
3. Calculate percentile-based confidence intervals
4. Determine statistical significance

Advantages:
- Non-parametric (no distribution assumptions)
- Robust to outliers
- Provides uncertainty quantification
"""

import numpy as np
import pandas as pd
from typing import Dict, Tuple, List
from .psi_calculator import compute_psi
from .ccs_calculator import compute_ccs
from .rho_pc_calculator import compute_rho_pc


def bootstrap_indicators(
    data: pd.DataFrame,
    n_iterations: int = 1000,
    confidence: float = 0.95,
    random_seed: int = None
) -> Dict:
    """
    Compute bootstrap confidence intervals for all three indicators.
    
    Args:
        data: Evaluation data
        n_iterations: Number of bootstrap samples (default 1000)
        confidence: Confidence level (default 0.95 for 95% CI)
        random_seed: Random seed for reproducibility
    
    Returns:
        Dictionary with bootstrap results for PSI, CCS, and ρ_PC
    
    Example:
        >>> df = pd.read_csv('data.csv')
        >>> results = bootstrap_indicators(df, n_iterations=1000)
        >>> print(results['psi']['ci_lower'], results['psi']['ci_upper'])
    """
    
    if random_seed is not None:
        np.random.seed(random_seed)
    
    n_samples = len(data)
    
    # Storage for bootstrap samples
    psi_samples = []
    ccs_samples = []
    rho_pc_samples = []
    
    # Track failures
    failures = {'psi': 0, 'ccs': 0, 'rho_pc': 0}
    
    print(f"🔄 Running {n_iterations} bootstrap iterations...")
    
    for i in range(n_iterations):
        if (i + 1) % 100 == 0:
            print(f"   Progress: {i+1}/{n_iterations}")
        
        # Resample with replacement
        sample_indices = np.random.choice(n_samples, size=n_samples, replace=True)
        sample_data = data.iloc[sample_indices].reset_index(drop=True)
        
        # Compute PSI
        try:
            psi_result = compute_psi(sample_data)
            psi_samples.append(psi_result['psi_score'])
        except Exception as e:
            failures['psi'] += 1
            psi_samples.append(np.nan)
        
        # Compute CCS
        try:
            ccs_result = compute_ccs(sample_data)
            ccs_samples.append(ccs_result['ccs_score'])
        except Exception as e:
            failures['ccs'] += 1
            ccs_samples.append(np.nan)
        
        # Compute ρ_PC
        try:
            rho_pc_result = compute_rho_pc(sample_data)
            rho_pc_samples.append(rho_pc_result['rho_pc'])
        except Exception as e:
            failures['rho_pc'] += 1
            rho_pc_samples.append(np.nan)
    
    # Remove NaN values
    psi_samples = np.array([x for x in psi_samples if not np.isnan(x)])
    ccs_samples = np.array([x for x in ccs_samples if not np.isnan(x)])
    rho_pc_samples = np.array([x for x in rho_pc_samples if not np.isnan(x)])
    
    # Compute confidence intervals
    alpha = 1 - confidence
    lower_percentile = (alpha / 2) * 100
    upper_percentile = (1 - alpha / 2) * 100
    
    # PSI results
    psi_ci = _compute_ci_stats(psi_samples, lower_percentile, upper_percentile)
    
    # CCS results
    ccs_ci = _compute_ci_stats(ccs_samples, lower_percentile, upper_percentile)
    
    # ρ_PC results
    rho_pc_ci = _compute_ci_stats(rho_pc_samples, lower_percentile, upper_percentile)
    
    # Overall summary
    summary = {
        'n_iterations': n_iterations,
        'confidence_level': confidence,
        'successful_samples': {
            'psi': len(psi_samples),
            'ccs': len(ccs_samples),
            'rho_pc': len(rho_pc_samples)
        },
        'failures': failures
    }
    
    return {
        'psi': psi_ci,
        'ccs': ccs_ci,
        'rho_pc': rho_pc_ci,
        'summary': summary
    }


def _compute_ci_stats(samples: np.ndarray, lower_pct: float, upper_pct: float) -> Dict:
    """
    Compute confidence interval statistics from bootstrap samples.
    
    Args:
        samples: Bootstrap sample values
        lower_pct: Lower percentile
        upper_pct: Upper percentile
    
    Returns:
        Dictionary with CI statistics
    """
    if len(samples) == 0:
        return {
            'mean': 0.0,
            'median': 0.0,
            'std': 0.0,
            'ci_lower': 0.0,
            'ci_upper': 0.0,
            'samples': [],
            'error': 'No valid samples'
        }
    
    mean = np.mean(samples)
    median = np.median(samples)
    std = np.std(samples)
    ci_lower = np.percentile(samples, lower_pct)
    ci_upper = np.percentile(samples, upper_pct)
    
    return {
        'mean': float(mean),
        'median': float(median),
        'std': float(std),
        'ci_lower': float(ci_lower),
        'ci_upper': float(ci_upper),
        'samples': samples.tolist()
    }


def compute_p_value(observed: float, samples: np.ndarray, threshold: float, direction: str = 'greater') -> float:
    """
    Compute p-value from bootstrap samples.
    
    Args:
        observed: Observed value in original data
        samples: Bootstrap sample values
        threshold: Threshold for hypothesis test
        direction: 'greater', 'less', or 'two-sided'
    
    Returns:
        P-value
    
    Example:
        >>> p_val = compute_p_value(0.20, psi_samples, threshold=0.15, direction='greater')
        >>> print(f"P-value for PSI > 0.15: {p_val:.4f}")
    """
    samples = np.array(samples)
    
    if direction == 'greater':
        # H0: indicator <= threshold, H1: indicator > threshold
        p_value = np.mean(samples <= threshold)
    elif direction == 'less':
        # H0: indicator >= threshold, H1: indicator < threshold
        p_value = np.mean(samples >= threshold)
    elif direction == 'two-sided':
        # Two-sided test
        diff = np.abs(samples - threshold)
        obs_diff = np.abs(observed - threshold)
        p_value = np.mean(diff >= obs_diff)
    else:
        raise ValueError(f"Invalid direction: {direction}")
    
    return float(p_value)


def bootstrap_difference(
    data1: pd.DataFrame,
    data2: pd.DataFrame,
    indicator: str = 'psi',
    n_iterations: int = 1000
) -> Dict:
    """
    Bootstrap test for difference between two datasets.
    
    Useful for comparing:
    - Different algorithms
    - Different time periods
    - Treatment vs control
    
    Args:
        data1: First dataset
        data2: Second dataset
        indicator: 'psi', 'ccs', or 'rho_pc'
        n_iterations: Number of bootstrap samples
    
    Returns:
        Dictionary with difference statistics and p-value
    """
    
    # Select calculator
    if indicator == 'psi':
        calc_func = lambda d: compute_psi(d)['psi_score']
    elif indicator == 'ccs':
        calc_func = lambda d: compute_ccs(d)['ccs_score']
    elif indicator == 'rho_pc':
        calc_func = lambda d: compute_rho_pc(d)['rho_pc']
    else:
        raise ValueError(f"Invalid indicator: {indicator}")
    
    # Observed difference
    obs1 = calc_func(data1)
    obs2 = calc_func(data2)
    obs_diff = obs1 - obs2
    
    # Bootstrap
    diff_samples = []
    
    for _ in range(n_iterations):
        # Resample both datasets
        idx1 = np.random.choice(len(data1), size=len(data1), replace=True)
        idx2 = np.random.choice(len(data2), size=len(data2), replace=True)
        
        sample1 = data1.iloc[idx1].reset_index(drop=True)
        sample2 = data2.iloc[idx2].reset_index(drop=True)
        
        try:
            val1 = calc_func(sample1)
            val2 = calc_func(sample2)
            diff_samples.append(val1 - val2)
        except:
            continue
    
    diff_samples = np.array(diff_samples)
    
    # Statistics
    mean_diff = np.mean(diff_samples)
    ci_lower = np.percentile(diff_samples, 2.5)
    ci_upper = np.percentile(diff_samples, 97.5)
    
    # P-value: is difference significant?
    p_value = np.mean(np.abs(diff_samples) >= np.abs(obs_diff))
    
    return {
        'observed_diff': float(obs_diff),
        'mean_diff': float(mean_diff),
        'ci_lower': float(ci_lower),
        'ci_upper': float(ci_upper),
        'p_value': float(p_value),
        'significant': p_value < 0.05,
        'samples': diff_samples.tolist()
    }


# Example usage
if __name__ == "__main__":
    print("=" * 70)
    print("Bootstrap Confidence Intervals - Test Run")
    print("=" * 70)
    
    # Load sample data
    print("\n📂 Loading sample data...")
    try:
        df = pd.read_csv('data/sample_data.csv')
        print(f"✓ Loaded {len(df)} rows")
    except FileNotFoundError:
        print("✗ Creating synthetic data...")
        df = pd.DataFrame({
            'time_period': [1, 1, 2, 2, 3, 3, 4, 4],
            'algorithm': ['A', 'B'] * 4,
            'performance': [0.7, 0.6, 0.72, 0.65, 0.74, 0.67, 0.76, 0.69],
            'constraint_compute': [100, 150, 105, 155, 110, 160, 115, 165],
            'constraint_memory': [8.0, 12.0, 8.5, 12.5, 9.0, 13.0, 9.5, 13.5]
        })
    
    # Compute bootstrap CI
    print("\n🔄 Computing bootstrap confidence intervals...")
    print("   (This may take 10-30 seconds)")
    
    results = bootstrap_indicators(df, n_iterations=1000, confidence=0.95, random_seed=42)
    
    # Display results
    print("\n" + "=" * 70)
    print("BOOTSTRAP RESULTS")
    print("=" * 70)
    
    for indicator in ['psi', 'ccs', 'rho_pc']:
        res = results[indicator]
        
        print(f"\n📊 {indicator.upper()}:")
        print(f"   Mean: {res['mean']:.4f}")
        print(f"   Median: {res['median']:.4f}")
        print(f"   Std Dev: {res['std']:.4f}")
        print(f"   95% CI: [{res['ci_lower']:.4f}, {res['ci_upper']:.4f}]")
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    summary = results['summary']
    print(f"\n✅ Bootstrap completed successfully!")
    print(f"   Total iterations: {summary['n_iterations']}")
    print(f"   Confidence level: {summary['confidence_level']*100:.0f}%")
    print(f"\n   Successful samples:")
    for ind, count in summary['successful_samples'].items():
        print(f"   - {ind.upper()}: {count}/{summary['n_iterations']}")
    
    if any(summary['failures'].values()):
        print(f"\n   ⚠️ Failures:")
        for ind, count in summary['failures'].items():
            if count > 0:
                print(f"   - {ind.upper()}: {count}")
    
    print("\n" + "=" * 70)
    print("TEST COMPLETED")
    print("=" * 70)
