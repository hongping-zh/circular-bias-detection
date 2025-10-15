"""
Quick test script for PSI Calculator

Run this to verify PSI implementation without pytest.
"""

import pandas as pd
from core.psi_calculator import compute_psi, compute_psi_per_algorithm

def main():
    print("=" * 70)
    print("PSI Calculator - Quick Test")
    print("=" * 70)
    
    # Load sample data
    print("\n📂 Loading sample data...")
    try:
        df = pd.read_csv('data/sample_data.csv')
        print(f"✓ Loaded {len(df)} rows, {len(df.columns)} columns")
        print(f"  Algorithms: {', '.join(df['algorithm'].unique())}")
        print(f"  Time periods: {len(df['time_period'].unique())}")
    except FileNotFoundError:
        print("✗ sample_data.csv not found, creating synthetic data...")
        df = pd.DataFrame({
            'time_period': [1, 1, 2, 2, 3, 3, 4, 4],
            'algorithm': ['A', 'B'] * 4,
            'performance': [0.7, 0.6, 0.72, 0.65, 0.74, 0.67, 0.76, 0.69],
            'constraint_compute': [100, 150, 105, 155, 110, 160, 115, 165],
            'constraint_memory': [8.0, 12.0, 8.5, 12.5, 9.0, 13.0, 9.5, 13.5]
        })
    
    # Compute PSI
    print("\n🔬 Computing PSI...")
    result = compute_psi(df)
    
    print("\n" + "=" * 70)
    print("RESULTS")
    print("=" * 70)
    
    print(f"\n📊 PSI Score: {result['psi_score']:.4f}")
    print(f"   Threshold: {result['threshold']}")
    print(f"   Status: {'⚠️ EXCEEDS THRESHOLD' if result['exceeds_threshold'] else '✓ Below threshold'}")
    
    print(f"\n📈 Analysis:")
    print(f"   Time periods analyzed: {result['num_periods']}")
    print(f"   Constraint columns: {result['num_constraints']}")
    
    print(f"\n💡 Interpretation:")
    print(f"   {result['interpretation']}")
    
    if result['psi_by_period']:
        print(f"\n📉 Per-Period Parameter Changes:")
        for i, dist in enumerate(result['psi_by_period'], 1):
            print(f"   Period {i} → {i+1}: {dist:.4f}")
    
    # Per-algorithm analysis
    print("\n" + "=" * 70)
    print("PER-ALGORITHM ANALYSIS")
    print("=" * 70)
    
    per_algo = compute_psi_per_algorithm(df)
    for algo, res in per_algo.items():
        if 'error' in res:
            print(f"\n{algo}: ✗ {res['error']}")
        else:
            status = "⚠️" if res['exceeds_threshold'] else "✓"
            print(f"\n{algo}: {status} PSI = {res['psi_score']:.4f}")
    
    print("\n" + "=" * 70)
    print("TEST COMPLETED")
    print("=" * 70)
    
    # Summary
    print("\n✅ PSI calculation successful!")
    print("   Next steps:")
    print("   1. Implement CCS calculator (Day 2)")
    print("   2. Implement ρ_PC calculator (Day 2)")
    print("   3. Add bootstrap confidence intervals (Day 3)")
    
    return result

if __name__ == "__main__":
    main()
