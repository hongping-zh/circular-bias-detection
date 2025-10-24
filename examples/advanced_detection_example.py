#!/usr/bin/env python3
"""
Advanced Detection Example: Showcasing new metrics and ML integration.

This example demonstrates:
1. New advanced metrics (TDI, ICS, CBI, ADS, MCI)
2. ML-based detection with XGBoost
3. Ensemble detection combining statistical and ML approaches
"""

import numpy as np
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from circular_bias_detector.utils import create_synthetic_data
from circular_bias_detector.advanced_metrics import (
    compute_tdi, compute_ics, compute_cbi, 
    compute_ads, compute_mci, compute_all_advanced_metrics
)


def demo_advanced_metrics():
    """Demonstrate new advanced detection metrics."""
    
    print("=" * 70)
    print("DEMO 1: Advanced Detection Metrics")
    print("=" * 70)
    
    # Generate test data
    print("\n📊 Generating synthetic evaluation data...")
    perf_clean, const_clean = create_synthetic_data(
        n_time_periods=20,
        n_algorithms=5,
        n_constraints=3,
        bias_intensity=0.0,
        random_seed=42
    )
    
    perf_biased, const_biased = create_synthetic_data(
        n_time_periods=20,
        n_algorithms=5,
        n_constraints=3,
        bias_intensity=0.8,
        random_seed=123
    )
    
    # Test on clean data
    print("\n🟢 Testing on CLEAN evaluation data:")
    print("-" * 50)
    
    tdi_clean = compute_tdi(perf_clean)
    ics_clean = compute_ics(perf_clean, const_clean)
    ads_clean = compute_ads(perf_clean, const_clean)
    mci_clean, mci_corr_clean = compute_mci(const_clean)
    
    print(f"TDI (Temporal Dependency):     {tdi_clean:.4f} {'✓' if tdi_clean < 0.6 else '⚠'}")
    print(f"ICS (Information Criterion):   {ics_clean:+.4f} {'✓' if ics_clean > -0.5 else '⚠'}")
    print(f"ADS (Adaptive Drift):          {ads_clean:.4f} {'✓' if ads_clean < 0.3 else '⚠'}")
    print(f"MCI (Multi-Constraint):        {mci_clean:.4f} {'✓' if mci_clean < 0.8 else '⚠'}")
    
    # Test on biased data
    print("\n🔴 Testing on BIASED evaluation data:")
    print("-" * 50)
    
    tdi_biased = compute_tdi(perf_biased)
    ics_biased = compute_ics(perf_biased, const_biased)
    ads_biased = compute_ads(perf_biased, const_biased)
    mci_biased, mci_corr_biased = compute_mci(const_biased)
    
    print(f"TDI (Temporal Dependency):     {tdi_biased:.4f} {'✓' if tdi_biased < 0.6 else '⚠'}")
    print(f"ICS (Information Criterion):   {ics_biased:+.4f} {'✓' if ics_biased > -0.5 else '⚠'}")
    print(f"ADS (Adaptive Drift):          {ads_biased:.4f} {'✓' if ads_biased < 0.3 else '⚠'}")
    print(f"MCI (Multi-Constraint):        {mci_biased:.4f} {'✓' if mci_biased < 0.8 else '⚠'}")
    
    # Compute all at once
    print("\n📈 Computing all advanced metrics at once:")
    all_metrics = compute_all_advanced_metrics(perf_biased, const_biased)
    
    for key, value in all_metrics.items():
        if key != 'mci_correlation_matrix':
            print(f"  {key.upper()}: {value}")


def demo_cross_benchmark():
    """Demonstrate Cross-Benchmark Inconsistency (CBI) metric."""
    
    print("\n" + "=" * 70)
    print("DEMO 2: Cross-Benchmark Inconsistency Detection")
    print("=" * 70)
    
    # Simulate evaluation on multiple benchmarks
    print("\n📊 Simulating multi-benchmark evaluation...")
    
    # 4 algorithms, 3 time periods per benchmark, 2 benchmarks
    T = 6
    K = 4
    
    # Performance on benchmark A (periods 0-2)
    perf_A = np.array([
        [0.85, 0.80, 0.75, 0.70],
        [0.86, 0.81, 0.76, 0.71],
        [0.87, 0.82, 0.77, 0.72]
    ])
    
    # Performance on benchmark B (periods 3-5)
    # Rankings should be consistent if unbiased
    perf_B_consistent = np.array([
        [0.83, 0.78, 0.73, 0.68],
        [0.84, 0.79, 0.74, 0.69],
        [0.85, 0.80, 0.75, 0.70]
    ])
    
    # Rankings inconsistent (potential benchmark-specific tuning)
    perf_B_inconsistent = np.array([
        [0.70, 0.85, 0.75, 0.80],  # Algorithm rankings reversed!
        [0.71, 0.86, 0.76, 0.81],
        [0.72, 0.87, 0.77, 0.82]
    ])
    
    # Test consistent case
    perf_consistent = np.vstack([perf_A, perf_B_consistent])
    benchmark_ids_consistent = np.array([0, 0, 0, 1, 1, 1])
    
    cbi_consistent = compute_cbi(perf_consistent, benchmark_ids_consistent)
    
    print("\n🟢 Scenario 1: Consistent across benchmarks")
    print(f"CBI Score: {cbi_consistent:.4f}")
    print(f"Status: {'✓ CONSISTENT' if cbi_consistent < 0.4 else '⚠ INCONSISTENT'}")
    
    # Test inconsistent case
    perf_inconsistent = np.vstack([perf_A, perf_B_inconsistent])
    benchmark_ids_inconsistent = np.array([0, 0, 0, 1, 1, 1])
    
    cbi_inconsistent = compute_cbi(perf_inconsistent, benchmark_ids_inconsistent)
    
    print("\n🔴 Scenario 2: Inconsistent across benchmarks")
    print(f"CBI Score: {cbi_inconsistent:.4f}")
    print(f"Status: {'✓ CONSISTENT' if cbi_inconsistent < 0.4 else '⚠ INCONSISTENT'}")
    print("\nInterpretation: High CBI suggests potential benchmark selection bias")


def demo_ml_detection():
    """Demonstrate ML-based bias detection."""
    
    print("\n" + "=" * 70)
    print("DEMO 3: Machine Learning-Based Detection")
    print("=" * 70)
    
    try:
        from circular_bias_detector.ml_detector import MLBiasDetector
    except ImportError as e:
        print(f"\n⚠️  ML detection requires additional dependencies:")
        print("   pip install xgboost scikit-learn")
        print(f"\n   Error: {e}")
        return
    
    print("\n📊 Generating training dataset...")
    
    # Generate training data
    n_samples = 100
    X_train = []
    y_train = []
    
    for i in range(n_samples):
        bias_intensity = np.random.rand()
        perf, const = create_synthetic_data(
            n_time_periods=15,
            n_algorithms=4,
            n_constraints=3,
            bias_intensity=bias_intensity,
            random_seed=i
        )
        
        detector = MLBiasDetector()
        features = detector.extract_features(perf, const)
        
        X_train.append(features)
        y_train.append(1 if bias_intensity > 0.5 else 0)
    
    X_train = np.array(X_train)
    y_train = np.array(y_train)
    
    print(f"Training samples: {len(X_train)}")
    print(f"  - No bias: {np.sum(y_train == 0)}")
    print(f"  - Bias: {np.sum(y_train == 1)}")
    print(f"Features extracted: {X_train.shape[1]}")
    
    # Train model
    print("\n🤖 Training ML model...")
    ml_detector = MLBiasDetector()
    ml_detector.train(X_train, y_train)
    
    # Test on new samples
    print("\n🧪 Testing on new samples...")
    
    test_cases = [
        (0.0, "Clean evaluation"),
        (0.8, "Biased evaluation")
    ]
    
    for bias_level, description in test_cases:
        perf_test, const_test = create_synthetic_data(
            n_time_periods=15,
            n_algorithms=4,
            n_constraints=3,
            bias_intensity=bias_level,
            random_seed=999 + int(bias_level * 100)
        )
        
        features_test = ml_detector.extract_features(perf_test, const_test).reshape(1, -1)
        pred, prob = ml_detector.predict(features_test)
        
        print(f"\n{description} (bias_intensity={bias_level})")
        print(f"  Prediction: {'BIAS DETECTED' if pred[0] == 1 else 'NO BIAS'}")
        print(f"  Probability: {prob[0]:.3f}")
    
    # Feature importance
    print("\n📊 Top 5 Most Important Features:")
    importance_df = ml_detector.get_feature_importance()
    print(importance_df.head())


def demo_ensemble_detection():
    """Demonstrate ensemble detection."""
    
    print("\n" + "=" * 70)
    print("DEMO 4: Ensemble Detection (Statistical + ML)")
    print("=" * 70)
    
    try:
        from circular_bias_detector.ml_detector import EnsembleBiasDetector, MLBiasDetector
    except ImportError:
        print("\n⚠️  Ensemble detection requires xgboost and scikit-learn")
        return
    
    # First train the ML component
    print("\n🔧 Setting up ensemble detector...")
    print("(Training ML component on synthetic data...)")
    
    # Quick training
    ml_detector = MLBiasDetector()
    X_train = []
    y_train = []
    
    for i in range(50):
        bias_level = 1 if i % 2 == 0 else 0
        perf, const = create_synthetic_data(
            n_time_periods=12,
            n_algorithms=3,
            n_constraints=2,
            bias_intensity=0.8 * bias_level,
            random_seed=i
        )
        features = ml_detector.extract_features(perf, const)
        X_train.append(features)
        y_train.append(bias_level)
    
    ml_detector.train(np.array(X_train), np.array(y_train))
    
    # Create ensemble
    ensemble = EnsembleBiasDetector(statistical_weight=0.6, ml_weight=0.4)
    ensemble.ml_detector = ml_detector
    
    # Test
    print("\n🧪 Testing ensemble detection...")
    
    perf_test, const_test = create_synthetic_data(
        n_time_periods=15,
        n_algorithms=4,
        n_constraints=3,
        bias_intensity=0.6,
        random_seed=777
    )
    
    results = ensemble.detect_bias(
        perf_test, const_test,
        algorithm_names=['AlgA', 'AlgB', 'AlgC', 'AlgD']
    )
    
    print(f"\n{'='*50}")
    print(f"Bias Detected: {results['bias_detected']}")
    print(f"{'='*50}")
    print(f"Ensemble Score:        {results['ensemble_score']:.3f}")
    print(f"Calibrated Confidence: {results['calibrated_confidence']:.3f}")
    print(f"\nComponent Scores:")
    print(f"  Statistical: {results['statistical_score']:.3f}")
    print(f"  ML:          {results['ml_score']:.3f}")
    print(f"  Agreement:   {results['method_agreement']:.3f}")
    print(f"\nWeights: Statistical={results['weights']['statistical']:.1f}, ML={results['weights']['ml']:.1f}")


def main():
    """Run all demonstrations."""
    
    print("\n" + "🔬" * 35)
    print("ADVANCED BIAS DETECTION - COMPREHENSIVE DEMO")
    print("🔬" * 35)
    
    # Demo 1: Advanced metrics
    demo_advanced_metrics()
    
    # Demo 2: Cross-benchmark inconsistency
    demo_cross_benchmark()
    
    # Demo 3: ML detection
    demo_ml_detection()
    
    # Demo 4: Ensemble detection
    demo_ensemble_detection()
    
    print("\n" + "="*70)
    print("✅ All demonstrations completed!")
    print("="*70)
    print("\n💡 Next steps:")
    print("   1. Explore advanced_metrics.py for metric implementations")
    print("   2. Check ml_detector.py for ML integration details")
    print("   3. Train ML model on your own labeled data")
    print("   4. Integrate into your evaluation pipeline")


if __name__ == "__main__":
    main()
