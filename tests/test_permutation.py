"""
Unit tests for enhanced permutation testing module.
"""

import pytest
import numpy as np
from circular_bias_detector.core.permutation import (
    permutation_test,
    retrain_null_test,
    adaptive_permutation_test,
    _permutation_worker
)
from circular_bias_detector.core.metrics import compute_psi, compute_ccs, compute_rho_pc


# Helper wrapper functions for metrics that only need performance matrix
def psi_wrapper(perf, const=None):
    """Wrapper for compute_psi that ignores constraint matrix."""
    return compute_psi(perf)


def ccs_wrapper(perf, const):
    """Wrapper for compute_ccs that uses constraint matrix."""
    return compute_ccs(const)


class TestPermutationTest:
    """Tests for basic permutation testing."""
    
    def test_permutation_test_basic(self):
        """Test basic permutation test execution."""
        np.random.seed(42)
        perf = np.random.rand(10, 3)
        const = np.random.rand(10, 2)
        
        results = permutation_test(
            perf, const, psi_wrapper,
            n_permutations=100,
            random_seed=42,
            n_jobs=1
        )
        
        assert 'observed' in results
        assert 'permuted_values' in results
        assert 'p_value' in results
        assert 0 <= results['p_value'] <= 1
        assert len(results['permuted_values']) <= 100
    
    def test_permutation_test_reproducibility(self):
        """Test that results are reproducible with same seed."""
        np.random.seed(42)
        perf = np.random.rand(10, 3)
        const = np.random.rand(10, 2)
        
        results1 = permutation_test(
            perf, const, psi_wrapper,
            n_permutations=50,
            random_seed=123,
            n_jobs=1
        )
        
        results2 = permutation_test(
            perf, const, psi_wrapper,
            n_permutations=50,
            random_seed=123,
            n_jobs=1
        )
        
        assert results1['observed'] == results2['observed']
        assert results1['p_value'] == results2['p_value']
        np.testing.assert_array_equal(
            results1['permuted_values'],
            results2['permuted_values']
        )
    
    def test_permutation_test_parallel_threads(self):
        """Test parallel execution with threads."""
        np.random.seed(42)
        perf = np.random.rand(10, 3)
        const = np.random.rand(10, 2)
        
        results = permutation_test(
            perf, const, psi_wrapper,
            n_permutations=50,
            random_seed=42,
            n_jobs=2,
            backend='threads'
        )
        
        assert results['n_permutations'] <= 50
        assert 0 <= results['p_value'] <= 1
    
    def test_permutation_test_parallel_processes(self):
        """Test parallel execution with processes."""
        np.random.seed(42)
        perf = np.random.rand(10, 3)
        const = np.random.rand(10, 2)
        
        results = permutation_test(
            perf, const, psi_wrapper,
            n_permutations=50,
            random_seed=42,
            n_jobs=2,
            backend='processes'
        )
        
        assert results['n_permutations'] <= 50
        assert 0 <= results['p_value'] <= 1
    
    def test_permutation_test_different_metrics(self):
        """Test with different metric functions."""
        np.random.seed(42)
        perf = np.random.rand(10, 3)
        const = np.random.rand(10, 2)
        
        # Test PSI
        results_psi = permutation_test(
            perf, const, psi_wrapper,
            n_permutations=50, random_seed=42
        )
        assert 'observed' in results_psi
        
        # Test CCS
        results_ccs = permutation_test(
            perf, const, lambda p, c: compute_ccs(c),
            n_permutations=50, random_seed=42
        )
        assert 'observed' in results_ccs
        
        # Test rho_PC
        results_rho = permutation_test(
            perf, const, compute_rho_pc,
            n_permutations=50, random_seed=42
        )
        assert 'observed' in results_rho
    
    def test_permutation_worker(self):
        """Test individual permutation worker."""
        np.random.seed(42)
        perf = np.random.rand(10, 3)
        const = np.random.rand(10, 2)
        
        result = _permutation_worker(
            seed=42,
            performance_matrix=perf,
            constraint_matrix=const,
            metric_func=psi_wrapper
        )
        
        assert isinstance(result, (float, np.floating))
        assert not np.isnan(result)
    
    def test_confidence_intervals(self):
        """Test confidence interval computation."""
        np.random.seed(42)
        perf = np.random.rand(20, 3)
        const = np.random.rand(20, 2)
        
        results = permutation_test(
            perf, const, psi_wrapper,
            n_permutations=200,
            random_seed=42
        )
        
        assert 'ci_lower' in results
        assert 'ci_upper' in results
        assert results['ci_lower'] < results['ci_upper']


class TestRetrainNullTest:
    """Tests for retrain-null permutation testing."""
    
    def test_retrain_null_basic(self):
        """Test basic retrain-null test."""
        pytest.importorskip('sklearn')
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.metrics import accuracy_score
        from sklearn.datasets import make_classification
        
        X, y = make_classification(n_samples=100, n_features=10, random_state=42)
        split = 70
        X_train, X_test = X[:split], X[split:]
        y_train, y_test = y[:split], y[split:]
        
        model_factory = lambda: RandomForestClassifier(
            n_estimators=10, max_depth=3, random_state=42
        )
        
        results = retrain_null_test(
            X_train, y_train, X_test, y_test,
            model_factory, accuracy_score,
            n_permutations=10,  # Small for speed
            random_seed=42,
            n_jobs=1
        )
        
        assert 'observed' in results
        assert 'permuted_values' in results
        assert 'p_value' in results
        assert 0 <= results['p_value'] <= 1
    
    def test_retrain_null_stratified(self):
        """Test retrain-null with stratified permutation."""
        pytest.importorskip('sklearn')
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.metrics import accuracy_score
        from sklearn.datasets import make_classification
        
        X, y = make_classification(
            n_samples=100, n_features=10, n_classes=3,
            n_informative=8, random_state=42
        )
        split = 70
        X_train, X_test = X[:split], X[split:]
        y_train, y_test = y[:split], y[split:]
        
        # Create stratify groups (e.g., by class)
        stratify_groups = y_train
        
        model_factory = lambda: RandomForestClassifier(
            n_estimators=10, max_depth=3, random_state=42
        )
        
        results = retrain_null_test(
            X_train, y_train, X_test, y_test,
            model_factory, accuracy_score,
            n_permutations=10,
            random_seed=42,
            stratify_groups=stratify_groups,
            n_jobs=1
        )
        
        assert 'observed' in results
        assert results['n_permutations'] <= 10
    
    def test_retrain_null_parallel(self):
        """Test retrain-null with parallel processing."""
        pytest.importorskip('sklearn')
        from sklearn.tree import DecisionTreeClassifier
        from sklearn.metrics import accuracy_score
        from sklearn.datasets import make_classification
        
        X, y = make_classification(n_samples=80, n_features=5, random_state=42)
        split = 60
        X_train, X_test = X[:split], X[split:]
        y_train, y_test = y[:split], y[split:]
        
        model_factory = lambda: DecisionTreeClassifier(max_depth=3, random_state=42)
        
        results = retrain_null_test(
            X_train, y_train, X_test, y_test,
            model_factory, accuracy_score,
            n_permutations=10,
            random_seed=42,
            n_jobs=2,
            backend='processes'
        )
        
        assert results['n_permutations'] <= 10


class TestAdaptivePermutationTest:
    """Tests for adaptive permutation testing."""
    
    def test_adaptive_basic(self):
        """Test basic adaptive permutation test."""
        np.random.seed(42)
        perf = np.random.rand(15, 3)
        const = np.random.rand(15, 2)
        
        results = adaptive_permutation_test(
            perf, const, psi_wrapper,
            max_permutations=500,
            min_permutations=50,
            precision=0.02,
            random_seed=42,
            n_jobs=1
        )
        
        assert 'observed' in results
        assert 'converged' in results
        assert 'n_permutations' in results
        assert results['n_permutations'] >= 50  # At least min_permutations
    
    def test_adaptive_convergence(self):
        """Test that adaptive test can converge early."""
        np.random.seed(42)
        # Create data with clear null hypothesis
        perf = np.random.rand(20, 3)
        const = np.random.rand(20, 2)
        
        results = adaptive_permutation_test(
            perf, const, psi_wrapper,
            max_permutations=2000,
            min_permutations=100,
            precision=0.01,
            random_seed=42,
            n_jobs=1
        )
        
        # Should converge before max
        assert results['n_permutations'] <= results['max_permutations']
    
    def test_adaptive_parallel(self):
        """Test adaptive test with parallelism."""
        np.random.seed(42)
        perf = np.random.rand(15, 3)
        const = np.random.rand(15, 2)
        
        results = adaptive_permutation_test(
            perf, const, psi_wrapper,
            max_permutations=300,
            min_permutations=50,
            random_seed=42,
            n_jobs=2,
            backend='threads'
        )
        
        assert 'converged' in results
        assert results['n_permutations'] >= 50


class TestEdgeCases:
    """Tests for edge cases and error handling."""
    
    def test_small_sample_size(self):
        """Test with very small sample size."""
        perf = np.random.rand(3, 2)
        const = np.random.rand(3, 2)
        
        results = permutation_test(
            perf, const, psi_wrapper,
            n_permutations=10,
            random_seed=42
        )
        
        assert 'observed' in results
    
    def test_single_algorithm(self):
        """Test with single algorithm."""
        perf = np.random.rand(10, 1)
        const = np.random.rand(10, 2)
        
        results = permutation_test(
            perf, const, psi_wrapper,
            n_permutations=50,
            random_seed=42
        )
        
        assert 'observed' in results
    
    def test_imbalanced_data(self):
        """Test with imbalanced classes in retrain-null."""
        pytest.importorskip('sklearn')
        from sklearn.tree import DecisionTreeClassifier
        from sklearn.metrics import accuracy_score
        
        # Highly imbalanced
        X = np.random.rand(100, 5)
        y = np.array([0] * 90 + [1] * 10)
        
        split = 70
        X_train, X_test = X[:split], X[split:]
        y_train, y_test = y[:split], y[split:]
        
        model_factory = lambda: DecisionTreeClassifier(max_depth=3, random_state=42)
        
        results = retrain_null_test(
            X_train, y_train, X_test, y_test,
            model_factory, accuracy_score,
            n_permutations=10,
            random_seed=42
        )
        
        assert 'observed' in results
    
    def test_all_permutations_fail(self):
        """Test handling when all permutations fail."""
        # Track if we're computing observed value
        call_count = [0]
        
        def failing_metric(perf, const=None):
            call_count[0] += 1
            # Succeed for first call (observed), fail for rest (permutations)
            if call_count[0] == 1:
                return 0.5
            raise ValueError("Intentional failure")
        
        perf = np.random.rand(10, 3)
        const = np.random.rand(10, 2)
        
        with pytest.raises(ValueError, match="All permutations failed"):
            permutation_test(
                perf, const, failing_metric,
                n_permutations=10,
                random_seed=42
            )
    
    def test_nan_handling(self):
        """Test handling of NaN values in permutations."""
        def sometimes_nan_metric(perf, const):
            if np.random.rand() < 0.3:
                return np.nan
            return psi_wrapper(perf)
        
        perf = np.random.rand(10, 3)
        const = np.random.rand(10, 2)
        
        results = permutation_test(
            perf, const, sometimes_nan_metric,
            n_permutations=50,
            random_seed=42
        )
        
        # Should have some successful permutations
        assert results['n_permutations'] > 0
        assert results['n_failed'] >= 0


class TestReproducibility:
    """Tests for reproducibility across different scenarios."""
    
    def test_sequential_vs_parallel_threads(self):
        """Test that sequential and parallel (threads) give same results."""
        np.random.seed(42)
        perf = np.random.rand(10, 3)
        const = np.random.rand(10, 2)
        
        results_seq = permutation_test(
            perf, const, psi_wrapper,
            n_permutations=50,
            random_seed=123,
            n_jobs=1
        )
        
        results_par = permutation_test(
            perf, const, psi_wrapper,
            n_permutations=50,
            random_seed=123,
            n_jobs=2,
            backend='threads'
        )
        
        # Should be identical due to seed-based RNG
        assert results_seq['observed'] == results_par['observed']
        assert results_seq['p_value'] == results_par['p_value']
    
    def test_multiple_runs_same_seed(self):
        """Test multiple runs with same seed produce identical results."""
        perf = np.random.rand(10, 3)
        const = np.random.rand(10, 2)
        
        results = []
        for _ in range(3):
            r = permutation_test(
                perf, const, psi_wrapper,
                n_permutations=50,
                random_seed=999
            )
            results.append(r)
        
        # All should be identical
        for i in range(1, len(results)):
            assert results[0]['p_value'] == results[i]['p_value']
            np.testing.assert_array_equal(
                results[0]['permuted_values'],
                results[i]['permuted_values']
            )


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
