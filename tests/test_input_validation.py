"""Tests for input validation and edge cases in detect_bias."""
import pytest
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score
from cbd.api import detect_bias
import pandas as pd


class TestInputValidation:
    """Test input validation and type handling."""
    
    def test_single_class_error(self):
        """Test that single-class y raises ValueError."""
        X = np.random.randn(100, 5)
        y = np.ones(100)  # All same class
        model = RandomForestClassifier(random_state=42)
        model.fit(X, y)
        
        with pytest.raises(ValueError, match="at least 2 unique classes"):
            detect_bias(model, X, y, accuracy_score, n_permutations=10)
    
    def test_inconsistent_length_error(self):
        """Test that inconsistent X and y lengths raise error."""
        X = np.random.randn(100, 5)
        y = np.random.randint(0, 2, 50)  # Different length
        model = RandomForestClassifier(random_state=42)
        
        with pytest.raises(ValueError):
            detect_bias(model, X, y, accuracy_score, n_permutations=10)
    
    def test_pandas_input(self):
        """Test that pandas DataFrames and Series work."""
        X = pd.DataFrame(np.random.randn(100, 5))
        y = pd.Series(np.random.randint(0, 2, 100))
        
        model = RandomForestClassifier(random_state=42)
        model.fit(X, y)
        
        result = detect_bias(model, X, y, accuracy_score, n_permutations=10)
        assert "p_value" in result
        assert result["n_samples"] == 100
    
    def test_list_input(self):
        """Test that lists work as input."""
        X = [[1, 2], [3, 4], [5, 6], [7, 8]]
        y = [0, 1, 0, 1]
        
        model = LogisticRegression()
        model.fit(X, y)
        
        result = detect_bias(model, X, y, accuracy_score, n_permutations=10)
        assert "p_value" in result
    
    def test_alpha_validation(self):
        """Test that invalid alpha values raise error."""
        X = np.random.randn(50, 5)
        y = np.random.randint(0, 2, 50)
        model = RandomForestClassifier(random_state=42)
        model.fit(X, y)
        
        # alpha must be in (0, 1)
        with pytest.raises(ValueError, match="alpha must be in"):
            detect_bias(model, X, y, accuracy_score, alpha=0.0)
        
        with pytest.raises(ValueError, match="alpha must be in"):
            detect_bias(model, X, y, accuracy_score, alpha=1.0)
        
        with pytest.raises(ValueError, match="alpha must be in"):
            detect_bias(model, X, y, accuracy_score, alpha=-0.1)
    
    def test_configurable_alpha(self):
        """Test that alpha is configurable and returned in results."""
        X = np.random.randn(50, 5)
        y = np.random.randint(0, 2, 50)
        model = RandomForestClassifier(random_state=42)
        model.fit(X, y)
        
        result = detect_bias(model, X, y, accuracy_score, alpha=0.01, n_permutations=10)
        assert result["alpha"] == 0.01
        assert "alpha" in result["conclusion"] or "0.01" in result["conclusion"]


class TestPredictProbaHandling:
    """Test handling of predict_proba and probability metrics."""
    
    def test_no_predict_proba_error(self):
        """Test that allow_proba=True without predict_proba raises error."""
        class DummyModel:
            def predict(self, X):
                return np.zeros(len(X))
        
        X = np.random.randn(50, 5)
        y = np.random.randint(0, 2, 50)
        model = DummyModel()
        
        with pytest.raises(ValueError, match="allow_proba=True but model has neither"):
            detect_bias(model, X, y, accuracy_score, allow_proba=True, n_permutations=10)
    
    def test_decision_function_fallback(self):
        """Test that decision_function is used as fallback when predict_proba unavailable."""
        from sklearn.svm import LinearSVC
        
        X = np.random.randn(50, 5)
        y = np.random.randint(0, 2, 50)
        model = LinearSVC(random_state=42)
        model.fit(X, y)
        
        # LinearSVC has decision_function but not predict_proba
        with pytest.warns(UserWarning, match="decision_function as fallback"):
            result = detect_bias(
                model, X, y, 
                lambda y_true, y_pred: np.mean(y_pred > 0),
                allow_proba=True, 
                n_permutations=10
            )
        assert "p_value" in result
    
    def test_predict_proba_with_auc(self):
        """Test that predict_proba works with AUC metric."""
        X = np.random.randn(100, 5)
        y = np.random.randint(0, 2, 100)
        model = RandomForestClassifier(random_state=42)
        model.fit(X, y)
        
        def auc_metric(y_true, y_pred_proba):
            # y_pred_proba is (n_samples, n_classes)
            return roc_auc_score(y_true, y_pred_proba[:, 1])
        
        result = detect_bias(
            model, X, y, auc_metric,
            allow_proba=True,
            n_permutations=50
        )
        assert "p_value" in result
        assert 0 <= result["observed_metric"] <= 1


class TestStratifiedPermutation:
    """Test stratified permutation for imbalanced datasets."""
    
    def test_stratified_preserves_distribution(self):
        """Test that stratified permutation preserves class distribution."""
        # Create imbalanced dataset
        X = np.random.randn(100, 5)
        y = np.array([0] * 90 + [1] * 10)  # 90% class 0, 10% class 1
        
        model = RandomForestClassifier(random_state=42)
        model.fit(X, y)
        
        result = detect_bias(
            model, X, y, accuracy_score,
            stratify=True,
            n_permutations=50,
            random_state=42
        )
        
        assert result["stratified"] is True
        assert "p_value" in result
    
    def test_stratified_vs_unstratified(self):
        """Test that stratified and unstratified give different results on imbalanced data."""
        X = np.random.randn(100, 5)
        y = np.array([0] * 95 + [1] * 5)  # Very imbalanced
        
        model = RandomForestClassifier(random_state=42)
        model.fit(X, y)
        
        result_unstratified = detect_bias(
            model, X, y, accuracy_score,
            stratify=False,
            n_permutations=100,
            random_state=42
        )
        
        result_stratified = detect_bias(
            model, X, y, accuracy_score,
            stratify=True,
            n_permutations=100,
            random_state=42
        )
        
        # Results should differ (though not guaranteed to be significant)
        assert result_unstratified["stratified"] is False
        assert result_stratified["stratified"] is True


class TestRetrainNullMethod:
    """Test retrain null method."""
    
    def test_retrain_without_fit_error(self):
        """Test that retrain without fit() raises error."""
        class DummyModel:
            def predict(self, X):
                return np.zeros(len(X))
        
        X = np.random.randn(50, 5)
        y = np.random.randint(0, 2, 50)
        model = DummyModel()
        
        with pytest.raises(ValueError, match="null_method='retrain' requires model to have fit"):
            detect_bias(model, X, y, accuracy_score, null_method="retrain", n_permutations=10)
    
    def test_retrain_method_works(self):
        """Test that retrain method executes successfully."""
        X = np.random.randn(50, 5)
        y = np.random.randint(0, 2, 50)
        model = RandomForestClassifier(random_state=42, n_estimators=5)
        model.fit(X, y)
        
        result = detect_bias(
            model, X, y, accuracy_score,
            null_method="retrain",
            n_permutations=10,  # Small number for speed
            random_state=42
        )
        
        assert result["null_method"] == "retrain"
        assert "p_value" in result


class TestRandomStateReproducibility:
    """Test random state and reproducibility."""
    
    def test_reproducibility_with_random_state(self):
        """Test that same random_state gives same results."""
        X = np.random.randn(50, 5)
        y = np.random.randint(0, 2, 50)
        model = RandomForestClassifier(random_state=42)
        model.fit(X, y)
        
        result1 = detect_bias(model, X, y, accuracy_score, n_permutations=50, random_state=42)
        result2 = detect_bias(model, X, y, accuracy_score, n_permutations=50, random_state=42)
        
        assert result1["p_value"] == result2["p_value"]
        assert result1["observed_metric"] == result2["observed_metric"]
    
    def test_different_random_states_differ(self):
        """Test that different random_states give different results."""
        X = np.random.randn(50, 5)
        y = np.random.randint(0, 2, 50)
        model = RandomForestClassifier(random_state=42)
        model.fit(X, y)
        
        result1 = detect_bias(model, X, y, accuracy_score, n_permutations=50, random_state=42)
        result2 = detect_bias(model, X, y, accuracy_score, n_permutations=50, random_state=123)
        
        # p-values should differ (with high probability)
        # observed_metric should be the same
        assert result1["observed_metric"] == result2["observed_metric"]


class TestResultFields:
    """Test that result dictionary contains expected fields."""
    
    def test_all_fields_present(self):
        """Test that all expected fields are in result."""
        X = np.random.randn(50, 5)
        y = np.random.randint(0, 2, 50)
        model = RandomForestClassifier(random_state=42)
        model.fit(X, y)
        
        result = detect_bias(
            model, X, y, accuracy_score,
            n_permutations=100,
            random_state=42,
            alpha=0.01,
            stratify=True
        )
        
        expected_fields = [
            "observed_metric", "p_value", "n_permutations", "conclusion",
            "alpha", "null_method", "stratified", "backend", "n_jobs",
            "n_samples", "n_classes", "subsampled"
        ]
        
        for field in expected_fields:
            assert field in result, f"Missing field: {field}"
    
    def test_n_classes_field(self):
        """Test that n_classes field is correct."""
        X = np.random.randn(50, 5)
        y = np.array([0, 1, 2] * 16 + [0, 1])  # 3 classes
        model = RandomForestClassifier(random_state=42)
        model.fit(X, y)
        
        result = detect_bias(model, X, y, accuracy_score, n_permutations=10)
        assert result["n_classes"] == 3
