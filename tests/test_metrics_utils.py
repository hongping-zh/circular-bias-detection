"""
Unit tests for metrics utilities module.
"""

import pytest
import numpy as np
from circular_bias_detector.metrics_utils import (
    MetricWrapper,
    detect_metric_type,
    create_metric_wrapper,
    get_metric_by_name,
    validate_metric_compatibility,
    safe_metric_call,
    get_common_metrics
)


class TestMetricWrapper:
    """Tests for MetricWrapper class."""
    
    def test_wrapper_with_predictions(self):
        """Test wrapper with prediction-based metric."""
        sklearn = pytest.importorskip('sklearn')
        from sklearn.metrics import accuracy_score
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.datasets import make_classification
        
        X, y = make_classification(n_samples=100, n_features=10, random_state=42)
        model = RandomForestClassifier(n_estimators=10, random_state=42)
        model.fit(X, y)
        
        wrapper = MetricWrapper(accuracy_score, requires_proba=False)
        score = wrapper(y, model, X)
        
        assert 0 <= score <= 1
        assert isinstance(score, (float, np.floating))
    
    def test_wrapper_with_probabilities(self):
        """Test wrapper with probability-based metric."""
        sklearn = pytest.importorskip('sklearn')
        from sklearn.metrics import roc_auc_score
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.datasets import make_classification
        
        X, y = make_classification(n_samples=100, n_features=10, random_state=42)
        model = RandomForestClassifier(n_estimators=10, random_state=42)
        model.fit(X, y)
        
        wrapper = MetricWrapper(roc_auc_score, requires_proba=True)
        score = wrapper(y, model, X)
        
        assert 0 <= score <= 1
    
    def test_wrapper_fallback_to_decision_function(self):
        """Test fallback to decision_function when predict_proba unavailable."""
        sklearn = pytest.importorskip('sklearn')
        from sklearn.metrics import roc_auc_score
        from sklearn.svm import SVC
        from sklearn.datasets import make_classification
        
        X, y = make_classification(n_samples=100, n_features=10, random_state=42)
        model = SVC(kernel='linear', random_state=42)  # No predict_proba
        model.fit(X, y)
        
        wrapper = MetricWrapper(roc_auc_score, requires_proba=True)
        
        # Should use decision_function with warning
        with pytest.warns(UserWarning):
            score = wrapper(y, model, X)
        
        assert isinstance(score, (float, np.floating))
    
    def test_wrapper_error_no_proba_method(self):
        """Test error when model has no probability method."""
        sklearn = pytest.importorskip('sklearn')
        from sklearn.metrics import roc_auc_score
        
        # Mock model with only predict
        class MockModel:
            def predict(self, X):
                return np.zeros(len(X))
        
        model = MockModel()
        X = np.random.rand(10, 5)
        y = np.zeros(10)
        
        wrapper = MetricWrapper(roc_auc_score, requires_proba=True)
        
        with pytest.raises(ValueError, match="requires probabilities"):
            wrapper(y, model, X)


class TestMetricDetection:
    """Tests for metric type detection."""
    
    def test_detect_proba_metrics(self):
        """Test detection of probability-based metrics."""
        sklearn = pytest.importorskip('sklearn')
        from sklearn.metrics import roc_auc_score, log_loss, brier_score_loss
        
        assert detect_metric_type(roc_auc_score) == 'proba'
        assert detect_metric_type(log_loss) == 'proba'
        assert detect_metric_type(brier_score_loss) == 'proba'
    
    def test_detect_pred_metrics(self):
        """Test detection of prediction-based metrics."""
        sklearn = pytest.importorskip('sklearn')
        from sklearn.metrics import accuracy_score, f1_score, precision_score
        
        assert detect_metric_type(accuracy_score) == 'pred'
        assert detect_metric_type(f1_score) == 'pred'
        assert detect_metric_type(precision_score) == 'pred'
    
    def test_create_wrapper_auto_detect(self):
        """Test automatic detection in wrapper creation."""
        sklearn = pytest.importorskip('sklearn')
        from sklearn.metrics import roc_auc_score, accuracy_score
        
        auc_wrapper = create_metric_wrapper(roc_auc_score)
        assert auc_wrapper.requires_proba is True
        
        acc_wrapper = create_metric_wrapper(accuracy_score)
        assert acc_wrapper.requires_proba is False
    
    def test_create_wrapper_override(self):
        """Test manual override of detection."""
        sklearn = pytest.importorskip('sklearn')
        from sklearn.metrics import accuracy_score
        
        # Force accuracy to require probabilities (unusual but possible)
        wrapper = create_metric_wrapper(accuracy_score, requires_proba=True)
        assert wrapper.requires_proba is True


class TestMetricByName:
    """Tests for getting metrics by name."""
    
    def test_get_common_metrics(self):
        """Test getting common metrics by name."""
        sklearn = pytest.importorskip('sklearn')
        
        acc = get_metric_by_name('accuracy')
        assert callable(acc)
        
        auc = get_metric_by_name('auc')
        assert callable(auc)
        
        f1 = get_metric_by_name('f1')
        assert callable(f1)
    
    def test_get_metric_aliases(self):
        """Test metric name aliases."""
        sklearn = pytest.importorskip('sklearn')
        
        # Test aliases
        assert get_metric_by_name('acc') == get_metric_by_name('accuracy')
        assert get_metric_by_name('roc_auc') == get_metric_by_name('auc')
        assert get_metric_by_name('logloss') == get_metric_by_name('log_loss')
    
    def test_get_metric_invalid_name(self):
        """Test error on invalid metric name."""
        sklearn = pytest.importorskip('sklearn')
        
        with pytest.raises(ValueError, match="Unknown metric"):
            get_metric_by_name('invalid_metric_name')
    
    def test_create_wrapper_from_string(self):
        """Test creating wrapper from metric name string."""
        sklearn = pytest.importorskip('sklearn')
        
        wrapper = create_metric_wrapper('accuracy')
        assert isinstance(wrapper, MetricWrapper)
        assert wrapper.requires_proba is False
        
        wrapper = create_metric_wrapper('auc')
        assert wrapper.requires_proba is True


class TestCompatibilityValidation:
    """Tests for model-metric compatibility validation."""
    
    def test_compatible_model_metric(self):
        """Test compatible model and metric."""
        sklearn = pytest.importorskip('sklearn')
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.metrics import roc_auc_score
        from sklearn.datasets import make_classification
        
        X, y = make_classification(n_samples=50, n_features=5, random_state=42)
        model = RandomForestClassifier(n_estimators=10, random_state=42)
        model.fit(X, y)
        
        compatible, msg = validate_metric_compatibility(model, roc_auc_score)
        assert compatible is True
        assert "predict_proba" in msg.lower()
    
    def test_incompatible_model_metric(self):
        """Test incompatible model and metric."""
        sklearn = pytest.importorskip('sklearn')
        from sklearn.svm import SVC
        from sklearn.metrics import roc_auc_score
        from sklearn.datasets import make_classification
        
        X, y = make_classification(n_samples=50, n_features=5, random_state=42)
        model = SVC(kernel='linear', random_state=42)
        model.fit(X, y)
        
        # SVC without probability=True has decision_function
        compatible, msg = validate_metric_compatibility(model, roc_auc_score)
        # Should be compatible via decision_function fallback
        assert compatible is True
        assert "decision_function" in msg.lower()
    
    def test_validation_with_string_metric(self):
        """Test validation with metric name string."""
        sklearn = pytest.importorskip('sklearn')
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.datasets import make_classification
        
        X, y = make_classification(n_samples=50, n_features=5, random_state=42)
        model = RandomForestClassifier(n_estimators=10, random_state=42)
        model.fit(X, y)
        
        compatible, msg = validate_metric_compatibility(model, 'auc')
        assert compatible is True
    
    def test_validation_raise_error(self):
        """Test validation with raise_error=True."""
        sklearn = pytest.importorskip('sklearn')
        
        # Mock model with no predict
        class BadModel:
            pass
        
        model = BadModel()
        
        with pytest.raises(ValueError, match="no predict method"):
            validate_metric_compatibility(model, 'accuracy', raise_error=True)


class TestSafeMetricCall:
    """Tests for safe metric calling."""
    
    def test_safe_call_success(self):
        """Test successful metric call."""
        sklearn = pytest.importorskip('sklearn')
        from sklearn.metrics import accuracy_score
        
        y_true = np.array([0, 1, 1, 0, 1])
        y_pred = np.array([0, 1, 0, 0, 1])
        
        score = safe_metric_call(accuracy_score, y_true, y_pred)
        assert 0 <= score <= 1
    
    def test_safe_call_with_error(self):
        """Test safe call with error returns default."""
        sklearn = pytest.importorskip('sklearn')
        from sklearn.metrics import accuracy_score
        
        y_true = np.array([0, 1, 1])
        y_pred = np.array([0, 1])  # Wrong shape
        
        with pytest.warns(UserWarning):
            score = safe_metric_call(accuracy_score, y_true, y_pred, default_value=-1.0)
        
        assert score == -1.0
    
    def test_safe_call_with_string_metric(self):
        """Test safe call with metric name."""
        sklearn = pytest.importorskip('sklearn')
        
        y_true = np.array([0, 1, 1, 0, 1])
        y_pred = np.array([0, 1, 0, 0, 1])
        
        score = safe_metric_call('accuracy', y_true, y_pred)
        assert 0 <= score <= 1


class TestCommonMetrics:
    """Tests for common metrics dictionary."""
    
    def test_get_common_metrics_dict(self):
        """Test getting common metrics dictionary."""
        sklearn = pytest.importorskip('sklearn')
        
        metrics = get_common_metrics()
        
        assert isinstance(metrics, dict)
        assert 'accuracy' in metrics
        assert 'auc' in metrics
        assert 'f1' in metrics
        
        # Check they are MetricWrapper instances
        for name, wrapper in metrics.items():
            assert isinstance(wrapper, MetricWrapper)
    
    def test_common_metrics_proba_flags(self):
        """Test that common metrics have correct proba flags."""
        sklearn = pytest.importorskip('sklearn')
        
        metrics = get_common_metrics()
        
        # Prediction-based
        assert metrics['accuracy'].requires_proba is False
        assert metrics['f1'].requires_proba is False
        assert metrics['precision'].requires_proba is False
        
        # Probability-based
        assert metrics['auc'].requires_proba is True
        assert metrics['log_loss'].requires_proba is True


class TestEdgeCases:
    """Tests for edge cases and error handling."""
    
    def test_binary_vs_multiclass_proba(self):
        """Test handling of binary vs multiclass probabilities."""
        sklearn = pytest.importorskip('sklearn')
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.metrics import roc_auc_score
        from sklearn.datasets import make_classification
        
        # Binary classification
        X, y = make_classification(n_samples=100, n_features=10, n_classes=2, random_state=42)
        model = RandomForestClassifier(n_estimators=10, random_state=42)
        model.fit(X, y)
        
        wrapper = MetricWrapper(roc_auc_score, requires_proba=True)
        score = wrapper(y, model, X)
        
        assert 0 <= score <= 1
    
    def test_multiclass_prediction(self):
        """Test with multiclass classification."""
        sklearn = pytest.importorskip('sklearn')
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.metrics import accuracy_score
        from sklearn.datasets import make_classification
        
        X, y = make_classification(
            n_samples=100, n_features=10, n_classes=3,
            n_informative=8, random_state=42
        )
        model = RandomForestClassifier(n_estimators=10, random_state=42)
        model.fit(X, y)
        
        wrapper = MetricWrapper(accuracy_score, requires_proba=False)
        score = wrapper(y, model, X)
        
        assert 0 <= score <= 1
    
    def test_regression_metrics(self):
        """Test with regression metrics."""
        sklearn = pytest.importorskip('sklearn')
        from sklearn.ensemble import RandomForestRegressor
        from sklearn.metrics import mean_squared_error
        from sklearn.datasets import make_regression
        
        X, y = make_regression(n_samples=100, n_features=10, random_state=42)
        model = RandomForestRegressor(n_estimators=10, random_state=42)
        model.fit(X, y)
        
        wrapper = MetricWrapper(mean_squared_error, requires_proba=False)
        score = wrapper(y, model, X)
        
        assert score >= 0  # MSE is non-negative
    
    def test_empty_predictions(self):
        """Test handling of empty predictions."""
        sklearn = pytest.importorskip('sklearn')
        from sklearn.metrics import accuracy_score
        
        y_true = np.array([])
        y_pred = np.array([])
        
        # Should handle gracefully (may emit RuntimeWarning or UserWarning)
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")  # Ignore numpy warnings
            score = safe_metric_call(accuracy_score, y_true, y_pred, default_value=0.0)
        
        # Empty arrays may return NaN (which is expected behavior)
        assert np.isnan(score) or score == 0.0


class TestIntegration:
    """Integration tests combining multiple components."""
    
    def test_full_workflow(self):
        """Test complete workflow from metric name to evaluation."""
        sklearn = pytest.importorskip('sklearn')
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.datasets import make_classification
        
        # Create data and model
        X, y = make_classification(n_samples=100, n_features=10, random_state=42)
        model = RandomForestClassifier(n_estimators=10, random_state=42)
        model.fit(X, y)
        
        # Get metric by name
        metric_name = 'auc'
        wrapper = create_metric_wrapper(metric_name)
        
        # Validate compatibility
        compatible, msg = validate_metric_compatibility(model, wrapper)
        assert compatible
        
        # Compute metric
        score = wrapper(y, model, X)
        assert 0 <= score <= 1
    
    def test_multiple_metrics_evaluation(self):
        """Test evaluating multiple metrics on same model."""
        sklearn = pytest.importorskip('sklearn')
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.datasets import make_classification
        
        X, y = make_classification(n_samples=100, n_features=10, random_state=42)
        model = RandomForestClassifier(n_estimators=10, random_state=42)
        model.fit(X, y)
        
        metrics = get_common_metrics()
        results = {}
        
        for name, wrapper in metrics.items():
            try:
                score = wrapper(y, model, X)
                results[name] = score
            except Exception as e:
                results[name] = None
        
        # Should have computed several metrics
        assert len([v for v in results.values() if v is not None]) > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
