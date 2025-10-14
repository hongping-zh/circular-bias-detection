"""
Example: Using Bootstrap Confidence Intervals and Adaptive Thresholds

This script demonstrates the enhanced statistical features:
1. Bootstrap resampling for confidence intervals and p-values
2. Adaptive threshold computation based on data
3. LLM evaluation bias detection
"""

import numpy as np
import pandas as pd
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from circular_bias_detector.core import (
    compute_psi, compute_ccs, compute_rho_pc,
    bootstrap_psi, bootstrap_ccs, bootstrap_rho_pc,
    compute_adaptive_thresholds
)

print("="*70)
print("BOOTSTRAP CONFIDENCE INTERVALS & ADAPTIVE THRESHOLDS DEMO")
print("="*70)

# Load LLM evaluation data
data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'llm_eval_sample.csv')
df = pd.read_csv(data_path)

print(f"\nLoaded data: {len(df)} rows, {len(df['time_period'].unique())} time periods")
print(f"Algorithms: {', '.join(df['algorithm'].unique())}")

# Prepare matrices
performance_matrix = df.pivot(
    index='time_period',
    columns='algorithm',
    values='performance'
).values

constraint_matrix = df.groupby('time_period')[[
    'constraint_compute',
    'constraint_memory',
    'constraint_dataset_size',
    'max_tokens',
    'temperature'
]].first().values

print(f"\nPerformance matrix shape: {performance_matrix.shape}")
print(f"Constraint matrix shape: {constraint_matrix.shape}")

# ============================================================================
# 1. POINT ESTIMATES (Traditional Method)
# ============================================================================

print("\n" + "="*70)
print("1. TRADITIONAL POINT ESTIMATES")
print("="*70)

psi_point = compute_psi(performance_matrix)
ccs_point = compute_ccs(constraint_matrix)
rho_point = compute_rho_pc(performance_matrix, constraint_matrix)

print(f"\nPSI Score: {psi_point:.4f}")
print(f"CCS Score: {ccs_point:.4f}")
print(f"ρ_PC Score: {rho_point:+.4f}")

# ============================================================================
# 2. BOOTSTRAP CONFIDENCE INTERVALS (Enhanced Method)
# ============================================================================

print("\n" + "="*70)
print("2. BOOTSTRAP CONFIDENCE INTERVALS (n=1000)")
print("="*70)

# PSI with Bootstrap
print("\n📊 PSI with Bootstrap:")
psi_boot = bootstrap_psi(performance_matrix, n_bootstrap=1000, random_seed=42)
print(f"   PSI = {psi_boot['psi']:.4f} [{psi_boot['ci_lower']:.4f} - {psi_boot['ci_upper']:.4f}]")
print(f"   p-value = {psi_boot['p_value']:.4f}")
print(f"   Standard Error = {psi_boot['std_error']:.4f}")

# CCS with Bootstrap
print("\n📊 CCS with Bootstrap:")
ccs_boot = bootstrap_ccs(constraint_matrix, n_bootstrap=1000, random_seed=42)
print(f"   CCS = {ccs_boot['ccs']:.4f} [{ccs_boot['ci_lower']:.4f} - {ccs_boot['ci_upper']:.4f}]")
print(f"   p-value = {ccs_boot['p_value']:.4f}")
print(f"   Standard Error = {ccs_boot['std_error']:.4f}")

# ρ_PC with Bootstrap
print("\n📊 ρ_PC with Bootstrap:")
rho_boot = bootstrap_rho_pc(performance_matrix, constraint_matrix, n_bootstrap=1000, random_seed=42)
print(f"   ρ_PC = {rho_boot['rho_pc']:+.4f} [{rho_boot['ci_lower']:+.4f} - {rho_boot['ci_upper']:+.4f}]")
print(f"   p-value = {rho_boot['p_value']:.4f}")
print(f"   Standard Error = {rho_boot['std_error']:.4f}")

# ============================================================================
# 3. ADAPTIVE THRESHOLDS (Data-Driven Method)
# ============================================================================

print("\n" + "="*70)
print("3. ADAPTIVE THRESHOLDS (95th percentile)")
print("="*70)

adaptive_thresholds = compute_adaptive_thresholds(
    performance_matrix, 
    constraint_matrix,
    quantile=0.95,
    n_simulations=500,
    random_seed=42
)

print("\n📈 Fixed vs. Adaptive Thresholds:")
print(f"\n   PSI Threshold:")
print(f"      Fixed:    0.15")
print(f"      Adaptive: {adaptive_thresholds['psi_threshold']:.4f}")

print(f"\n   CCS Threshold:")
print(f"      Fixed:    0.85")
print(f"      Adaptive: {adaptive_thresholds['ccs_threshold']:.4f}")

print(f"\n   ρ_PC Threshold:")
print(f"      Fixed:    0.50")
print(f"      Adaptive: {adaptive_thresholds['rho_pc_threshold']:.4f}")

# ============================================================================
# 4. BIAS DETECTION WITH BOTH METHODS
# ============================================================================

print("\n" + "="*70)
print("4. BIAS DETECTION COMPARISON")
print("="*70)

# Fixed thresholds
print("\n🔍 Using FIXED Thresholds:")
psi_bias_fixed = psi_point > 0.15
ccs_bias_fixed = ccs_point < 0.85
rho_bias_fixed = abs(rho_point) > 0.50

bias_votes_fixed = sum([psi_bias_fixed, ccs_bias_fixed, rho_bias_fixed])
overall_bias_fixed = bias_votes_fixed >= 2

print(f"   PSI > 0.15:       {'✗ YES' if psi_bias_fixed else '✓ NO'}")
print(f"   CCS < 0.85:       {'✗ YES' if ccs_bias_fixed else '✓ NO'}")
print(f"   |ρ_PC| > 0.50:    {'✗ YES' if rho_bias_fixed else '✓ NO'}")
print(f"\n   Overall Bias:     {'✗ DETECTED' if overall_bias_fixed else '✓ NOT DETECTED'}")
print(f"   Confidence:       {bias_votes_fixed / 3 * 100:.1f}%")

# Adaptive thresholds
print("\n🔍 Using ADAPTIVE Thresholds:")
psi_bias_adapt = psi_point > adaptive_thresholds['psi_threshold']
ccs_bias_adapt = ccs_point < adaptive_thresholds['ccs_threshold']
rho_bias_adapt = abs(rho_point) > adaptive_thresholds['rho_pc_threshold']

bias_votes_adapt = sum([psi_bias_adapt, ccs_bias_adapt, rho_bias_adapt])
overall_bias_adapt = bias_votes_adapt >= 2

print(f"   PSI > {adaptive_thresholds['psi_threshold']:.4f}:  {'✗ YES' if psi_bias_adapt else '✓ NO'}")
print(f"   CCS < {adaptive_thresholds['ccs_threshold']:.4f}:  {'✗ YES' if ccs_bias_adapt else '✓ NO'}")
print(f"   |ρ_PC| > {adaptive_thresholds['rho_pc_threshold']:.4f}: {'✗ YES' if rho_bias_adapt else '✓ NO'}")
print(f"\n   Overall Bias:     {'✗ DETECTED' if overall_bias_adapt else '✓ NOT DETECTED'}")
print(f"   Confidence:       {bias_votes_adapt / 3 * 100:.1f}%")

# ============================================================================
# 5. STATISTICAL SIGNIFICANCE
# ============================================================================

print("\n" + "="*70)
print("5. STATISTICAL SIGNIFICANCE (p < 0.05)")
print("="*70)

print(f"\n   PSI:  p = {psi_boot['p_value']:.4f}  {'✓ Significant' if psi_boot['p_value'] < 0.05 else '  Not significant'}")
print(f"   CCS:  p = {ccs_boot['p_value']:.4f}  {'✓ Significant' if ccs_boot['p_value'] < 0.05 else '  Not significant'}")
print(f"   ρ_PC: p = {rho_boot['p_value']:.4f}  {'✓ Significant' if rho_boot['p_value'] < 0.05 else '  Not significant'}")

# ============================================================================
# 6. FORMATTED OUTPUT FOR WEB APP
# ============================================================================

print("\n" + "="*70)
print("6. FORMATTED OUTPUT (Web App Style)")
print("="*70)

print(f"\nPSI Score:  {psi_boot['psi']:.4f} [{psi_boot['ci_lower']:.4f}-{psi_boot['ci_upper']:.4f}], p={psi_boot['p_value']:.3f}")
print(f"CCS Score:  {ccs_boot['ccs']:.4f} [{ccs_boot['ci_lower']:.4f}-{ccs_boot['ci_upper']:.4f}], p={ccs_boot['p_value']:.3f}")
print(f"ρ_PC Score: {rho_boot['rho_pc']:+.4f} [{rho_boot['ci_lower']:+.4f}-{rho_boot['ci_upper']:+.4f}], p={rho_boot['p_value']:.3f}")

# ============================================================================
# INTERPRETATION
# ============================================================================

print("\n" + "="*70)
print("💡 INTERPRETATION")
print("="*70)

print(f"""
LLM Evaluation Analysis Summary:

1. Performance-Structure Independence (PSI = {psi_boot['psi']:.4f}, p={psi_boot['p_value']:.3f}):
   - Measures parameter stability across prompt variants
   - {'High variability detected - prompts significantly affect results' if psi_boot['psi'] > 0.15 else 'Stable parameters across prompt variants'}

2. Constraint-Consistency Score (CCS = {ccs_boot['ccs']:.4f}, p={ccs_boot['p_value']:.3f}):
   - Measures consistency of sampling parameters (temperature, top_p, max_tokens)
   - {'Inconsistent sampling settings detected' if ccs_boot['ccs'] < 0.85 else 'Consistent sampling configuration'}

3. Performance-Constraint Correlation (ρ_PC = {rho_boot['rho_pc']:+.4f}, p={rho_boot['p_value']:.3f}):
   - Correlation between performance and constraint adjustments
   - {'Strong correlation suggests constraints tuned to improve scores' if abs(rho_boot['rho_pc']) > 0.5 else 'Weak correlation indicates independent constraint settings'}

Overall Assessment: {'⚠️ CIRCULAR BIAS DETECTED' if overall_bias_adapt else '✓ EVALUATION APPEARS SOUND'}

{'High correlation (ρ_PC=' + f'{rho_boot["rho_pc"]:.2f}' + ') indicates prompt engineering and sampling ' + 
'parameters may have been iteratively adjusted to inflate performance.' if abs(rho_boot['rho_pc']) > 0.5 else 
'Evaluation methodology appears sound with minimal evidence of circular bias.'}
""")

print("="*70)
print("✅ Analysis Complete!")
print("="*70)
