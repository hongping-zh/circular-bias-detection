#!/usr/bin/env python3
"""
Basic usage example for the Circular Reasoning Bias Detection Framework.
This script demonstrates how to use the BiasDetector class for bias detection.
"""

import numpy as np
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from circular_bias_detector import BiasDetector
from circular_bias_detector.utils import create_synthetic_data

def main():
    """Demonstrate basic usage of the BiasDetector."""
    
    print("🔍 Circular Reasoning Bias Detection - Basic Example")
    print("=" * 60)
    
    # Create synthetic evaluation data
    print("📊 Generating synthetic evaluation data...")
    
    # Case 1: Clean evaluation (no bias)
    print("\n1. CLEAN EVALUATION (No Bias Expected)")
    print("-" * 40)
    
    perf_clean, const_clean = create_synthetic_data(
        n_time_periods=15,
        n_algorithms=4,
        n_constraints=3,
        bias_intensity=0.0,  # No bias
        random_seed=42
    )
    
    # Initialize detector
    detector = BiasDetector()
    
    # Detect bias
    results_clean = detector.detect_bias(
        performance_matrix=perf_clean,
        constraint_matrix=const_clean,
        algorithm_names=['ResNet', 'VGG', 'DenseNet', 'EfficientNet']
    )
    
    # Print results
    print(f"PSI Score: {results_clean['psi_score']:.4f}")
    print(f"CCS Score: {results_clean['ccs_score']:.4f}")
    print(f"ρ_PC Score: {results_clean['rho_pc_score']:+.4f}")
    print(f"Bias Detected: {results_clean['overall_bias']}")
    print(f"Confidence: {results_clean['confidence']:.1%}")
    
    # Case 2: Biased evaluation
    print("\n2. BIASED EVALUATION (Bias Expected)")
    print("-" * 40)
    
    perf_biased, const_biased = create_synthetic_data(
        n_time_periods=15,
        n_algorithms=4,
        n_constraints=3,
        bias_intensity=0.8,  # High bias
        random_seed=123
    )
    
    results_biased = detector.detect_bias(
        performance_matrix=perf_biased,
        constraint_matrix=const_biased,
        algorithm_names=['ResNet', 'VGG', 'DenseNet', 'EfficientNet']
    )
    
    print(f"PSI Score: {results_biased['psi_score']:.4f}")
    print(f"CCS Score: {results_biased['ccs_score']:.4f}")
    print(f"ρ_PC Score: {results_biased['rho_pc_score']:+.4f}")
    print(f"Bias Detected: {results_biased['overall_bias']}")
    print(f"Confidence: {results_biased['confidence']:.1%}")
    
    # Generate detailed reports
    print("\n" + "=" * 60)
    print("DETAILED CLEAN EVALUATION REPORT")
    print("=" * 60)
    print(detector.generate_report(results_clean))
    
    print("\n" + "=" * 60)
    print("DETAILED BIASED EVALUATION REPORT")
    print("=" * 60)
    print(detector.generate_report(results_biased))
    
    # Save results
    from circular_bias_detector.utils import save_results_json
    
    save_results_json(results_clean, 'clean_evaluation_results.json')
    save_results_json(results_biased, 'biased_evaluation_results.json')
    
    print("\n✅ Results saved to JSON files:")
    print("   • clean_evaluation_results.json")
    print("   • biased_evaluation_results.json")
    
    # Demonstrate plotting (if matplotlib available)
    try:
        print("\n📈 Generating visualization plots...")
        detector.plot_indicators(results_clean, 'clean_evaluation_plot.png')
        detector.plot_indicators(results_biased, 'biased_evaluation_plot.png')
        print("✅ Plots saved:")
        print("   • clean_evaluation_plot.png")
        print("   • biased_evaluation_plot.png")
    except ImportError:
        print("⚠️  Matplotlib not available - skipping plots")
    
    print(f"\n🎯 Example completed successfully!")
    print(f"📖 See generated files for detailed results")

if __name__ == "__main__":
    main()
