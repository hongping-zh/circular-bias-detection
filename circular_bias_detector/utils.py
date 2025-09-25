"""
Utility functions for the circular bias detection framework.
"""

import numpy as np
import pandas as pd
from typing import Union, Optional, Tuple
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
