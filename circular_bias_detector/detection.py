"""
Main BiasDetector class for comprehensive bias detection workflow.
"""

import numpy as np
import pandas as pd
from typing import Union, Dict, List, Optional, Tuple
import warnings

from .core import compute_all_indicators
from .utils import validate_matrices, load_data


class BiasDetector:
    """
    Main class for detecting circular reasoning bias in AI algorithm evaluation.
    
    This class provides a high-level interface for bias detection using the
    PSI, CCS, and ρ_PC indicators.
    """
    
    def __init__(self, 
                 psi_threshold: float = 0.1,
                 ccs_threshold: float = 0.8,
                 rho_pc_threshold: float = 0.3):
        """
        Initialize BiasDetector with detection thresholds.
        
        Parameters:
        -----------
        psi_threshold : float
            PSI threshold for bias detection (default: 0.1)
        ccs_threshold : float
            CCS threshold for bias detection (default: 0.8)
        rho_pc_threshold : float
            |ρ_PC| threshold for bias detection (default: 0.3)
        """
        self.psi_threshold = psi_threshold
        self.ccs_threshold = ccs_threshold
        self.rho_pc_threshold = rho_pc_threshold
        
        # Storage for results
        self.last_results = None
        
    def detect_bias(self,
                   performance_matrix: Union[np.ndarray, pd.DataFrame],
                   constraint_matrix: Union[np.ndarray, pd.DataFrame],
                   algorithm_params: Optional[Union[np.ndarray, pd.DataFrame]] = None,
                   algorithm_names: Optional[List[str]] = None,
                   enable_bootstrap: bool = False,
                   n_bootstrap: int = 1000,
                   enable_adaptive_thresholds: bool = False) -> Dict:
        """
        Detect circular reasoning bias in evaluation data.
        
        Parameters:
        -----------
        performance_matrix : array-like
            Shape (T, K) where T is time periods, K is algorithms
        constraint_matrix : array-like
            Shape (T, p) where T is time periods, p is constraint types
        algorithm_params : array-like, optional
            Shape (T, K, p) algorithm parameters across time
        algorithm_names : list, optional
            Names of algorithms for reporting
        enable_bootstrap : bool, optional
            If True, compute bootstrap confidence intervals and p-values (default: False)
        n_bootstrap : int, optional
            Number of bootstrap samples (default: 1000)
        enable_adaptive_thresholds : bool, optional
            If True, use data-adaptive thresholds instead of fixed values (default: False)
            
        Returns:
        --------
        dict
            Comprehensive bias detection results with optional bootstrap statistics
        """
        
        # Convert to numpy arrays
        if isinstance(performance_matrix, pd.DataFrame):
            perf_array = performance_matrix.values
            if algorithm_names is None:
                algorithm_names = list(performance_matrix.columns)
        else:
            perf_array = np.array(performance_matrix)
            
        if isinstance(constraint_matrix, pd.DataFrame):
            const_array = constraint_matrix.values
        else:
            const_array = np.array(constraint_matrix)
            
        if algorithm_params is not None:
            if isinstance(algorithm_params, pd.DataFrame):
                params_array = algorithm_params.values
            else:
                params_array = np.array(algorithm_params)
        else:
            params_array = None
            
        # Validate input matrices
        try:
            validate_matrices(perf_array, const_array, params_array)
        except ValueError as e:
            raise ValueError(f"Input validation failed: {e}")
            
        # Compute adaptive thresholds if requested
        if enable_adaptive_thresholds:
            from .core import compute_adaptive_thresholds
            adaptive_thresholds = compute_adaptive_thresholds(
                perf_array, 
                const_array,
                quantile=0.95,
                n_simulations=500
            )
            # Use adaptive thresholds
            psi_threshold = adaptive_thresholds['psi_threshold']
            ccs_threshold = adaptive_thresholds['ccs_threshold']
            rho_pc_threshold = adaptive_thresholds['rho_pc_threshold']
        else:
            # Use fixed thresholds
            psi_threshold = self.psi_threshold
            ccs_threshold = self.ccs_threshold
            rho_pc_threshold = self.rho_pc_threshold
        
        # Compute bootstrap statistics if requested
        if enable_bootstrap:
            from .core import bootstrap_psi, bootstrap_ccs, bootstrap_rho_pc
            
            psi_boot = bootstrap_psi(perf_array, params_array, n_bootstrap=n_bootstrap)
            ccs_boot = bootstrap_ccs(const_array, n_bootstrap=n_bootstrap)
            rho_boot = bootstrap_rho_pc(perf_array, const_array, n_bootstrap=n_bootstrap)
            
            results = {
                'psi_score': psi_boot['psi'],
                'ccs_score': ccs_boot['ccs'],
                'rho_pc_score': rho_boot['rho_pc'],
                'psi_ci_lower': psi_boot['ci_lower'],
                'psi_ci_upper': psi_boot['ci_upper'],
                'psi_pvalue': psi_boot['p_value'],
                'ccs_ci_lower': ccs_boot['ci_lower'],
                'ccs_ci_upper': ccs_boot['ci_upper'],
                'ccs_pvalue': ccs_boot['p_value'],
                'rho_pc_ci_lower': rho_boot['ci_lower'],
                'rho_pc_ci_upper': rho_boot['ci_upper'],
                'rho_pc_pvalue': rho_boot['p_value'],
                'bootstrap_enabled': True,
                'n_bootstrap': n_bootstrap
            }
        else:
            # Standard computation
            results = compute_all_indicators(
                perf_array, 
                const_array, 
                params_array
            )
            results['bootstrap_enabled'] = False
        
        # Apply thresholds
        from .core import detect_bias_threshold
        bias_results = detect_bias_threshold(
            results['psi_score'],
            results['ccs_score'], 
            results['rho_pc_score'],
            psi_threshold,
            ccs_threshold,
            rho_pc_threshold
        )
        
        # Update results with custom thresholds
        results.update(bias_results)
        
        # Add metadata
        T, K = perf_array.shape
        results['metadata'] = {
            'time_periods': T,
            'num_algorithms': K,
            'num_constraints': const_array.shape[1],
            'algorithm_names': algorithm_names or [f'Algorithm_{i+1}' for i in range(K)],
            'thresholds': {
                'psi': psi_threshold,
                'ccs': ccs_threshold,
                'rho_pc': rho_pc_threshold
            },
            'adaptive_thresholds_enabled': enable_adaptive_thresholds
        }
        
        # Add adaptive threshold info if used
        if enable_adaptive_thresholds:
            results['metadata']['adaptive_method'] = 'quantile_95'
        
        # Store results
        self.last_results = results
        
        return results
    
    def detect_from_file(self, 
                        data_file: str,
                        performance_cols: List[str],
                        constraint_cols: List[str],
                        time_col: str = 'time_period') -> Dict:
        """
        Detect bias directly from CSV/Excel file.
        
        Parameters:
        -----------
        data_file : str
            Path to data file (CSV or Excel)
        performance_cols : list
            Column names for algorithm performance
        constraint_cols : list
            Column names for constraints
        time_col : str
            Column name for time periods
            
        Returns:
        --------
        dict
            Bias detection results
        """
        
        # Load data
        data = load_data(data_file)
        
        # Sort by time
        data = data.sort_values(time_col)
        
        # Extract matrices
        performance_matrix = data[performance_cols].values
        constraint_matrix = data[constraint_cols].values
        
        return self.detect_bias(
            performance_matrix,
            constraint_matrix,
            algorithm_names=performance_cols
        )
    
    def generate_report(self, results: Optional[Dict] = None) -> str:
        """
        Generate a human-readable bias detection report.
        
        Parameters:
        -----------
        results : dict, optional
            Results from detect_bias(). Uses last results if None.
            
        Returns:
        --------
        str
            Formatted report string
        """
        
        if results is None:
            if self.last_results is None:
                raise ValueError("No results available. Run detect_bias() first.")
            results = self.last_results
            
        report = []
        report.append("=" * 60)
        report.append("CIRCULAR REASONING BIAS DETECTION REPORT")
        report.append("=" * 60)
        
        # Overall result
        if results['overall_bias']:
            report.append("🚨 BIAS DETECTED")
            report.append(f"   Confidence: {results['confidence']:.1%}")
        else:
            report.append("✅ NO BIAS DETECTED")
            report.append(f"   Confidence: {1-results['confidence']:.1%}")
            
        report.append("")
        
        # Individual indicators
        report.append("INDICATOR SCORES:")
        report.append("-" * 30)
        
        bootstrap_enabled = results.get('bootstrap_enabled', False)
        
        psi = results['psi_score']
        if bootstrap_enabled:
            psi_ci_lower = results['psi_ci_lower']
            psi_ci_upper = results['psi_ci_upper']
            psi_pvalue = results['psi_pvalue']
            report.append(f"PSI (Parameter Stability):     {psi:.4f} [{psi_ci_lower:.4f}-{psi_ci_upper:.4f}]")
            report.append(f"  p-value: {psi_pvalue:.3f} {'***' if psi_pvalue < 0.001 else '**' if psi_pvalue < 0.01 else '*' if psi_pvalue < 0.05 else 'ns'}")
        else:
            report.append(f"PSI (Parameter Stability):     {psi:.4f}")
        report.append(f"  Threshold: {results['metadata']['thresholds']['psi']:.4f}")
        report.append(f"  Status: {'⚠️  UNSTABLE' if results['psi_bias'] else '✅ STABLE'}")
        report.append("")
        
        ccs = results['ccs_score']
        if bootstrap_enabled:
            ccs_ci_lower = results['ccs_ci_lower']
            ccs_ci_upper = results['ccs_ci_upper']
            ccs_pvalue = results['ccs_pvalue']
            report.append(f"CCS (Constraint Consistency):  {ccs:.4f} [{ccs_ci_lower:.4f}-{ccs_ci_upper:.4f}]")
            report.append(f"  p-value: {ccs_pvalue:.3f} {'***' if ccs_pvalue < 0.001 else '**' if ccs_pvalue < 0.01 else '*' if ccs_pvalue < 0.05 else 'ns'}")
        else:
            report.append(f"CCS (Constraint Consistency):  {ccs:.4f}")
        report.append(f"  Threshold: {results['metadata']['thresholds']['ccs']:.4f}")
        report.append(f"  Status: {'⚠️  INCONSISTENT' if results['ccs_bias'] else '✅ CONSISTENT'}")
        report.append("")
        
        rho_pc = results['rho_pc_score']
        if bootstrap_enabled:
            rho_ci_lower = results['rho_pc_ci_lower']
            rho_ci_upper = results['rho_pc_ci_upper']
            rho_pvalue = results['rho_pc_pvalue']
            report.append(f"ρ_PC (Performance-Constraint): {rho_pc:+.4f} [{rho_ci_lower:+.4f}-{rho_ci_upper:+.4f}]")
            report.append(f"  p-value: {rho_pvalue:.3f} {'***' if rho_pvalue < 0.001 else '**' if rho_pvalue < 0.01 else '*' if rho_pvalue < 0.05 else 'ns'}")
        else:
            report.append(f"ρ_PC (Performance-Constraint): {rho_pc:+.4f}")
        report.append(f"  Threshold: ±{results['metadata']['thresholds']['rho_pc']:.4f}")
        report.append(f"  Status: {'⚠️  CORRELATED' if results['rho_pc_bias'] else '✅ INDEPENDENT'}")
        report.append("")
        
        if bootstrap_enabled:
            report.append(f"✨ Bootstrap resampling (n={results['n_bootstrap']})")
            report.append("   Significance: *** p<0.001, ** p<0.01, * p<0.05, ns p≥0.05")
            report.append("")
        
        # Metadata
        meta = results['metadata']
        report.append("EVALUATION METADATA:")
        report.append("-" * 30)
        report.append(f"Time periods: {meta['time_periods']}")
        report.append(f"Algorithms: {meta['num_algorithms']}")
        report.append(f"Constraints: {meta['num_constraints']}")
        report.append("")
        
        if len(meta['algorithm_names']) <= 10:
            report.append(f"Algorithm names: {', '.join(meta['algorithm_names'])}")
        else:
            report.append(f"Algorithm names: {', '.join(meta['algorithm_names'][:3])}, ... (+{len(meta['algorithm_names'])-3} more)")
            
        report.append("")
        report.append("=" * 60)
        
        return "\n".join(report)
    
    def plot_indicators(self, results: Optional[Dict] = None, save_path: Optional[str] = None):
        """
        Create visualization of bias indicators.
        
        Parameters:
        -----------
        results : dict, optional
            Results from detect_bias()
        save_path : str, optional
            Path to save plot (if None, displays plot)
        """
        
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            warnings.warn("matplotlib not available for plotting")
            return
            
        if results is None:
            results = self.last_results
            
        if results is None:
            raise ValueError("No results available for plotting")
            
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        
        # PSI
        axes[0].bar(['PSI'], [results['psi_score']], 
                   color='red' if results['psi_bias'] else 'green', alpha=0.7)
        axes[0].axhline(y=self.psi_threshold, color='red', linestyle='--', alpha=0.8)
        axes[0].set_title('Parameter Stability Index')
        axes[0].set_ylabel('PSI Score')
        
        # CCS
        axes[1].bar(['CCS'], [results['ccs_score']], 
                   color='red' if results['ccs_bias'] else 'green', alpha=0.7)
        axes[1].axhline(y=self.ccs_threshold, color='red', linestyle='--', alpha=0.8)
        axes[1].set_title('Constraint Consistency Score')
        axes[1].set_ylabel('CCS Score')
        
        # ρ_PC
        rho_pc = results['rho_pc_score']
        axes[2].bar(['ρ_PC'], [rho_pc], 
                   color='red' if results['rho_pc_bias'] else 'green', alpha=0.7)
        axes[2].axhline(y=self.rho_pc_threshold, color='red', linestyle='--', alpha=0.8)
        axes[2].axhline(y=-self.rho_pc_threshold, color='red', linestyle='--', alpha=0.8)
        axes[2].set_title('Performance-Constraint Correlation')
        axes[2].set_ylabel('ρ_PC Score')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()
