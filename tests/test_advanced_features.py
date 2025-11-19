"""Tests for advanced features: prompt analysis, risk summary, and multivariate detection."""
import pytest
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score


class TestPromptAnalysis:
    """Test prompt variation quantification."""
    
    def test_compute_prompt_similarity_basic(self):
        """Test basic prompt similarity computation."""
        pytest.importorskip("sentence_transformers")
        from cbd.prompt_analysis import compute_prompt_similarity
        
        prompts = [
            "Translate English to French",
            "Translate to French",
            "What is the capital of France?"
        ]
        
        similarity_matrix = compute_prompt_similarity(prompts)
        
        assert similarity_matrix.shape == (3, 3)
        assert np.allclose(np.diag(similarity_matrix), 1.0)  # Self-similarity = 1
        assert similarity_matrix[0, 1] > similarity_matrix[0, 2]  # Similar prompts more similar
    
    def test_detect_prompt_constraint_cheating(self):
        """Test prompt constraint cheating detection."""
        pytest.importorskip("sentence_transformers")
        from cbd.prompt_analysis import detect_prompt_constraint_cheating
        
        # Suspicious: very similar prompts, different performance
        prompts = [
            "Translate to French: Hello",
            "Translate into French: Hello",
            "French translation: Hello"
        ]
        scores = [0.95, 0.70, 0.88]  # High variance
        
        result = detect_prompt_constraint_cheating(prompts, scores)
        
        assert 'risk_level' in result
        assert 'n_suspicious_pairs' in result
        assert result['n_prompts'] == 3
    
    def test_analyze_prompt_diversity(self):
        """Test prompt diversity analysis."""
        pytest.importorskip("sentence_transformers")
        from cbd.prompt_analysis import analyze_prompt_diversity
        
        prompts = ["Translate: ...", "Summarize: ...", "Answer: ..."]
        
        result = analyze_prompt_diversity(prompts)
        
        assert 'diversity_score' in result
        assert 'diversity_level' in result
        assert 0 <= result['diversity_score'] <= 1
    
    def test_compute_prompt_constraint_score(self):
        """Test single constraint score computation."""
        pytest.importorskip("sentence_transformers")
        from cbd.prompt_analysis import compute_prompt_constraint_score
        
        prompts = ["Test A", "Test B"]
        score = compute_prompt_constraint_score(prompts)
        
        assert 0 <= score <= 1


class TestRiskSummary:
    """Test risk summary generation."""
    
    def test_generate_risk_summary_high_risk(self):
        """Test risk summary for high-risk case."""
        from cbd.risk_summary import generate_risk_summary
        
        detection_result = {
            'p_value': 0.001,
            'alpha': 0.05,
            'observed_metric': 0.95,
            'n_permutations': 1000
        }
        
        summary = generate_risk_summary(detection_result, "accuracy")
        
        assert "风险" in summary or "risk" in summary.lower()
        assert "0.001" in summary or "0.95" in summary
    
    def test_generate_risk_summary_low_risk(self):
        """Test risk summary for low-risk case."""
        from cbd.risk_summary import generate_risk_summary
        
        detection_result = {
            'p_value': 0.5,
            'alpha': 0.05,
            'observed_metric': 0.75,
            'n_permutations': 1000
        }
        
        summary = generate_risk_summary(detection_result, "accuracy")
        
        assert "低风险" in summary or "low risk" in summary.lower() or "无明显" in summary
    
    def test_generate_batch_risk_summary(self):
        """Test batch risk summary."""
        from cbd.risk_summary import generate_batch_risk_summary
        
        results = [
            {'p_value': 0.001, 'alpha': 0.05},
            {'p_value': 0.03, 'alpha': 0.05},
            {'p_value': 0.5, 'alpha': 0.05}
        ]
        
        summary = generate_batch_risk_summary(results)
        
        assert "3个测试" in summary or "3" in summary
        assert "2个" in summary or "异常" in summary
    
    def test_create_risk_report(self):
        """Test comprehensive risk report creation."""
        from cbd.risk_summary import create_risk_report
        
        detection_result = {
            'p_value': 0.01,
            'alpha': 0.05,
            'observed_metric': 0.92,
            'n_permutations': 1000,
            'null_method': 'permute',
            'backend': 'sequential'
        }
        
        report = create_risk_report(detection_result, "F1 score")
        
        assert len(report) > 100  # Should be substantial
        assert "风险" in report or "risk" in report.lower()


class TestMultivariateDetection:
    """Test multivariate bias detection."""
    
    def test_detect_multivariate_bias_energy(self):
        """Test multivariate detection with energy distance."""
        from cbd.multivariate_detection import detect_multivariate_bias
        
        X = np.random.randn(100, 5)
        y = np.random.randint(0, 2, 100)
        
        model = RandomForestClassifier(random_state=42, n_estimators=10)
        model.fit(X, y)
        
        metrics = [accuracy_score, f1_score, precision_score]
        
        result = detect_multivariate_bias(
            model, X, y, metrics,
            metric_names=['Accuracy', 'F1', 'Precision'],
            n_permutations=50,  # Small for speed
            method='energy',
            random_state=42
        )
        
        assert 'p_value' in result
        assert 'test_type' in result
        assert result['n_metrics'] == 3
        assert 'individual_stats' in result
        assert len(result['individual_stats']) == 3
    
    def test_detect_multivariate_bias_manova(self):
        """Test multivariate detection with MANOVA."""
        pytest.importorskip("scipy")
        from cbd.multivariate_detection import detect_multivariate_bias
        
        X = np.random.randn(50, 5)
        y = np.random.randint(0, 2, 50)
        
        model = RandomForestClassifier(random_state=42, n_estimators=5)
        model.fit(X, y)
        
        metrics = [accuracy_score, f1_score]
        
        result = detect_multivariate_bias(
            model, X, y, metrics,
            n_permutations=20,
            method='manova',
            random_state=42
        )
        
        assert result['method'] == 'manova'
        assert 'test_statistic' in result
    
    def test_detect_multitask_bias(self):
        """Test multitask bias detection."""
        from cbd.multivariate_detection import detect_multitask_bias
        
        # Create 3 simple tasks
        models = {}
        X_dict = {}
        y_dict = {}
        
        for task_name in ['task1', 'task2', 'task3']:
            X = np.random.randn(50, 5)
            y = np.random.randint(0, 2, 50)
            
            model = RandomForestClassifier(random_state=42, n_estimators=5)
            model.fit(X, y)
            
            models[task_name] = model
            X_dict[task_name] = X
            y_dict[task_name] = y
        
        result = detect_multitask_bias(
            models, X_dict, y_dict,
            accuracy_score,
            n_permutations=20,
            random_state=42
        )
        
        assert result['n_tasks'] == 3
        assert 'task_stats' in result
        assert len(result['task_stats']) == 3
    
    def test_compute_multivariate_psi(self):
        """Test multivariate PSI computation."""
        pytest.importorskip("scipy")
        from cbd.multivariate_detection import compute_multivariate_psi
        
        # Performance increases with model size (suspicious)
        performance_matrix = np.array([
            [0.70, 0.68, 0.72],  # Small model
            [0.85, 0.83, 0.87],  # Medium model
            [0.95, 0.94, 0.96]   # Large model
        ])
        costs = np.array([1e6, 1e8, 1e10])
        
        result = compute_multivariate_psi(performance_matrix, costs)
        
        assert 'risk_level' in result
        assert 'avg_abs_correlation' in result
        assert 'combined_p_value' in result
        assert result['n_models'] == 3
        assert result['n_metrics'] == 3


class TestIntegration:
    """Integration tests combining multiple features."""
    
    def test_full_pipeline_with_risk_summary(self):
        """Test full detection pipeline with risk summary."""
        from cbd.api import detect_bias
        from cbd.risk_summary import generate_risk_summary
        
        X = np.random.randn(100, 5)
        y = np.random.randint(0, 2, 100)
        
        model = RandomForestClassifier(random_state=42)
        model.fit(X, y)
        
        result = detect_bias(model, X, y, accuracy_score, n_permutations=50)
        summary = generate_risk_summary(result, "accuracy")
        
        assert isinstance(summary, str)
        assert len(summary) > 20
    
    def test_multivariate_with_risk_summary(self):
        """Test multivariate detection with risk summary."""
        from cbd.multivariate_detection import detect_multivariate_bias
        from cbd.risk_summary import generate_multivariate_risk_summary
        
        X = np.random.randn(50, 5)
        y = np.random.randint(0, 2, 50)
        
        model = RandomForestClassifier(random_state=42, n_estimators=5)
        model.fit(X, y)
        
        result = detect_multivariate_bias(
            model, X, y,
            [accuracy_score, f1_score],
            n_permutations=20,
            random_state=42
        )
        
        summary = generate_multivariate_risk_summary(result, ['Accuracy', 'F1'])
        
        assert isinstance(summary, str)
        assert "指标" in summary or "metric" in summary.lower()
