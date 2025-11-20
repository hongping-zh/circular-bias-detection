"""
Example: Retrain-Null Permutation Testing

This example demonstrates how to use retrain-null permutation testing
for conservative bias detection in machine learning models.
"""

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import make_classification
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split

from circular_bias_detector.core.permutation import retrain_null_test


def example_basic_retrain_null():
    """Basic retrain-null test example."""
    print("=" * 60)
    print("Example 1: Basic Retrain-Null Test")
    print("=" * 60)
    
    # Generate synthetic data
    X, y = make_classification(
        n_samples=200,
        n_features=20,
        n_informative=15,
        n_redundant=5,
        random_state=42
    )
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )
    
    print(f"\nData: {len(X_train)} train, {len(X_test)} test samples")
    
    # Define model factory
    def model_factory():
        return RandomForestClassifier(
            n_estimators=50,
            max_depth=5,
            random_state=42
        )
    
    # Run retrain-null test
    print("\nRunning retrain-null test (this may take a minute)...")
    results = retrain_null_test(
        X_train, y_train,
        X_test, y_test,
        model_factory=model_factory,
        metric_func=accuracy_score,
        n_permutations=50,  # Small for demo
        random_seed=42,
        n_jobs=-1,
        backend='processes',
        verbose=1
    )
    
    print(f"\nResults:")
    print(f"  Observed accuracy: {results['observed']:.4f}")
    print(f"  Null mean: {np.mean(results['permuted_values']):.4f}")
    print(f"  Null std: {np.std(results['permuted_values']):.4f}")
    print(f"  95% CI: [{results['ci_lower']:.4f}, {results['ci_upper']:.4f}]")
    print(f"  p-value: {results['p_value']:.4f}")
    print(f"  Permutations: {results['n_permutations']}")
    
    if results['p_value'] < 0.05:
        print("\n✅ Model performance is significantly better than random!")
    else:
        print("\n⚠️  Model performance not significantly different from random.")


def example_stratified_retrain_null():
    """Retrain-null with stratified permutation for imbalanced data."""
    print("\n" + "=" * 60)
    print("Example 2: Stratified Retrain-Null (Imbalanced Data)")
    print("=" * 60)
    
    # Generate imbalanced data
    X, y = make_classification(
        n_samples=200,
        n_features=15,
        n_informative=10,
        n_classes=2,
        weights=[0.9, 0.1],  # 90% class 0, 10% class 1
        random_state=42
    )
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, stratify=y, random_state=42
    )
    
    print(f"\nClass distribution in training:")
    print(f"  Class 0: {np.sum(y_train == 0)} ({np.mean(y_train == 0):.1%})")
    print(f"  Class 1: {np.sum(y_train == 1)} ({np.mean(y_train == 1):.1%})")
    
    def model_factory():
        return DecisionTreeClassifier(max_depth=5, random_state=42)
    
    # Test WITHOUT stratification
    print("\nTest 1: Without stratification...")
    results_unstratified = retrain_null_test(
        X_train, y_train, X_test, y_test,
        model_factory=model_factory,
        metric_func=accuracy_score,
        n_permutations=30,
        random_seed=42,
        n_jobs=-1,
        stratify_groups=None  # No stratification
    )
    
    # Test WITH stratification
    print("\nTest 2: With stratification...")
    results_stratified = retrain_null_test(
        X_train, y_train, X_test, y_test,
        model_factory=model_factory,
        metric_func=accuracy_score,
        n_permutations=30,
        random_seed=42,
        n_jobs=-1,
        stratify_groups=y_train  # Stratify by class
    )
    
    print(f"\nComparison:")
    print(f"  Observed: {results_stratified['observed']:.4f}")
    print(f"  Without stratification - Null mean: {np.mean(results_unstratified['permuted_values']):.4f}")
    print(f"  With stratification    - Null mean: {np.mean(results_stratified['permuted_values']):.4f}")
    print(f"  Without stratification - p-value: {results_unstratified['p_value']:.4f}")
    print(f"  With stratification    - p-value: {results_stratified['p_value']:.4f}")
    
    print("\n💡 Stratification preserves class balance in permutations,")
    print("   providing a more appropriate null distribution.")


def example_probability_metric():
    """Retrain-null with probability-based metric (AUC)."""
    print("\n" + "=" * 60)
    print("Example 3: Retrain-Null with AUC Metric")
    print("=" * 60)
    
    # Generate data
    X, y = make_classification(
        n_samples=200,
        n_features=15,
        n_informative=10,
        random_state=42
    )
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )
    
    def model_factory():
        return RandomForestClassifier(
            n_estimators=30,
            max_depth=4,
            random_state=42
        )
    
    # Custom metric that uses predict_proba
    def auc_metric(y_true, y_pred_proba):
        """AUC metric using probabilities."""
        return roc_auc_score(y_true, y_pred_proba)
    
    # Wrapper to get probabilities from model
    def model_predict_proba(model, X):
        return model.predict_proba(X)[:, 1]
    
    # Modified retrain worker for probability metrics
    print("\nRunning retrain-null test with AUC...")
    
    # Train observed model
    model_obs = model_factory()
    model_obs.fit(X_train, y_train)
    y_pred_proba = model_obs.predict_proba(X_test)[:, 1]
    observed_auc = roc_auc_score(y_test, y_pred_proba)
    
    print(f"\nObserved AUC: {observed_auc:.4f}")
    
    # For probability metrics, we need a custom approach
    # (Standard retrain_null_test uses predict, not predict_proba)
    print("\n💡 For probability-based metrics, consider using standard")
    print("   permutation_test on the metric values directly, or")
    print("   implement a custom retrain worker.")


def example_comparison_with_standard():
    """Compare retrain-null with standard permutation test."""
    print("\n" + "=" * 60)
    print("Example 4: Retrain-Null vs Standard Permutation Test")
    print("=" * 60)
    
    from circular_bias_detector.core.permutation import permutation_test
    from circular_bias_detector.core.metrics import compute_psi
    
    # Generate evaluation time series data
    np.random.seed(42)
    T, K, p = 15, 4, 2
    perf_matrix = np.random.rand(T, K)
    const_matrix = np.random.rand(T, p)
    
    print(f"\nData: {T} time periods, {K} algorithms")
    
    # Standard permutation test
    print("\nRunning standard permutation test...")
    standard_results = permutation_test(
        perf_matrix, const_matrix, compute_psi,
        n_permutations=500,
        random_seed=42,
        n_jobs=-1
    )
    
    print(f"  Observed PSI: {standard_results['observed']:.4f}")
    print(f"  p-value: {standard_results['p_value']:.4f}")
    print(f"  Time: Fast (seconds)")
    
    # Note: Retrain-null is for ML models, not for PSI/CCS/rho_PC
    print("\n💡 Comparison:")
    print("  Standard permutation test:")
    print("    - Fast (permutes data only)")
    print("    - Good for PSI, CCS, ρ_PC metrics")
    print("    - Assumes metric is stable")
    print("\n  Retrain-null test:")
    print("    - Slow (retrains model each time)")
    print("    - Good for ML model evaluation")
    print("    - More conservative")
    print("    - Accounts for model variability")


def example_cost_analysis():
    """Demonstrate computational cost of retrain-null."""
    print("\n" + "=" * 60)
    print("Example 5: Computational Cost Analysis")
    print("=" * 60)
    
    import time
    
    # Small dataset for timing
    X, y = make_classification(
        n_samples=100,
        n_features=10,
        random_state=42
    )
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )
    
    def model_factory():
        return DecisionTreeClassifier(max_depth=3, random_state=42)
    
    # Time a single model training
    start = time.time()
    model = model_factory()
    model.fit(X_train, y_train)
    single_train_time = time.time() - start
    
    print(f"\nSingle model training time: {single_train_time:.3f} seconds")
    
    # Estimate costs
    n_perms = [10, 50, 100, 500]
    n_jobs_options = [1, 2, 4, -1]
    
    print(f"\nEstimated time for different configurations:")
    print(f"{'n_perm':<10} {'n_jobs':<10} {'Est. Time (seq)':<20} {'Est. Time (par)':<20}")
    print("-" * 60)
    
    for n in n_perms:
        for jobs in n_jobs_options:
            seq_time = n * single_train_time
            if jobs == 1:
                par_time = seq_time
            elif jobs == -1:
                import multiprocessing
                par_time = seq_time / multiprocessing.cpu_count()
            else:
                par_time = seq_time / jobs
            
            print(f"{n:<10} {jobs:<10} {seq_time:>6.1f}s {' '*13} {par_time:>6.1f}s")
    
    print("\n💡 Recommendations:")
    print("  - Start with n_permutations=50-100")
    print("  - Always use n_jobs=-1 for parallelism")
    print("  - Use processes backend for CPU-bound training")
    print("  - Consider adaptive testing for large experiments")


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("RETRAIN-NULL PERMUTATION TESTING EXAMPLES")
    print("=" * 60)
    
    try:
        example_basic_retrain_null()
        example_stratified_retrain_null()
        example_probability_metric()
        example_comparison_with_standard()
        example_cost_analysis()
        
        print("\n" + "=" * 60)
        print("All examples completed!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
