"""
CBS (Circular Bias Score) - Composite Bias Indicator

Combines PSI, CCS, and ρ_PC into a single comprehensive bias score.

Formula:
    CBS = w₁ · ψ(PSI) + w₂ · ψ(CCS) + w₃ · ψ(ρ_PC)

where:
    ψ(·) = normalization function to [0, 1]
    w₁, w₂, w₃ = weights (default: 0.33, 0.33, 0.34)

CBS Interpretation:
    CBS < 0.3: Low risk
    0.3 ≤ CBS < 0.6: Medium risk
    CBS ≥ 0.6: High risk
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
from .psi_calculator import compute_psi, normalize_psi
from .ccs_calculator import compute_ccs, normalize_ccs
from .rho_pc_calculator import compute_rho_pc, normalize_rho_pc
from .bootstrap import bootstrap_indicators


def detect_circular_bias(
    data: pd.DataFrame,
    weights: List[float] = [0.33, 0.33, 0.34],
    run_bootstrap: bool = False,
    n_bootstrap: int = 1000
) -> Dict:
    """
    Main function to detect circular reasoning bias in evaluation data.
    
    This is the primary API endpoint for bias detection.
    
    Args:
        data: Evaluation data (CSV format with required columns)
        weights: Weights for PSI, CCS, ρ_PC (default: equal weights)
        run_bootstrap: Whether to compute bootstrap CI (slower)
        n_bootstrap: Number of bootstrap iterations
    
    Returns:
        Comprehensive dictionary with:
        - Individual indicators (PSI, CCS, ρ_PC)
        - CBS composite score
        - Risk level and interpretation
        - Recommendations
        - (Optional) Bootstrap confidence intervals
    
    Example:
        >>> df = pd.read_csv('evaluation_data.csv')
        >>> results = detect_circular_bias(df)
        >>> print(results['cbs_score'])
        >>> print(results['risk_level'])
        >>> print(results['bias_detected'])
    """
    
    # Validate weights
    if len(weights) != 3:
        raise ValueError("weights must have exactly 3 elements")
    if not np.isclose(sum(weights), 1.0):
        raise ValueError(f"weights must sum to 1.0, got {sum(weights)}")
    
    # Compute individual indicators
    print("🔬 Computing PSI...")
    psi_result = compute_psi(data)
    
    print("🔬 Computing CCS...")
    ccs_result = compute_ccs(data)
    
    print("🔬 Computing ρ_PC...")
    rho_pc_result = compute_rho_pc(data)
    
    # Normalize to [0, 1]
    psi_norm = _normalize_psi_for_cbs(psi_result['psi_score'])
    ccs_norm = _normalize_ccs_for_cbs(ccs_result['ccs_score'])
    rho_pc_norm = _normalize_rho_pc_for_cbs(rho_pc_result['rho_pc'])
    
    # Compute CBS
    cbs_score = (
        weights[0] * psi_norm +
        weights[1] * ccs_norm +
        weights[2] * rho_pc_norm
    )
    
    # Risk assessment
    risk_level, risk_category = _assess_risk(cbs_score)
    
    # Bias detection decision
    indicators_triggered = sum([
        psi_result['exceeds_threshold'],
        not ccs_result['exceeds_threshold'],  # CCS low = bad
        rho_pc_result['exceeds_threshold']
    ])
    
    bias_detected = indicators_triggered >= 2  # 2 out of 3 rule
    confidence = (indicators_triggered / 3.0) * 100
    
    # Generate interpretation and recommendations
    interpretation = _generate_interpretation(
        psi_result, ccs_result, rho_pc_result,
        cbs_score, risk_level, bias_detected
    )
    
    recommendations = _generate_recommendations(
        psi_result, ccs_result, rho_pc_result, bias_detected
    )
    
    # Compile results
    results = {
        # Individual indicators
        'psi': {
            'score': psi_result['psi_score'],
            'normalized': float(psi_norm),
            'threshold': psi_result['threshold'],
            'exceeds_threshold': psi_result['exceeds_threshold'],
            'interpretation': psi_result['interpretation']
        },
        'ccs': {
            'score': ccs_result['ccs_score'],
            'normalized': float(ccs_norm),
            'threshold': ccs_result['threshold'],
            'exceeds_threshold': ccs_result['exceeds_threshold'],
            'interpretation': ccs_result['interpretation']
        },
        'rho_pc': {
            'score': rho_pc_result['rho_pc'],
            'normalized': float(rho_pc_norm),
            'threshold': rho_pc_result['threshold'],
            'exceeds_threshold': rho_pc_result['exceeds_threshold'],
            'p_value': rho_pc_result['p_value'],
            'significant': rho_pc_result['significant'],
            'interpretation': rho_pc_result['interpretation']
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
            'num_rows': len(data),
            'num_algorithms': len(data['algorithm'].unique()),
            'num_periods': len(data['time_period'].unique()),
            'algorithms': data['algorithm'].unique().tolist(),
            'time_periods': sorted(data['time_period'].unique())
        }
    }
    
    # Optional: Bootstrap CI
    if run_bootstrap:
        print(f"\n🔄 Running bootstrap ({n_bootstrap} iterations)...")
        bootstrap_results = bootstrap_indicators(data, n_iterations=n_bootstrap)
        results['bootstrap'] = bootstrap_results
    
    return results


def _normalize_psi_for_cbs(psi_score: float, max_psi: float = 0.5) -> float:
    """
    Normalize PSI for CBS calculation.
    
    High PSI = bad, so normalize to [0, 1] where 1 = worst
    """
    return min(psi_score / max_psi, 1.0)


def _normalize_ccs_for_cbs(ccs_score: float) -> float:
    """
    Normalize CCS for CBS calculation.
    
    Low CCS = bad, so invert: 1 - CCS
    """
    return 1.0 - ccs_score


def _normalize_rho_pc_for_cbs(rho_pc: float) -> float:
    """
    Normalize ρ_PC for CBS calculation.
    
    High |ρ_PC| = bad, so use absolute value
    """
    return abs(rho_pc)


def _assess_risk(cbs_score: float) -> Tuple[str, str]:
    """
    Assess risk level from CBS score.
    
    Returns:
        (risk_level_text, risk_category)
    """
    if cbs_score < 0.3:
        return ("Low Risk", "low")
    elif cbs_score < 0.6:
        return ("Medium Risk", "medium")
    else:
        return ("High Risk", "high")


def _generate_interpretation(
    psi_result: Dict,
    ccs_result: Dict,
    rho_pc_result: Dict,
    cbs_score: float,
    risk_level: str,
    bias_detected: bool
) -> str:
    """Generate human-readable interpretation of results."""
    
    if bias_detected:
        verdict = "⚠️ CIRCULAR BIAS DETECTED"
        explanation = "Multiple indicators suggest evaluation protocol manipulation."
    else:
        verdict = "✅ NO SIGNIFICANT BIAS"
        explanation = "Evaluation appears methodologically sound."
    
    details = []
    
    # PSI details
    if psi_result['exceeds_threshold']:
        details.append(f"PSI={psi_result['psi_score']:.3f} indicates parameter instability")
    
    # CCS details
    if not ccs_result['exceeds_threshold']:
        details.append(f"CCS={ccs_result['ccs_score']:.3f} indicates constraint inconsistency")
    
    # ρ_PC details
    if rho_pc_result['exceeds_threshold']:
        direction = "positive" if rho_pc_result['rho_pc'] > 0 else "negative"
        details.append(f"ρ_PC={rho_pc_result['rho_pc']:.3f} indicates {direction} correlation")
    
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
    psi_result: Dict,
    ccs_result: Dict,
    rho_pc_result: Dict,
    bias_detected: bool
) -> List[str]:
    """Generate actionable recommendations."""
    
    recommendations = []
    
    if not bias_detected:
        recommendations.append("✅ Evaluation methodology appears sound")
        recommendations.append("Continue monitoring in future evaluations")
        return recommendations
    
    # PSI recommendations
    if psi_result['exceeds_threshold']:
        recommendations.append(
            "🔧 PSI Issue: Review parameter/hyperparameter changes between evaluations. "
            "Ensure consistent settings across all algorithms."
        )
    
    # CCS recommendations
    if not ccs_result['exceeds_threshold']:
        recommendations.append(
            "🔧 CCS Issue: Standardize evaluation constraints (compute budget, memory, dataset size). "
            "Document any protocol changes explicitly."
        )
    
    # ρ_PC recommendations
    if rho_pc_result['exceeds_threshold']:
        if rho_pc_result['rho_pc'] > 0:
            recommendations.append(
                "🔧 ρ_PC Issue: Performance correlates with resources. "
                "Verify that resource allocations were not adjusted based on preliminary results. "
                "Consider fixed-budget evaluation."
            )
        else:
            recommendations.append(
                "🚨 ρ_PC Red Flag: Negative correlation detected. "
                "This is highly unusual and suggests potential cherry-picking or protocol gaming. "
                "Conduct thorough investigation."
            )
    
    # General recommendations
    recommendations.append(
        "📋 General: Pre-register evaluation protocol, use held-out test sets, "
        "and ensure blind evaluation where possible."
    )
    
    return recommendations


# Example usage
if __name__ == "__main__":
    print("=" * 70)
    print("Circular Bias Detection - Full Pipeline Test")
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
    
    # Run detection
    print("\n🔍 Running bias detection...")
    results = detect_circular_bias(df, run_bootstrap=False)
    
    # Display results
    print("\n" + "=" * 70)
    print("RESULTS")
    print("=" * 70)
    
    print(f"\n{results['interpretation']}")
    
    print("\n" + "=" * 70)
    print("DETAILED SCORES")
    print("=" * 70)
    
    print(f"\nPSI: {results['psi']['score']:.4f} (normalized: {results['psi']['normalized']:.4f})")
    print(f"CCS: {results['ccs']['score']:.4f} (normalized: {results['ccs']['normalized']:.4f})")
    print(f"ρ_PC: {results['rho_pc']['score']:.4f} (normalized: {results['rho_pc']['normalized']:.4f})")
    print(f"\nCBS: {results['cbs_score']:.4f}")
    print(f"Confidence: {results['confidence']:.1f}%")
    
    print("\n" + "=" * 70)
    print("RECOMMENDATIONS")
    print("=" * 70)
    
    for i, rec in enumerate(results['recommendations'], 1):
        print(f"\n{i}. {rec}")
    
    print("\n" + "=" * 70)
    print("TEST COMPLETED")
    print("=" * 70)
