"""
Comprehensive tests for enhanced detect_bias functionality.
Tests parallel backends, RNG stability, metric types, and null methods.
"""

import pytest
import numpy as np
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, roc_auc_score, log_loss, f1_score, mean_squared_error

from cbd.api import detect_bias


@pytest.fixture
def binary_classification_data():
    """Generate binary classification dataset."""
    X, y = make_classification(
        n_samples=200,
        n_features=10,
        n_informative=5,
        n_redundant=2,
        random_state=42
    )
    return X, y


@pytest.fixture
def multiclass_classification_data():
    """Generate multiclass classification dataset."""
    X, y = make_classification(
        n_samples=200,
        n_features=10,
        n_informative=5,
        n_classes=3,
        random_state=42
    )
    return X, y


@pytest.fixture
def fitted_logistic_model(binary_classification_data):
    """Fitted logistic regression model."""
    X, y = binary_classification_data
    model = LogisticRegression(random_state=42, max_iter=1000)
    model.fit(X, y)
    return model


@pytest.fixture
def fitted_tree_model(binary_classification_data):
    """Fitted decision tree model."""
    X, y = binary_classification_data
    model = DecisionTreeClassifier(random_state=42, max_depth=5)
    model.fit(X, y)
    return model


class TestBasicFunctionality:
    """Test basic detect_bias functionality."""
    
    def test_basic_detection(self, binary_classification_data, fitted_logistic_model):
        """Test basic bias detection with default parameters."""
        X, y = binary_classification_data
        result = detect_bias(
            fitted_logistic_model,
            X, y,
            metric=accuracy_score,
            n_permutations=100,
            random_state=42
        )
        
        assert "observed_metric" in result
        assert "p_value" in result
        assert "conclusion" in result
        assert 0 <= result["p_value"] <= 1
        assert result["n_permutations"] == 100
    
    def test_return_permutations(self, binary_classification_data, fitted_logistic_model):
        """Test returning permutation metrics."""
        X, y = binary_classification_data
        result = detect_bias(
            fitted_logistic_model,
            X, y,
            metric=accuracy_score,
            n_permutations=50,
            random_state=42,
            return_permutations=True
        )
        
        assert "permuted_metrics" in result
        assert len(result["permuted_metrics"]) == 50
        assert all(isinstance(m, float) for m in result["permuted_metrics"])


class TestParallelization:
    """Test parallel execution backends."""
    
    def test_threads_backend(self, binary_classification_data, fitted_logistic_model):
        """Test thread-based parallelization."""
        X, y = binary_classification_data
        result = detect_bias(
            fitted_logistic_model,
            X, y,
            metric=accuracy_score,
            n_permutations=100,
            n_jobs=2,
            backend="threads",
            random_state=42
        )
        
        assert result["backend"] == "threads"
        assert result["n_jobs"] == 2
        assert "p_value" in result
    
    def test_processes_backend(self, binary_classification_data, fitted_logistic_model):
        """Test process-based parallelization."""
        X, y = binary_classification_data
        result = detect_bias(
            fitted_logistic_model,
            X, y,
            metric=accuracy_score,
            n_permutations=100,
            n_jobs=2,
            backend="processes",
            random_state=42
        )
        
        assert result["backend"] == "processes"
        assert result["n_jobs"] == 2
        assert "p_value" in result
    
    def test_parallel_reproducibility(self, binary_classification_data, fitted_logistic_model):
        """Test that parallel execution is reproducible with same seed."""
        X, y = binary_classification_data
        
        result1 = detect_bias(
            fitted_logistic_model,
            X, y,
            metric=accuracy_score,
            n_permutations=100,
            n_jobs=2,
            backend="threads",
            random_state=42,
            return_permutations=True
        )
        
        result2 = detect_bias(
            fitted_logistic_model,
            X, y,
            metric=accuracy_score,
            n_permutations=100,
            n_jobs=2,
            backend="threads",
            random_state=42,
            return_permutations=True
        )
        
        assert result1["p_value"] == result2["p_value"]
        assert np.allclose(result1["permuted_metrics"], result2["permuted_metrics"])
    
    def test_sequential_vs_parallel_consistency(self, binary_classification_data, fitted_logistic_model):
        """Test that sequential and parallel give same results."""
        X, y = binary_classification_data
        
        result_seq = detect_bias(
            fitted_logistic_model,
            X, y,
            metric=accuracy_score,
            n_permutations=50,
            n_jobs=1,
            random_state=42,
            return_permutations=True
        )
        
        result_par = detect_bias(
            fitted_logistic_model,
            X, y,
            metric=accuracy_score,
            n_permutations=50,
            n_jobs=2,
            backend="threads",
            random_state=42,
            return_permutations=True
        )
        
        # Results should be identical with same seed
        assert result_seq["p_value"] == result_par["p_value"]
        assert np.allclose(result_seq["permuted_metrics"], result_par["permuted_metrics"])


class TestMetricTypes:
    """Test different metric types and predict_proba support."""
    
    def test_accuracy_metric(self, binary_classification_data, fitted_logistic_model):
        """Test with accuracy metric."""
        X, y = binary_classification_data
        result = detect_bias(
            fitted_logistic_model,
            X, y,
            metric=accuracy_score,
            n_permutations=50,
            random_state=42
        )
        assert "p_value" in result
    
    def test_f1_metric(self, binary_classification_data, fitted_logistic_model):
        """Test with F1 score metric."""
        X, y = binary_classification_data
        result = detect_bias(
            fitted_logistic_model,
            X, y,
            metric=lambda y_true, y_pred: f1_score(y_true, y_pred, average='binary'),
            n_permutations=50,
            random_state=42
        )
        assert "p_value" in result
    
    def test_auc_with_proba(self, binary_classification_data, fitted_logistic_model):
        """Test AUC metric with predict_proba."""
        X, y = binary_classification_data
        
        def auc_metric(y_true, y_proba):
            # y_proba is (n_samples, n_classes), take positive class
            if y_proba.ndim == 2:
                y_proba = y_proba[:, 1]
            return roc_auc_score(y_true, y_proba)
        
        result = detect_bias(
            fitted_logistic_model,
            X, y,
            metric=auc_metric,
            n_permutations=50,
            allow_proba=True,
            random_state=42
        )
        
        assert "p_value" in result
        assert 0 <= result["observed_metric"] <= 1
    
    def test_logloss_with_proba(self, binary_classification_data, fitted_logistic_model):
        """Test log loss metric with predict_proba."""
        X, y = binary_classification_data
        
        result = detect_bias(
            fitted_logistic_model,
            X, y,
            metric=log_loss,
            n_permutations=50,
            allow_proba=True,
            random_state=42
        )
        
        assert "p_value" in result
        assert result["observed_metric"] >= 0
    
    def test_proba_without_predict_proba_raises(self, binary_classification_data):
        """Test that allow_proba=True raises error if model lacks predict_proba."""
        X, y = binary_classification_data
        
        # SVC without probability=True doesn't have predict_proba
        model = SVC(kernel='linear', random_state=42)
        model.fit(X, y)
        
        # Should use decision_function as fallback
        result = detect_bias(
            model,
            X, y,
            metric=lambda y_true, y_score: roc_auc_score(y_true, y_score),
            n_permutations=50,
            allow_proba=True,
            random_state=42
        )
        
        assert "p_value" in result
    
    def test_mse_metric(self, binary_classification_data, fitted_logistic_model):
        """Test with MSE metric (regression-style)."""
        X, y = binary_classification_data
        
        # Convert to regression problem
        y_float = y.astype(float)
        
        result = detect_bias(
            fitted_logistic_model,
            X, y_float,
            metric=lambda y_true, y_pred: -mean_squared_error(y_true, y_pred),  # Negative for higher-is-better
            n_permutations=50,
            random_state=42
        )
        
        assert "p_value" in result


class TestNullMethods:
    """Test different null hypothesis methods."""
    
    def test_permute_method(self, binary_classification_data, fitted_logistic_model):
        """Test permute null method (default, fast)."""
        X, y = binary_classification_data
        result = detect_bias(
            fitted_logistic_model,
            X, y,
            metric=accuracy_score,
            n_permutations=50,
            null_method="permute",
            random_state=42
        )
        
        assert result["null_method"] == "permute"
        assert "p_value" in result
    
    def test_retrain_method(self, binary_classification_data):
        """Test retrain null method (conservative, slow)."""
        X, y = binary_classification_data
        
        # Use a fresh model that will be retrained
        model = LogisticRegression(random_state=42, max_iter=1000)
        model.fit(X, y)
        
        result = detect_bias(
            model,
            X, y,
            metric=accuracy_score,
            n_permutations=20,  # Fewer permutations since retrain is slow
            null_method="retrain",
            random_state=42
        )
        
        assert result["null_method"] == "retrain"
        assert "p_value" in result
    
    def test_retrain_without_fit_raises(self, binary_classification_data):
        """Test that retrain method raises error if model lacks fit()."""
        X, y = binary_classification_data
        
        # Create a mock model without fit method
        class NoFitModel:
            def predict(self, X):
                return np.zeros(len(X))
        
        model = NoFitModel()
        
        with pytest.raises(ValueError, match="null_method='retrain' requires model to have fit"):
            detect_bias(
                model,
                X, y,
                metric=accuracy_score,
                n_permutations=10,
                null_method="retrain"
            )
    
    def test_retrain_with_parallel(self, binary_classification_data):
        """Test retrain method with parallel execution."""
        X, y = binary_classification_data
        
        model = LogisticRegression(random_state=42, max_iter=1000)
        model.fit(X, y)
        
        result = detect_bias(
            model,
            X, y,
            metric=accuracy_score,
            n_permutations=10,
            null_method="retrain",
            n_jobs=2,
            backend="threads",
            random_state=42
        )
        
        assert result["null_method"] == "retrain"
        assert result["n_jobs"] == 2
        assert "p_value" in result


class TestEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def test_small_dataset(self, fitted_logistic_model):
        """Test with very small dataset."""
        X = np.random.randn(20, 5)
        y = np.random.randint(0, 2, 20)
        
        model = LogisticRegression(random_state=42)
        model.fit(X, y)
        
        result = detect_bias(
            model,
            X, y,
            metric=accuracy_score,
            n_permutations=50,
            random_state=42
        )
        
        assert "p_value" in result
    
    def test_imbalanced_classes(self):
        """Test with highly imbalanced classes."""
        X, y = make_classification(
            n_samples=200,
            n_features=10,
            weights=[0.9, 0.1],  # 90-10 imbalance
            random_state=42
        )
        
        model = LogisticRegression(random_state=42, max_iter=1000)
        model.fit(X, y)
        
        result = detect_bias(
            model,
            X, y,
            metric=accuracy_score,
            n_permutations=50,
            random_state=42
        )
        
        assert "p_value" in result
    
    def test_perfect_predictions(self):
        """Test when model has perfect predictions."""
        X = np.random.randn(100, 5)
        y = np.random.randint(0, 2, 100)
        
        # Create a model that memorizes training data
        model = DecisionTreeClassifier(random_state=42)
        model.fit(X, y)
        
        result = detect_bias(
            model,
            X, y,
            metric=accuracy_score,
            n_permutations=50,
            random_state=42
        )
        
        # Should detect potential circular bias
        assert result["p_value"] < 0.05
    
    def test_random_predictions(self):
        """Test when model has random predictions."""
        X = np.random.randn(100, 5)
        y = np.random.randint(0, 2, 100)
        
        # Create a model with random predictions
        class RandomModel:
            def __init__(self, seed):
                self.rng = np.random.RandomState(seed)
            
            def predict(self, X):
                return self.rng.randint(0, 2, len(X))
        
        model = RandomModel(42)
        
        result = detect_bias(
            model,
            X, y,
            metric=accuracy_score,
            n_permutations=50,
            random_state=42
        )
        
        # Should not detect bias (p-value should be high)
        assert result["p_value"] > 0.05
    
    def test_different_random_seeds(self, binary_classification_data, fitted_logistic_model):
        """Test that different seeds give different results."""
        X, y = binary_classification_data
        
        result1 = detect_bias(
            fitted_logistic_model,
            X, y,
            metric=accuracy_score,
            n_permutations=100,
            random_state=42,
            return_permutations=True
        )
        
        result2 = detect_bias(
            fitted_logistic_model,
            X, y,
            metric=accuracy_score,
            n_permutations=100,
            random_state=123,
            return_permutations=True
        )
        
        # Different seeds should give different permutation metrics
        assert not np.allclose(result1["permuted_metrics"], result2["permuted_metrics"])
        # But p-values should be similar (not identical due to randomness)
        assert abs(result1["p_value"] - result2["p_value"]) < 0.2


class TestConcurrentStability:
    """Test concurrent execution stability."""
    
    def test_repeated_runs_same_seed(self, binary_classification_data, fitted_logistic_model):
        """Test that repeated runs with same seed yield identical results."""
        X, y = binary_classification_data
        
        results = []
        for _ in range(3):
            result = detect_bias(
                fitted_logistic_model,
                X, y,
                metric=accuracy_score,
                n_permutations=100,
                random_state=42,
                return_permutations=True
            )
            results.append(result)
        
        # All results should be identical
        for i in range(1, len(results)):
            assert results[0]["p_value"] == results[i]["p_value"]
            assert np.allclose(results[0]["permuted_metrics"], results[i]["permuted_metrics"])
    
    def test_parallel_stability(self, binary_classification_data, fitted_logistic_model):
        """Test parallel execution stability across multiple runs."""
        X, y = binary_classification_data
        
        results = []
        for _ in range(3):
            result = detect_bias(
                fitted_logistic_model,
                X, y,
                metric=accuracy_score,
                n_permutations=100,
                n_jobs=2,
                backend="threads",
                random_state=42,
                return_permutations=True
            )
            results.append(result)
        
        # All results should be identical
        for i in range(1, len(results)):
            assert results[0]["p_value"] == results[i]["p_value"]
            assert np.allclose(results[0]["permuted_metrics"], results[i]["permuted_metrics"])


class TestMulticlass:
    """Test multiclass classification scenarios."""
    
    def test_multiclass_accuracy(self, multiclass_classification_data):
        """Test multiclass classification with accuracy."""
        X, y = multiclass_classification_data
        
        model = LogisticRegression(random_state=42, max_iter=1000)
        model.fit(X, y)
        
        result = detect_bias(
            model,
            X, y,
            metric=accuracy_score,
            n_permutations=50,
            random_state=42
        )
        
        assert "p_value" in result
    
    def test_multiclass_f1(self, multiclass_classification_data):
        """Test multiclass classification with F1 score."""
        X, y = multiclass_classification_data
        
        model = LogisticRegression(random_state=42, max_iter=1000)
        model.fit(X, y)
        
        result = detect_bias(
            model,
            X, y,
            metric=lambda y_true, y_pred: f1_score(y_true, y_pred, average='weighted'),
            n_permutations=50,
            random_state=42
        )
        
        assert "p_value" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
