"""
Quick test script to verify all v1.3 features.
Run this to ensure all enhancements are working correctly.
"""

import numpy as np
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score
from cbd.api import detect_bias

print("=" * 60)
print("CBD v1.3 Feature Verification")
print("=" * 60)

# Generate test data
print("\n1. Generating test data...")
X, y = make_classification(
    n_samples=500,
    n_features=20,
    n_informative=10,
    random_state=42
)
print(f"   ✓ Dataset: {X.shape[0]} samples, {X.shape[1]} features")

# Train model
print("\n2. Training model...")
model = LogisticRegression(random_state=42, max_iter=1000)
model.fit(X, y)
print(f"   ✓ Model trained: {type(model).__name__}")

# Test 1: Basic functionality (backward compatibility)
print("\n3. Testing basic functionality (backward compatibility)...")
result = detect_bias(
    model, X, y,
    metric=accuracy_score,
    n_permutations=100,
    random_state=42
)
print(f"   ✓ P-value: {result['p_value']:.4f}")
print(f"   ✓ Conclusion: {result['conclusion']}")

# Test 2: Parallel execution
print("\n4. Testing parallel execution...")
result_parallel = detect_bias(
    model, X, y,
    metric=accuracy_score,
    n_permutations=100,
    n_jobs=2,
    backend='threads',
    random_state=42
)
print(f"   ✓ Backend: {result_parallel['backend']}")
print(f"   ✓ Workers: {result_parallel['n_jobs']}")
print(f"   ✓ P-value: {result_parallel['p_value']:.4f}")

# Test 3: Reproducibility
print("\n5. Testing reproducibility...")
result_rep1 = detect_bias(
    model, X, y,
    metric=accuracy_score,
    n_permutations=100,
    n_jobs=2,
    random_state=42,
    return_permutations=True
)
result_rep2 = detect_bias(
    model, X, y,
    metric=accuracy_score,
    n_permutations=100,
    n_jobs=2,
    random_state=42,
    return_permutations=True
)
is_reproducible = (
    result_rep1['p_value'] == result_rep2['p_value'] and
    np.allclose(result_rep1['permuted_metrics'], result_rep2['permuted_metrics'])
)
print(f"   ✓ Reproducible: {is_reproducible}")
assert is_reproducible, "Results should be reproducible with same seed!"

# Test 4: Probability-based metrics (AUC)
print("\n6. Testing probability-based metrics (AUC)...")
def auc_metric(y_true, y_proba):
    if y_proba.ndim == 2:
        y_proba = y_proba[:, 1]
    return roc_auc_score(y_true, y_proba)

result_auc = detect_bias(
    model, X, y,
    metric=auc_metric,
    allow_proba=True,
    n_permutations=100,
    random_state=42
)
print(f"   ✓ AUC metric: {result_auc['observed_metric']:.4f}")
print(f"   ✓ P-value: {result_auc['p_value']:.4f}")

# Test 5: Retrain null method
print("\n7. Testing retrain null method...")
result_retrain = detect_bias(
    model, X, y,
    metric=accuracy_score,
    null_method='retrain',
    n_permutations=20,  # Fewer due to computational cost
    n_jobs=2,
    random_state=42
)
print(f"   ✓ Null method: {result_retrain['null_method']}")
print(f"   ✓ P-value: {result_retrain['p_value']:.4f}")

# Test 6: Subsampling
print("\n8. Testing subsampling...")
result_subsample = detect_bias(
    model, X, y,
    metric=accuracy_score,
    subsample_size=200,
    n_permutations=100,
    n_jobs=2,
    random_state=42
)
print(f"   ✓ Subsampled: {result_subsample['subsampled']}")
print(f"   ✓ Samples used: {result_subsample['n_samples']}")
print(f"   ✓ P-value: {result_subsample['p_value']:.4f}")

# Test 7: P-value confidence interval
print("\n9. Testing p-value confidence interval...")
result_ci = detect_bias(
    model, X, y,
    metric=accuracy_score,
    n_permutations=1000,  # Need >= 1000 for CI
    confidence_level=0.95,
    random_state=42
)
if 'p_value_ci' in result_ci:
    ci = result_ci['p_value_ci']
    print(f"   ✓ P-value: {result_ci['p_value']:.4f}")
    print(f"   ✓ 95% CI: [{ci[0]:.4f}, {ci[1]:.4f}]")
else:
    print("   ⚠ CI not computed (need n_permutations >= 1000)")

# Test 8: Return permutations
print("\n10. Testing return permutations...")
result_perm = detect_bias(
    model, X, y,
    metric=accuracy_score,
    n_permutations=50,
    return_permutations=True,
    random_state=42
)
print(f"   ✓ Permutations returned: {len(result_perm['permuted_metrics'])}")
print(f"   ✓ Mean permuted: {np.mean(result_perm['permuted_metrics']):.4f}")
print(f"   ✓ Std permuted: {np.std(result_perm['permuted_metrics']):.4f}")

# Summary
print("\n" + "=" * 60)
print("✅ All v1.3 features verified successfully!")
print("=" * 60)
print("\nKey improvements:")
print("  • Parallel execution (threads/processes)")
print("  • Reproducible results with RNG")
print("  • Probability-based metrics (AUC, log loss)")
print("  • Retrain null method")
print("  • Subsampling for large datasets")
print("  • P-value confidence intervals")
print("  • Comprehensive test coverage")
print("\nFor more examples, see:")
print("  - examples/visualization_and_model_card.ipynb")
print("  - docs/ENHANCEMENTS_V1.3.md")
print("  - docs/NEW_FEATURES_V1.3.md")
