"""Tests for threshold tables and fast mode."""
import pytest
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


class TestThresholds:
    """Test pre-computed thresholds and fast mode."""
    
    def test_get_nearest_threshold(self):
        """Test nearest threshold lookup."""
        from cbd.thresholds import get_nearest_threshold
        
        # Exact match
        thresholds = get_nearest_threshold(100, 10, 'accuracy')
        assert thresholds is not None
        assert len(thresholds) == 3  # (p_05, p_01, p_001)
        assert all(0 < t < 1 for t in thresholds)
        
        # Nearest match
        thresholds = get_nearest_threshold(95, 8, 'accuracy')
        assert thresholds is not None
    
    def test_detect_bias_fast_precomputed(self):
        """Test fast detection with pre-computed thresholds."""
        from cbd.thresholds import detect_bias_fast
        
        X = np.random.randn(100, 10)
        y = np.random.randint(0, 2, 100)
        
        model = RandomForestClassifier(random_state=42, n_estimators=5)
        model.fit(X, y)
        
        result = detect_bias_fast(
            model, X, y, accuracy_score,
            metric_name='accuracy',
            use_precomputed=True
        )
        
        assert 'mode' in result
        assert result['mode'] in ['precomputed', 'quick_permutation']
        assert 'computation_time' in result
        assert result['computation_time'] < 1.0  # Should be fast
    
    def test_detect_bias_fast_fallback(self):
        """Test fast detection fallback to permutation."""
        from cbd.thresholds import detect_bias_fast
        
        # Use unusual size that won't have pre-computed threshold
        X = np.random.randn(73, 13)
        y = np.random.randint(0, 2, 73)
        
        model = RandomForestClassifier(random_state=42, n_estimators=5)
        model.fit(X, y)
        
        result = detect_bias_fast(
            model, X, y, accuracy_score,
            use_precomputed=False,  # Force fallback
            n_permutations_fallback=50
        )
        
        assert result['mode'] == 'quick_permutation'
        assert result['n_permutations'] == 50
    
    def test_estimate_computation_time(self):
        """Test computation time estimation."""
        from cbd.thresholds import estimate_computation_time
        
        times = estimate_computation_time(1000, n_permutations=1000, n_jobs=1)
        
        assert 'fast_mode' in times
        assert 'quick_mode' in times
        assert 'full_mode' in times
        assert times['fast_mode'] < times['quick_mode'] < times['full_mode']
        assert times['speedup_fast_vs_full'] > 10
    
    def test_recommend_mode(self):
        """Test mode recommendation."""
        from cbd.thresholds import recommend_mode
        
        # Small dataset -> fast mode
        mode = recommend_mode(100, 10)
        assert mode in ['fast', 'quick', 'full']
        
        # Large dataset -> full mode
        mode = recommend_mode(10000, 100)
        assert mode in ['quick', 'full']
        
        # With time budget
        mode = recommend_mode(1000, 20, time_budget_seconds=0.1)
        assert mode == 'fast'
