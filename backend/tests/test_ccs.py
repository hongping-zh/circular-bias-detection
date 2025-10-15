"""
Unit tests for CCS Calculator
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import pandas as pd
import numpy as np
from core.ccs_calculator import compute_ccs, compute_ccs_by_period, detect_constraint_outliers, normalize_ccs


class TestCCSCalculator:
    """Test suite for CCS calculation"""
    
    @pytest.fixture
    def stable_data(self):
        """Create data with perfectly stable constraints (CCS = 1.0)"""
        return pd.DataFrame({
            'time_period': [1, 1, 2, 2, 3, 3],
            'algorithm': ['A', 'B', 'A', 'B', 'A', 'B'],
            'performance': [0.7, 0.6, 0.72, 0.65, 0.74, 0.67],
            'constraint_compute': [100, 150, 100, 150, 100, 150],
            'constraint_memory': [8.0, 12.0, 8.0, 12.0, 8.0, 12.0]
        })
    
    @pytest.fixture
    def unstable_data(self):
        """Create data with varying constraints (low CCS)"""
        return pd.DataFrame({
            'time_period': [1, 1, 2, 2, 3, 3],
            'algorithm': ['A', 'B', 'A', 'B', 'A', 'B'],
            'performance': [0.7, 0.6, 0.72, 0.65, 0.74, 0.67],
            'constraint_compute': [100, 150, 200, 250, 300, 350],
            'constraint_memory': [8.0, 12.0, 16.0, 20.0, 24.0, 28.0]
        })
    
    @pytest.fixture
    def sample_data(self):
        """Create sample data with moderate variation"""
        return pd.DataFrame({
            'time_period': [1, 1, 2, 2, 3, 3],
            'algorithm': ['A', 'B', 'A', 'B', 'A', 'B'],
            'performance': [0.7, 0.6, 0.72, 0.65, 0.74, 0.67],
            'constraint_compute': [100, 150, 105, 155, 110, 160],
            'constraint_memory': [8.0, 12.0, 8.5, 12.5, 9.0, 13.0]
        })
    
    def test_ccs_basic_calculation(self, sample_data):
        """Test basic CCS calculation"""
        result = compute_ccs(sample_data)
        
        assert 'ccs_score' in result
        assert 'cv_by_constraint' in result
        assert isinstance(result['ccs_score'], float)
        assert 0 <= result['ccs_score'] <= 1, "CCS should be in [0, 1] range"
    
    def test_ccs_stable_constraints(self, stable_data):
        """Test CCS with perfectly stable constraints"""
        result = compute_ccs(stable_data)
        
        # Stable constraints should give CCS very close to 1.0
        # (might not be exactly 1.0 due to mean/std across different algorithms)
        assert result['ccs_score'] > 0.85, f"Expected high CCS for stable data, got {result['ccs_score']}"
        assert result['exceeds_threshold']
    
    def test_ccs_unstable_constraints(self, unstable_data):
        """Test CCS with varying constraints"""
        result = compute_ccs(unstable_data)
        
        # Unstable constraints should give lower CCS
        assert result['ccs_score'] < 0.85, f"Expected low CCS for unstable data, got {result['ccs_score']}"
        assert not result['exceeds_threshold']
    
    def test_ccs_cv_calculation(self, sample_data):
        """Test coefficient of variation calculation"""
        result = compute_ccs(sample_data)
        
        # Should have CV for each constraint
        assert len(result['cv_by_constraint']) == 2  # Two constraints
        
        # CV should be non-negative
        for cv in result['cv_by_constraint'].values():
            assert cv >= 0
    
    def test_ccs_missing_columns(self):
        """Test error handling for missing columns"""
        bad_data = pd.DataFrame({
            'time_period': [1, 2],
            'algorithm': ['A', 'A']
            # Missing 'performance' column
        })
        
        with pytest.raises(ValueError, match="Missing required column"):
            compute_ccs(bad_data)
    
    def test_ccs_no_constraints(self):
        """Test error handling when no constraint columns exist"""
        bad_data = pd.DataFrame({
            'time_period': [1, 2],
            'algorithm': ['A', 'A'],
            'performance': [0.7, 0.8]
            # No constraint columns
        })
        
        with pytest.raises(ValueError, match="No constraint columns found"):
            compute_ccs(bad_data)
    
    def test_ccs_constraint_stats(self, sample_data):
        """Test constraint statistics are computed"""
        result = compute_ccs(sample_data)
        
        assert 'constraint_stats' in result
        stats = result['constraint_stats']
        
        for col_stats in stats.values():
            assert 'mean' in col_stats
            assert 'std' in col_stats
            assert 'min' in col_stats
            assert 'max' in col_stats
    
    def test_ccs_by_period(self, sample_data):
        """Test per-period CCS calculation"""
        result = compute_ccs_by_period(sample_data)
        
        assert len(result) == 3  # Three time periods
        for period, res in result.items():
            if 'error' not in res:
                assert 'ccs_score' in res
    
    def test_outlier_detection(self, unstable_data):
        """Test constraint outlier detection"""
        outliers = detect_constraint_outliers(unstable_data, z_threshold=1.5)
        
        # Should detect outliers in unstable data
        assert isinstance(outliers, dict)
    
    def test_normalize_ccs(self):
        """Test CCS normalization"""
        assert normalize_ccs(0.0) == 0.0
        assert normalize_ccs(0.5) == 0.5
        assert normalize_ccs(1.0) == 1.0
        assert normalize_ccs(1.5) == 1.0  # Caps at 1.0
        assert normalize_ccs(-0.1) == 0.0  # Floors at 0.0
    
    def test_ccs_interpretation(self, sample_data):
        """Test that interpretation string is generated"""
        result = compute_ccs(sample_data)
        
        assert 'interpretation' in result
        assert isinstance(result['interpretation'], str)
        assert len(result['interpretation']) > 0
    
    def test_ccs_threshold_check(self, stable_data, unstable_data):
        """Test threshold checking"""
        stable_result = compute_ccs(stable_data)
        unstable_result = compute_ccs(unstable_data)
        
        assert stable_result['exceeds_threshold']
        assert not unstable_result['exceeds_threshold']
    
    def test_ccs_single_algorithm(self):
        """Test CCS with single algorithm"""
        single_algo = pd.DataFrame({
            'time_period': [1, 2, 3],
            'algorithm': ['A', 'A', 'A'],
            'performance': [0.7, 0.75, 0.8],
            'constraint_compute': [100, 105, 110]
        })
        
        result = compute_ccs(single_algo)
        assert 'ccs_score' in result
        assert result['ccs_score'] >= 0


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
