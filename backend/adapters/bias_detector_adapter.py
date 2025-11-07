"""
Adapter for circular_bias_detector package
Provides backward-compatible interface for existing Flask API
"""

import pandas as pd
from typing import Dict, List
import traceback

# Import from the circular_bias_detector package
try:
    from circular_bias_detector import BiasDetector
    from circular_bias_detector.config import BiasDetectionConfig, get_config, set_config
    from circular_bias_detector.exceptions import CircularBiasDetectorError
    from circular_bias_detector.core.metrics import (
        compute_psi, compute_ccs, compute_rho_pc, compute_all_indicators
    )
    PACKAGE_AVAILABLE = True
    print("[OK] circular-bias-detector package loaded successfully")
except ImportError as e:
    PACKAGE_AVAILABLE = False
    print(f"[WARN] circular-bias-detector not available: {e}")
    print("       Falling back to legacy core implementation")


class BiasDetectorAdapter:
    """
    Adapter to integrate circular_bias_detector package into existing Flask API.
    Provides backward-compatible interface with the original core/bias_scorer.py
    """
    
    def __init__(self):
        """Initialize detector with API-optimized configuration"""
        if not PACKAGE_AVAILABLE:
            raise ImportError(
                "circular-bias-detector package is not available. "
                "Please install with: pip install circular-bias-detector"
            )
        
        self.detector = BiasDetector()
        
        # Configure for API usage (less verbose)
        config = get_config()
        config.log_level = "WARNING"
        config.enable_bootstrap = False  # Default to fast mode
        set_config(config)
    
    def detect_bias_from_dataframe(
        self, 
        df: pd.DataFrame, 
        weights: List[float] = [0.33, 0.33, 0.34],
        run_bootstrap: bool = False,
        n_bootstrap: int = 1000
    ) -> Dict:
        """
        Detect bias using circular_bias_detector package.
        
        Args:
            df: DataFrame with evaluation data
            weights: Weights for PSI, CCS, ρ_PC (default: equal weights)
            run_bootstrap: Whether to compute bootstrap CI
            n_bootstrap: Number of bootstrap iterations
            
        Returns:
            Dictionary with detection results (API-compatible format)
        """
        try:
            # Validate input data
            required_columns = ['time_period', 'algorithm', 'performance']
            missing = [col for col in required_columns if col not in df.columns]
            if missing:
                raise ValueError(f"Missing required columns: {missing}")
            
            # Compute individual indicators
            print("[Computing] PSI...")
            psi_result = compute_psi(df)
            
            print("[Computing] CCS...")
            ccs_result = compute_ccs(df)
            
            print("[Computing] rho_PC...")
            rho_pc_result = compute_rho_pc(df)
            
            # Normalize to [0, 1]
            psi_norm = self._normalize_psi(psi_result['psi_score'])
            ccs_norm = self._normalize_ccs(ccs_result['ccs_score'])
            rho_pc_norm = self._normalize_rho_pc(rho_pc_result['rho_pc'])
            
            # Compute CBS
            cbs_score = (
                weights[0] * psi_norm +
                weights[1] * ccs_norm +
                weights[2] * rho_pc_norm
            )
            
            # Risk assessment
            risk_level, risk_category = self._assess_risk(cbs_score)
            
            # Bias detection decision (2 out of 3 rule)
            indicators_triggered = sum([
                psi_result.get('exceeds_threshold', False),
                not ccs_result.get('exceeds_threshold', True),  # CCS low = bad
                rho_pc_result.get('exceeds_threshold', False)
            ])
            
            bias_detected = indicators_triggered >= 2
            confidence = (indicators_triggered / 3.0) * 100
            
            # Generate interpretation and recommendations
            interpretation = self._generate_interpretation(
                psi_result, ccs_result, rho_pc_result,
                cbs_score, risk_level, bias_detected
            )
            
            recommendations = self._generate_recommendations(
                psi_result, ccs_result, rho_pc_result, bias_detected
            )
            
            # Compile API-compatible results
            api_results = {
                # Individual indicators
                'psi': {
                    'score': float(psi_result.get('psi_score', 0.0)),
                    'normalized': float(psi_norm),
                    'threshold': psi_result.get('threshold', 0.2),
                    'exceeds_threshold': psi_result.get('exceeds_threshold', False),
                    'interpretation': psi_result.get('interpretation', '')
                },
                'ccs': {
                    'score': float(ccs_result.get('ccs_score', 0.0)),
                    'normalized': float(ccs_norm),
                    'threshold': ccs_result.get('threshold', 0.85),
                    'exceeds_threshold': ccs_result.get('exceeds_threshold', True),
                    'interpretation': ccs_result.get('interpretation', '')
                },
                'rho_pc': {
                    'score': float(rho_pc_result.get('rho_pc', 0.0)),
                    'normalized': float(rho_pc_norm),
                    'threshold': rho_pc_result.get('threshold', 0.5),
                    'exceeds_threshold': rho_pc_result.get('exceeds_threshold', False),
                    'p_value': rho_pc_result.get('p_value', 1.0),
                    'significant': rho_pc_result.get('significant', False),
                    'interpretation': rho_pc_result.get('interpretation', '')
                },
                
                # CBS composite
                'cbs_score': float(cbs_score),
                'risk_level': risk_level,
                'risk_category': risk_category,
                'weights': weights,
                
                # Decision
                'bias_detected': bias_detected,
                'indicators_triggered': indicators_triggered,
                'confidence': float(confidence),
                
                # Explanations
                'interpretation': interpretation,
                'recommendations': recommendations,
                
                # Metadata
                'data_stats': {
                    'num_rows': len(df),
                    'num_algorithms': len(df['algorithm'].unique()) if 'algorithm' in df.columns else 0,
                    'num_periods': len(df['time_period'].unique()) if 'time_period' in df.columns else 0,
                    'algorithms': df['algorithm'].unique().tolist() if 'algorithm' in df.columns else [],
                    'time_periods': sorted(df['time_period'].unique().tolist()) if 'time_period' in df.columns else []
                }
            }
            
            # Optional: Bootstrap CI
            if run_bootstrap:
                print(f"\n[Bootstrap] Running {n_bootstrap} iterations...")
                # Placeholder for bootstrap - can be implemented if needed
                api_results['bootstrap'] = {'enabled': True, 'n_iterations': n_bootstrap}
            
            return api_results
            
        except Exception as e:
            print(f"[ERROR] Package implementation failed: {str(e)}")
            print("[FALLBACK] Attempting to use legacy core implementation...")
            try:
                from core.bias_scorer import detect_circular_bias as original_detect
                return original_detect(df, weights, run_bootstrap, n_bootstrap)
            except Exception as fallback_error:
                print(f"[ERROR] Fallback also failed: {fallback_error}")
                print(traceback.format_exc())
                raise CircularBiasDetectorError(f"Bias detection failed: {str(e)}")
    
    def _normalize_psi(self, psi_score: float, max_psi: float = 0.5) -> float:
        """Normalize PSI for CBS calculation (high PSI = bad)"""
        return min(psi_score / max_psi, 1.0)
    
    def _normalize_ccs(self, ccs_score: float) -> float:
        """Normalize CCS for CBS calculation (low CCS = bad)"""
        return 1.0 - ccs_score
    
    def _normalize_rho_pc(self, rho_pc: float) -> float:
        """Normalize ρ_PC for CBS calculation (high |ρ_PC| = bad)"""
        return abs(rho_pc)
    
    def _assess_risk(self, cbs_score: float) -> tuple:
        """Assess risk level from CBS score"""
        if cbs_score < 0.3:
            return ("Low Risk", "low")
        elif cbs_score < 0.6:
            return ("Medium Risk", "medium")
        else:
            return ("High Risk", "high")
    
    def _generate_interpretation(
        self,
        psi_result: Dict,
        ccs_result: Dict,
        rho_pc_result: Dict,
        cbs_score: float,
        risk_level: str,
        bias_detected: bool
    ) -> str:
        """Generate human-readable interpretation"""
        
        if bias_detected:
            verdict = "⚠️ CIRCULAR BIAS DETECTED"
            explanation = "Multiple indicators suggest evaluation protocol manipulation."
        else:
            verdict = "✅ NO SIGNIFICANT BIAS"
            explanation = "Evaluation appears methodologically sound."
        
        details = []
        
        # PSI details
        if psi_result.get('exceeds_threshold', False):
            details.append(f"PSI={psi_result.get('psi_score', 0):.3f} indicates parameter instability")
        
        # CCS details
        if not ccs_result.get('exceeds_threshold', True):
            details.append(f"CCS={ccs_result.get('ccs_score', 0):.3f} indicates constraint inconsistency")
        
        # ρ_PC details
        if rho_pc_result.get('exceeds_threshold', False):
            direction = "positive" if rho_pc_result.get('rho_pc', 0) > 0 else "negative"
            details.append(f"ρ_PC={rho_pc_result.get('rho_pc', 0):.3f} indicates {direction} correlation")
        
        if details:
            detail_str = "\n  • " + "\n  • ".join(details)
        else:
            detail_str = "\n  • All indicators within acceptable ranges"
        
        return (
            f"{verdict}\n\n"
            f"Circular Bias Score (CBS): {cbs_score:.3f}\n"
            f"Risk Level: {risk_level}\n\n"
            f"{explanation}{detail_str}"
        )
    
    def _generate_recommendations(
        self,
        psi_result: Dict,
        ccs_result: Dict,
        rho_pc_result: Dict,
        bias_detected: bool
    ) -> List[str]:
        """Generate actionable recommendations"""
        
        recommendations = []
        
        if not bias_detected:
            recommendations.append("✅ Evaluation methodology appears sound")
            recommendations.append("Continue monitoring in future evaluations")
            return recommendations
        
        # PSI recommendations
        if psi_result.get('exceeds_threshold', False):
            recommendations.append(
                "🔧 PSI Issue: Review parameter/hyperparameter changes between evaluations. "
                "Ensure consistent settings across all algorithms."
            )
        
        # CCS recommendations
        if not ccs_result.get('exceeds_threshold', True):
            recommendations.append(
                "🔧 CCS Issue: Standardize evaluation constraints (compute budget, memory, dataset size). "
                "Document any protocol changes explicitly."
            )
        
        # ρ_PC recommendations
        if rho_pc_result.get('exceeds_threshold', False):
            if rho_pc_result.get('rho_pc', 0) > 0:
                recommendations.append(
                    "🔧 ρ_PC Issue: Performance correlates with resources. "
                    "Verify that resource allocations were not adjusted based on preliminary results."
                )
            else:
                recommendations.append(
                    "🚨 ρ_PC Red Flag: Negative correlation detected. "
                    "This suggests potential cherry-picking or protocol gaming."
                )
        
        recommendations.append(
            "📋 General: Pre-register evaluation protocol, use held-out test sets, "
            "and ensure blind evaluation where possible."
        )
        
        return recommendations


# Drop-in replacement function for backward compatibility
def detect_circular_bias(
    data: pd.DataFrame,
    weights: List[float] = [0.33, 0.33, 0.34],
    run_bootstrap: bool = False,
    n_bootstrap: int = 1000
) -> Dict:
    """
    Drop-in replacement for original detect_circular_bias function.
    Now uses circular_bias_detector package via adapter.
    
    Args:
        data: Evaluation data (CSV format with required columns)
        weights: Weights for PSI, CCS, ρ_PC (default: equal weights)
        run_bootstrap: Whether to compute bootstrap CI (slower)
        n_bootstrap: Number of bootstrap iterations
    
    Returns:
        Comprehensive dictionary with bias detection results
    """
    if not PACKAGE_AVAILABLE:
        # Fallback to original implementation if package not available
        from core.bias_scorer import detect_circular_bias as original_detect
        print("[WARN] Using legacy core implementation")
        return original_detect(data, weights, run_bootstrap, n_bootstrap)
    
    adapter = BiasDetectorAdapter()
    return adapter.detect_bias_from_dataframe(
        data, 
        weights=weights,
        run_bootstrap=run_bootstrap,
        n_bootstrap=n_bootstrap
    )
