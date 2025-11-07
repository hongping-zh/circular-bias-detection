"""
Test script to verify circular-bias-detector integration
"""

import pandas as pd
from adapters.bias_detector_adapter import detect_circular_bias

# Create sample data
print("=" * 70)
print("Testing circular-bias-detector Integration")
print("=" * 70)

# Sample evaluation data
data = pd.DataFrame({
    'time_period': [1, 1, 2, 2, 3, 3, 4, 4],
    'algorithm': ['A', 'B'] * 4,
    'performance': [0.7, 0.6, 0.72, 0.65, 0.74, 0.67, 0.76, 0.69],
    'constraint_compute': [100, 150, 105, 155, 110, 160, 115, 165],
    'constraint_memory': [8.0, 12.0, 8.5, 12.5, 9.0, 13.0, 9.5, 13.5]
})

print(f"\n[Data] Loaded {len(data)} rows")
print(f"[Data] Algorithms: {data['algorithm'].unique().tolist()}")
print(f"[Data] Time periods: {sorted(data['time_period'].unique())}")

# Run detection
print("\n" + "=" * 70)
print("Running Bias Detection...")
print("=" * 70 + "\n")

try:
    results = detect_circular_bias(data, run_bootstrap=False)
    
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
    print(f"rho_PC: {results['rho_pc']['score']:.4f} (normalized: {results['rho_pc']['normalized']:.4f})")
    print(f"\nCBS: {results['cbs_score']:.4f}")
    print(f"Risk Level: {results['risk_level']}")
    print(f"Confidence: {results['confidence']:.1f}%")
    
    print("\n" + "=" * 70)
    print("RECOMMENDATIONS")
    print("=" * 70)
    
    for i, rec in enumerate(results['recommendations'], 1):
        print(f"\n{i}. {rec}")
    
    print("\n" + "=" * 70)
    print("[SUCCESS] Integration test completed successfully!")
    print("=" * 70)
    
except Exception as e:
    print(f"\n[ERROR] Test failed: {str(e)}")
    import traceback
    traceback.print_exc()
