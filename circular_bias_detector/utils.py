"""
Utility functions for data loading, validation, and preprocessing.
"""

import numpy as np
import pandas as pd
from typing import Tuple, Optional, Union, Dict, List
import warnings
import json

def validate_matrices(performance_matrix: np.ndarray,
                     constraint_matrix: np.ndarray,
                     algorithm_params: Optional[np.ndarray] = None) -> None:
    """
    Validate input matrices for bias detection.
    
    Parameters:
    -----------
    performance_matrix : np.ndarray
        Shape (T, K) where T is time periods, K is algorithms
    constraint_matrix : np.ndarray
        Shape (T, p) where T is time periods, p is constraint types
    algorithm_params : np.ndarray, optional
        Shape (T, K, p) where p is parameter dimensions
    
    Raises:
    -------
    ValueError
        If matrices have invalid shapes or contain invalid values
    """
    
    # Check performance matrix
    if not isinstance(performance_matrix, np.ndarray):
        raise ValueError("performance_matrix must be numpy array")
    
    if performance_matrix.ndim != 2:
        raise ValueError("performance_matrix must be 2D (T, K)")
    
    T_perf, K = performance_matrix.shape
    
    if T_perf < 2:
        raise ValueError("Need at least 2 time periods")
    
    if K < 1:
        raise ValueError("Need at least 1 algorithm")
    
    # Check for NaN/inf
    if not np.isfinite(performance_matrix).all():
        raise ValueError("performance_matrix contains NaN or infinite values")
    
    # Check constraint matrix
    if not isinstance(constraint_matrix, np.ndarray):
        raise ValueError("constraint_matrix must be numpy array")
    
    if constraint_matrix.ndim != 2:
        raise ValueError("constraint_matrix must be 2D (T, p)")
    
    T_const, p = constraint_matrix.shape
    
    if T_const != T_perf:
        raise ValueError(f"Time dimension mismatch: performance={T_perf}, constraints={T_const}")
    
    if p < 1:
        raise ValueError("Need at least 1 constraint type")
    
    if not np.isfinite(constraint_matrix).all():
        raise ValueError("constraint_matrix contains NaN or infinite values")
    
    # Check algorithm parameters if provided
    if algorithm_params is not None:
        if not isinstance(algorithm_params, np.ndarray):
            raise ValueError("algorithm_params must be numpy array")
        
        if algorithm_params.ndim != 3:
            raise ValueError("algorithm_params must be 3D (T, K, p)")
        
        T_params, K_params, p_params = algorithm_params.shape
        
        if T_params != T_perf:
            raise ValueError(f"Time dimension mismatch in algorithm_params: {T_params} vs {T_perf}")
        
        if K_params != K:
            raise ValueError(f"Algorithm dimension mismatch in algorithm_params: {K_params} vs {K}")
        
        if not np.isfinite(algorithm_params).all():
            raise ValueError("algorithm_params contains NaN or infinite values")

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load evaluation data from CSV or Excel file.
    
    Parameters:
    -----------
    file_path : str
        Path to data file
        
    Returns:
    --------
    pd.DataFrame
        Loaded data
    """
    
    try:
        if file_path.endswith('.csv'):
            data = pd.read_csv(file_path)
        elif file_path.endswith(('.xlsx', '.xls')):
            data = pd.read_excel(file_path)
        else:
            raise ValueError("Unsupported file format. Use CSV or Excel.")
        
        return data
        
    except Exception as e:
        raise ValueError(f"Error loading data from {file_path}: {e}")

def generate_report(results: dict, output_file: Optional[str] = None) -> str:
    """
    Generate comprehensive bias detection report.
    
    Parameters:
    -----------
    results : dict
        Results from BiasDetector.detect_bias()
    output_file : str, optional
        File path to save report
        
    Returns:
    --------
    str
        Formatted report
    """
    
    report_lines = []
    
    # Header
    report_lines.append("=" * 80)
    report_lines.append("CIRCULAR REASONING BIAS DETECTION REPORT")
    report_lines.append("=" * 80)
    report_lines.append("")
    
    # Executive Summary
    report_lines.append("EXECUTIVE SUMMARY")
    report_lines.append("-" * 40)
    
    if results['overall_bias']:
        report_lines.append("🚨 CIRCULAR REASONING BIAS DETECTED")
        report_lines.append(f"Confidence Level: {results['confidence']:.1%}")
        report_lines.append(f"Indicators Triggered: {results['bias_votes']}/3")
    else:
        report_lines.append("✅ NO SIGNIFICANT BIAS DETECTED")
        report_lines.append(f"Confidence Level: {1-results['confidence']:.1%}")
        report_lines.append(f"Indicators Triggered: {results['bias_votes']}/3")
    
    report_lines.append("")
    
    # Detailed Analysis
    report_lines.append("DETAILED INDICATOR ANALYSIS")
    report_lines.append("-" * 40)
    
    # PSI Analysis
    report_lines.append("1. PARAMETER STABILITY INDEX (PSI)")
    report_lines.append(f"   Score: {results['psi_score']:.6f}")
    report_lines.append(f"   Status: {'⚠️  UNSTABLE PARAMETERS' if results['psi_bias'] else '✅ STABLE PARAMETERS'}")
    report_lines.append(f"   Interpretation: {'High parameter variation suggests iterative tuning based on performance' if results['psi_bias'] else 'Parameters remain consistent across evaluation periods'}")
    report_lines.append("")
    
    # CCS Analysis  
    report_lines.append("2. CONSTRAINT CONSISTENCY SCORE (CCS)")
    report_lines.append(f"   Score: {results['ccs_score']:.6f}")
    report_lines.append(f"   Status: {'⚠️  INCONSISTENT CONSTRAINTS' if results['ccs_bias'] else '✅ CONSISTENT CONSTRAINTS'}")
    report_lines.append(f"   Interpretation: {'Constraints vary significantly, indicating potential manipulation' if results['ccs_bias'] else 'Constraints remain consistent throughout evaluation'}")
    report_lines.append("")
    
    # ρ_PC Analysis
    report_lines.append("3. PERFORMANCE-CONSTRAINT CORRELATION (ρ_PC)")
    report_lines.append(f"   Score: {results['rho_pc_score']:+.6f}")
    report_lines.append(f"   Status: {'⚠️  SUSPICIOUS CORRELATION' if results['rho_pc_bias'] else '✅ INDEPENDENT PERFORMANCE'}")
    report_lines.append(f"   Interpretation: {'Strong correlation suggests constraints adapted to favor performance' if results['rho_pc_bias'] else 'Performance and constraints appear independent'}")
    report_lines.append("")
    
    # Recommendations
    report_lines.append("RECOMMENDATIONS")
    report_lines.append("-" * 40)
    
    if results['overall_bias']:
        report_lines.append("⚠️  IMMEDIATE ACTIONS REQUIRED:")
        report_lines.append("   • Review evaluation protocol for potential circular reasoning")
        report_lines.append("   • Re-evaluate with fixed constraints and parameters")
        report_lines.append("   • Consider independent validation with different evaluation setup")
        report_lines.append("   • Document all protocol changes with justification")
    else:
        report_lines.append("✅ EVALUATION APPEARS SOUND:")
        report_lines.append("   • Current evaluation protocol shows no signs of circular bias")
        report_lines.append("   • Continue monitoring indicators in future evaluations")
        report_lines.append("   • Maintain documentation of evaluation procedures")
    
    report_lines.append("")
    
    # Technical Details
    if 'metadata' in results:
        meta = results['metadata']
        report_lines.append("TECHNICAL DETAILS")
        report_lines.append("-" * 40)
        report_lines.append(f"Time Periods Analyzed: {meta['time_periods']}")
        report_lines.append(f"Algorithms Evaluated: {meta['num_algorithms']}")
        report_lines.append(f"Constraint Types: {meta['num_constraints']}")
        
        if 'algorithm_names' in meta:
            report_lines.append(f"Algorithm Names: {', '.join(meta['algorithm_names'][:5])}")
            if len(meta['algorithm_names']) > 5:
                report_lines.append(f"   ... and {len(meta['algorithm_names'])-5} more")
        
        if 'thresholds' in meta:
            thresh = meta['thresholds']
            report_lines.append("")
            report_lines.append("Detection Thresholds:")
            report_lines.append(f"   PSI Threshold: {thresh['psi']}")
            report_lines.append(f"   CCS Threshold: {thresh['ccs']}")
            report_lines.append(f"   ρ_PC Threshold: ±{thresh['rho_pc']}")
    
    report_lines.append("")
    report_lines.append("=" * 80)
    report_lines.append("Report generated by Circular Bias Detection Framework v1.0")
    report_lines.append("https://doi.org/10.5281/zenodo.17196639")
    report_lines.append("=" * 80)
    
    report_text = "\n".join(report_lines)
    
    # Save to file if requested
    if output_file:
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report_text)
        except Exception as e:
            warnings.warn(f"Could not save report to {output_file}: {e}")
    
    return report_text

def create_synthetic_data(n_time_periods: int = 20,
                         n_algorithms: int = 5,
                         n_constraints: int = 3,
                         bias_intensity: float = 0.0,
                         random_seed: int = 42) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate synthetic evaluation data for testing.
    
    Parameters:
    -----------
    n_time_periods : int
        Number of evaluation time periods
    n_algorithms : int
        Number of algorithms to evaluate
    n_constraints : int
        Number of constraint types
    bias_intensity : float
        Intensity of circular bias to inject (0.0 = no bias, 1.0 = high bias)
    random_seed : int
        Random seed for reproducibility
        
    Returns:
    --------
    tuple
        (performance_matrix, constraint_matrix)
    """
    
    np.random.seed(random_seed)
    
    # Generate base performance (random walk)
    performance_matrix = np.random.beta(2, 2, (n_time_periods, n_algorithms))
    
    # Add temporal correlation
    for k in range(n_algorithms):
        for t in range(1, n_time_periods):
            performance_matrix[t, k] = (0.7 * performance_matrix[t-1, k] + 
                                      0.3 * np.random.beta(2, 2))
    
    # Generate base constraints
    constraint_matrix = np.random.uniform(1, 10, (n_time_periods, n_constraints))
    
    # Inject bias if requested
    if bias_intensity > 0:
        # Make constraints correlate with performance
        avg_performance = np.mean(performance_matrix, axis=1)
        
        for j in range(n_constraints):
            noise = np.random.normal(0, 1, n_time_periods)
            constraint_matrix[:, j] = (
                (1 - bias_intensity) * constraint_matrix[:, j] +
                bias_intensity * (avg_performance * 10 + noise)
            )
    
    return performance_matrix, constraint_matrix

def save_results_json(results: dict, output_file: str) -> None:
    """
    Save bias detection results to JSON file.
    
    Parameters:
    -----------
    results : dict
        Results from BiasDetector.detect_bias()
    output_file : str
        Path to output JSON file
    """
    
    # Convert numpy types to Python types for JSON serialization
    json_results = {}
    for key, value in results.items():
        if isinstance(value, np.ndarray):
            json_results[key] = value.tolist()
        elif isinstance(value, (np.int64, np.int32)):
            json_results[key] = int(value)
        elif isinstance(value, (np.float64, np.float32)):
            json_results[key] = float(value)
        else:
            json_results[key] = value
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(json_results, f, indent=2, ensure_ascii=False)
    except Exception as e:
        raise ValueError(f"Error saving results to {output_file}: {e}")

def load_results_json(input_file: str) -> dict:
    """
    Load bias detection results from JSON file.
    
    Parameters:
    -----------
    input_file : str
        Path to input JSON file
        
    Returns:
    --------
    dict
        Loaded results
    """
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            results = json.load(f)
        return results
    except Exception as e:
        raise ValueError(f"Error loading results from {input_file}: {e}")


def validate_and_clean_data(df: pd.DataFrame, 
                            performance_cols: list,
                            constraint_cols: list,
                            time_col: str = 'time_period',
                            algorithm_col: str = 'algorithm',
                            auto_fix: bool = True) -> Tuple[pd.DataFrame, dict]:
    """
    Validate and automatically clean evaluation data.
    
    Detects and optionally fixes:
    - Missing values (NaN)
    - Duplicate entries
    - Outliers (IQR method)
    - Non-monotonic time periods
    - Negative performance values
    
    Parameters:
    -----------
    df : pd.DataFrame
        Raw evaluation data
    performance_cols : list
        Column names for performance metrics
    constraint_cols : list
        Column names for constraints
    time_col : str
        Column name for time periods
    algorithm_col : str
        Column name for algorithm identifiers
    auto_fix : bool
        If True, automatically apply fixes. If False, only report issues.
        
    Returns:
    --------
    tuple
        (cleaned_df, validation_report)
    """
    
    report = {
        'issues_found': [],
        'fixes_applied': [],
        'warnings': [],
        'summary': {}
    }
    
    df_clean = df.copy()
    
    # 1. Check for missing values
    missing_values = df_clean[performance_cols + constraint_cols].isnull().sum()
    if missing_values.any():
        missing_info = missing_values[missing_values > 0].to_dict()
        report['issues_found'].append({
            'type': 'missing_values',
            'details': missing_info,
            'severity': 'high'
        })
        
        if auto_fix:
            # Forward fill for time series
            for col in performance_cols + constraint_cols:
                if df_clean[col].isnull().any():
                    df_clean[col] = df_clean.groupby(algorithm_col)[col].ffill()
                    # If still NaN, use column mean
                    if df_clean[col].isnull().any():
                        df_clean[col].fillna(df_clean[col].mean(), inplace=True)
            
            report['fixes_applied'].append({
                'type': 'missing_values',
                'method': 'forward_fill_then_mean',
                'columns': list(missing_info.keys())
            })
    
    # 2. Check for duplicates
    duplicates = df_clean.duplicated(subset=[time_col, algorithm_col])
    if duplicates.any():
        n_duplicates = duplicates.sum()
        report['issues_found'].append({
            'type': 'duplicates',
            'count': int(n_duplicates),
            'severity': 'high'
        })
        
        if auto_fix:
            df_clean = df_clean.drop_duplicates(subset=[time_col, algorithm_col], keep='first')
            report['fixes_applied'].append({
                'type': 'duplicates',
                'method': 'keep_first',
                'removed': int(n_duplicates)
            })
    
    # 3. Check for outliers in performance (IQR method)
    outlier_cols = []
    for col in performance_cols:
        Q1 = df_clean[col].quantile(0.25)
        Q3 = df_clean[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 3 * IQR
        upper_bound = Q3 + 3 * IQR
        
        outliers = (df_clean[col] < lower_bound) | (df_clean[col] > upper_bound)
        if outliers.any():
            outlier_cols.append({
                'column': col,
                'count': int(outliers.sum()),
                'bounds': (float(lower_bound), float(upper_bound))
            })
            
            if auto_fix:
                # Clip to bounds
                df_clean[col] = df_clean[col].clip(lower=lower_bound, upper=upper_bound)
    
    if outlier_cols:
        report['issues_found'].append({
            'type': 'outliers',
            'details': outlier_cols,
            'severity': 'medium'
        })
        
        if auto_fix:
            report['fixes_applied'].append({
                'type': 'outliers',
                'method': 'IQR_clipping',
                'columns': [x['column'] for x in outlier_cols]
            })
    
    # 4. Check for negative performance values
    negative_perf = []
    for col in performance_cols:
        neg_count = (df_clean[col] < 0).sum()
        if neg_count > 0:
            negative_perf.append({'column': col, 'count': int(neg_count)})
            
            if auto_fix:
                df_clean[col] = df_clean[col].abs()
    
    if negative_perf:
        report['issues_found'].append({
            'type': 'negative_values',
            'details': negative_perf,
            'severity': 'high'
        })
        
        if auto_fix:
            report['fixes_applied'].append({
                'type': 'negative_values',
                'method': 'absolute_value'
            })
    
    # 5. Check time period consistency
    time_periods = sorted(df_clean[time_col].unique())
    expected_periods = list(range(1, len(time_periods) + 1))
    
    if time_periods != expected_periods:
        report['issues_found'].append({
            'type': 'non_sequential_time',
            'found': time_periods,
            'expected': expected_periods,
            'severity': 'medium'
        })
        
        if auto_fix:
            # Remap to sequential
            time_mapping = {old: new for old, new in zip(time_periods, expected_periods)}
            df_clean[time_col] = df_clean[time_col].map(time_mapping)
            
            report['fixes_applied'].append({
                'type': 'non_sequential_time',
                'method': 'remap_sequential',
                'mapping': time_mapping
            })
    
    # 6. Check for constant constraints (low variance)
    constant_constraints = []
    for col in constraint_cols:
        if df_clean[col].std() < 1e-6:
            constant_constraints.append(col)
    
    if constant_constraints:
        report['warnings'].append({
            'type': 'constant_constraints',
            'columns': constant_constraints,
            'message': 'These constraints have near-zero variance. CCS may be unreliable.'
        })
    
    # 7. Summary statistics
    report['summary'] = {
        'total_issues_found': len(report['issues_found']),
        'total_fixes_applied': len(report['fixes_applied']),
        'total_warnings': len(report['warnings']),
        'data_quality_score': _compute_quality_score(report),
        'rows_original': len(df),
        'rows_cleaned': len(df_clean),
        'time_periods': len(df_clean[time_col].unique()),
        'algorithms': len(df_clean[algorithm_col].unique())
    }
    
    return df_clean, report


def _compute_quality_score(report: dict) -> float:
    """
    Compute data quality score (0-100) based on validation report.
    
    Scoring:
    - Start with 100
    - Deduct 20 per high severity issue
    - Deduct 10 per medium severity issue
    - Deduct 5 per warning
    """
    score = 100.0
    
    for issue in report['issues_found']:
        if issue['severity'] == 'high':
            score -= 20
        elif issue['severity'] == 'medium':
            score -= 10
    
    score -= len(report['warnings']) * 5
    
    return max(0.0, score)


def print_validation_report(report: dict) -> None:
    """
    Print a formatted validation report to console.
    
    Parameters:
    -----------
    report : dict
        Validation report from validate_and_clean_data()
    """
    
    print("=" * 60)
    print("DATA VALIDATION REPORT")
    print("=" * 60)
    
    # Summary
    summary = report['summary']
    quality_score = summary['data_quality_score']
    
    if quality_score >= 90:
        quality_status = "✅ EXCELLENT"
    elif quality_score >= 70:
        quality_status = "⚠️  GOOD"
    elif quality_score >= 50:
        quality_status = "⚠️  FAIR"
    else:
        quality_status = "❌ POOR"
    
    print(f"\nData Quality Score: {quality_score:.1f}/100 {quality_status}")
    print(f"Rows: {summary['rows_original']} → {summary['rows_cleaned']}")
    print(f"Time periods: {summary['time_periods']}")
    print(f"Algorithms: {summary['algorithms']}")
    
    # Issues
    if report['issues_found']:
        print(f"\n⚠️  ISSUES FOUND: {len(report['issues_found'])}")
        print("-" * 30)
        for issue in report['issues_found']:
            severity_icon = "🔴" if issue['severity'] == 'high' else "🟡"
            print(f"{severity_icon} {issue['type'].upper()}")
            if 'details' in issue:
                print(f"   Details: {issue['details']}")
    else:
        print("\n✅ NO ISSUES FOUND")
    
    # Fixes
    if report['fixes_applied']:
        print(f"\n✨ FIXES APPLIED: {len(report['fixes_applied'])}")
        print("-" * 30)
        for fix in report['fixes_applied']:
            print(f"✓ {fix['type']}: {fix['method']}")
    
    # Warnings
    if report['warnings']:
        print(f"\n⚠️  WARNINGS: {len(report['warnings'])}")
        print("-" * 30)
        for warning in report['warnings']:
            print(f"⚠️  {warning['type']}: {warning['message']}")
    
    print("\n" + "=" * 60)
