"""
LLM Evaluation Bias Detection Example

This script demonstrates how to detect circular bias in LLM evaluation,
particularly when prompt engineering and sampling parameters are iteratively
tuned to improve benchmark scores.

Use case: Detecting bias in GLUE benchmark evaluations where:
- Prompts are iteratively modified (vanilla → few-shot → chain-of-thought)
- Sampling parameters are adjusted (temperature, top_p)
- Dataset and compute resources are scaled
"""

import numpy as np
import pandas as pd
from circular_bias_detector import BiasDetector

# Load LLM evaluation data
print("=" * 60)
print("LLM EVALUATION BIAS DETECTION")
print("=" * 60)
print("\nLoading LLM evaluation data from GLUE benchmark...")

df = pd.read_csv('data/llm_eval_sample.csv')

print(f"\nDataset shape: {df.shape}")
print(f"Time periods: {df['time_period'].nunique()}")
print(f"LLMs evaluated: {df['algorithm'].unique().tolist()}")
print(f"\nPrompt variants: {df['prompt_variant'].unique().tolist()}")

# Prepare performance matrix (T x K)
performance_matrix = df.pivot(
    index='time_period',
    columns='algorithm',
    values='performance'
).values

algorithms = df['algorithm'].unique().tolist()

# Prepare constraint matrix including LLM-specific constraints
# Traditional constraints: compute, memory, dataset_size
# LLM-specific: max_tokens, temperature, top_p
constraint_columns = [
    'constraint_compute',
    'constraint_memory',
    'constraint_dataset_size',
    'max_tokens',      # LLM-specific
    'temperature'      # LLM-specific
]

constraint_matrix = df.groupby('time_period')[constraint_columns].first().values

print(f"\nConstraint types: {len(constraint_columns)}")
print("  - Traditional: compute, memory, dataset_size")
print("  - LLM-specific: max_tokens, temperature")

# Standard detection (without bootstrap)
print("\n" + "=" * 60)
print("STANDARD DETECTION (Fast)")
print("=" * 60)

detector = BiasDetector(
    psi_threshold=0.15,
    ccs_threshold=0.85,
    rho_pc_threshold=0.5
)

results_standard = detector.detect_bias(
    performance_matrix=performance_matrix,
    constraint_matrix=constraint_matrix,
    algorithm_names=algorithms
)

print(f"\nPSI:  {results_standard['psi_score']:.4f} (threshold: 0.15)")
print(f"CCS:  {results_standard['ccs_score']:.4f} (threshold: 0.85)")
print(f"ρ_PC: {results_standard['rho_pc_score']:+.4f} (threshold: ±0.5)")
print(f"\nBias detected: {'YES ⚠️' if results_standard['overall_bias'] else 'NO ✅'}")
print(f"Confidence: {results_standard['confidence']:.1%}")

# Enhanced detection with Bootstrap (statistical significance)
print("\n" + "=" * 60)
print("ENHANCED DETECTION WITH BOOTSTRAP (n=1000)")
print("=" * 60)
print("Computing confidence intervals and p-values...")

results_bootstrap = detector.detect_bias(
    performance_matrix=performance_matrix,
    constraint_matrix=constraint_matrix,
    algorithm_names=algorithms,
    enable_bootstrap=True,
    n_bootstrap=1000
)

print("\nResults with 95% confidence intervals:")
print(f"PSI:  {results_bootstrap['psi_score']:.4f} "
      f"[{results_bootstrap['psi_ci_lower']:.4f}-{results_bootstrap['psi_ci_upper']:.4f}], "
      f"p={results_bootstrap['psi_pvalue']:.3f}")

print(f"CCS:  {results_bootstrap['ccs_score']:.4f} "
      f"[{results_bootstrap['ccs_ci_lower']:.4f}-{results_bootstrap['ccs_ci_upper']:.4f}], "
      f"p={results_bootstrap['ccs_pvalue']:.3f}")

print(f"ρ_PC: {results_bootstrap['rho_pc_score']:+.4f} "
      f"[{results_bootstrap['rho_pc_ci_lower']:+.4f}-{results_bootstrap['rho_pc_ci_upper']:+.4f}], "
      f"p={results_bootstrap['rho_pc_pvalue']:.3f}")

# Interpretation
print("\n" + "=" * 60)
print("INTERPRETATION FOR LLM EVALUATION")
print("=" * 60)

if abs(results_bootstrap['rho_pc_score']) > 0.5:
    print("\n⚠️  HIGH CORRELATION DETECTED (ρ_PC > 0.5)")
    print("    This suggests that:")
    print("    1. Sampling parameters (temperature, top_p) were likely")
    print("       adjusted in response to observed scores")
    print("    2. Prompt engineering variants correlate with score improvements")
    print("    3. Evaluation protocol may have circular dependency")
    print("\n    ⚠️  RECOMMENDATION:")
    print("    - Pre-register evaluation protocol before experiments")
    print("    - Fix sampling parameters across all time periods")
    print("    - Use held-out test set for final evaluation")
    
if results_bootstrap['psi_score'] > 0.15:
    print("\n⚠️  HIGH PSI DETECTED")
    print("    Parameter instability suggests model configurations")
    print("    were modified during evaluation.")
    
if results_bootstrap['ccs_score'] < 0.85:
    print("\n⚠️  LOW CCS DETECTED")
    print("    Constraint inconsistency suggests evaluation resources")
    print("    were adjusted between time periods.")

# Adaptive thresholds (data-driven)
print("\n" + "=" * 60)
print("DATA-ADAPTIVE THRESHOLDS")
print("=" * 60)
print("Computing adaptive thresholds from null distribution...")

results_adaptive = detector.detect_bias(
    performance_matrix=performance_matrix,
    constraint_matrix=constraint_matrix,
    algorithm_names=algorithms,
    enable_adaptive_thresholds=True,
    enable_bootstrap=True,
    n_bootstrap=500  # Fewer iterations for speed
)

print(f"\nAdaptive thresholds (95th percentile):")
print(f"  PSI:  {results_adaptive['metadata']['thresholds']['psi']:.4f}")
print(f"  CCS:  {results_adaptive['metadata']['thresholds']['ccs']:.4f}")
print(f"  ρ_PC: {results_adaptive['metadata']['thresholds']['rho_pc']:.4f}")

print(f"\nBias detected: {'YES ⚠️' if results_adaptive['overall_bias'] else 'NO ✅'}")

# Generate detailed report
print("\n" + "=" * 60)
print("DETAILED REPORT")
print("=" * 60)
report = detector.generate_report(results_bootstrap)
print(report)

# Save results to JSON
import json

output_file = 'llm_bias_detection_results.json'
with open(output_file, 'w') as f:
    # Convert numpy types to Python types for JSON serialization
    json_results = {
        'standard': {k: float(v) if isinstance(v, np.number) else v 
                    for k, v in results_standard.items() if k != 'metadata'},
        'bootstrap': {k: float(v) if isinstance(v, np.number) else v 
                     for k, v in results_bootstrap.items() if k != 'metadata'},
        'adaptive': {k: float(v) if isinstance(v, np.number) else v 
                    for k, v in results_adaptive.items() if k != 'metadata'}
    }
    json.dump(json_results, f, indent=2)

print(f"\n✅ Results saved to: {output_file}")

print("\n" + "=" * 60)
print("KEY TAKEAWAYS")
print("=" * 60)
print("✓ Use enable_bootstrap=True for statistical significance")
print("✓ Use enable_adaptive_thresholds=True for data-driven cutoffs")
print("✓ High ρ_PC indicates prompt/parameter tuning bias")
print("✓ Monitor temperature and top_p as additional constraints")
print("✓ Pre-register evaluation protocols to prevent circular bias")
print("=" * 60)
