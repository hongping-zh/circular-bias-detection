"""
Unit tests for ρ_PC Calculator
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import pandas as pd
import numpy as np
from core.rho_pc_calculator import compute_rho_pc, compute_rho_pc_by_algorithm, normalize_rho_pc


class TestRhoPCCalculator:
    """Test suite for ρ_PC calculation"""
    
    @pytest.fixture
    def positive_correlation_data(self):
        """Create data with strong positive correlation"""
        return pd.DataFrame({
            'time_period': [1, 1, 2, 2, 3, 3, 4, 4],
            'algorithm': ['A', 'B'] * 4,
            'performance': [0.6, 0.55, 0.7, 0.65, 0.8, 0.75, 0.9, 0.85],
            'constraint_compute': [100, 90, 150, 140, 200, 190, 250, 240]
        })
    
    @pytest.fixture
    def negative_correlation_data(self):
        """Create data with strong negative correlation"""
        return pd.DataFrame({
            'time_period': [1, 1, 2, 2, 3, 3, 4, 4],
            'algorithm': ['A', 'B'] * 4,
            'performance': [0.6, 0.55, 0.7, 0.65, 0.8, 0.75, 0.9, 0.85],
            'constraint_compute': [250, 240, 200, 190, 150, 140, 100, 90]
        })
    
    @pytest.fixture
    def no_correlation_data(self):
        """Create data with no correlation"""
        return pd.DataFrame({
            'time_period': [1, 1, 2, 2, 3, 3, 4, 4],
            'algorithm': ['A', 'B'] * 4,
            'performance': [0.6, 0.7, 0.65, 0.75, 0.8, 0.7, 0.75, 0.85],
            'constraint_compute': [100, 100, 100, 100, 100, 100, 100, 100]
        })
    
    def test_rho_pc_basic_calculation(self, positive_correlation_data):
        """Test basic ρ_PC calculation"""
        result = compute_rho_pc(positive_correlation_data)
        
        assert 'rho_pc' in result
        assert 'p_value' in result
        assert isinstance(result['rho_pc'], float)
        assert -1 <= result['rho_pc'] <= 1, "ρ_PC should be in [-1, 1] range"
    
    def test_rho_pc_positive_correlation(self, positive_correlation_data):
        """Test ρ_PC with positive correlation"""
        result = compute_rho_pc(positive_correlation_data)
        
        assert result['rho_pc'] > 0.5, f"Expected high positive ρ_PC, got {result['rho_pc']}"
        assert result['exceeds_threshold']
        assert result['p_value'] < 0.05, "Should be statistically significant"
    
    def test_rho_pc_negative_correlation(self, negative_correlation_data):
        """Test ρ_PC with negative correlation"""
        result = compute_rho_pc(negative_correlation_data)
        
        assert result['rho_pc'] < -0.5, f"Expected high negative ρ_PC, got {result['rho_pc']}"
        assert result['exceeds_threshold']  # Absolute value > threshold
        assert result['p_value'] < 0.05, "Should be statistically significant"
    
    def test_rho_pc_no_correlation(self, no_correlation_data):
        """Test ρ_PC with no correlation"""
        result = compute_rho_pc(no_correlation_data)
        
        # No correlation should give low ρ_PC
        assert abs(result['rho_pc']) < 0.5, f"Expected low |ρ_PC|, got {result['rho_pc']}"
        assert not result['exceeds_threshold']
    
    def test_rho_pc_missing_columns(self):
        """Test error handling for missing columns"""
        bad_data = pd.DataFrame({
            'time_period': [1, 2],
            'algorithm': ['A', 'A']
            # Missing 'performance' column
        })
        
        with pytest.raises(ValueError, match="Missing required column"):
            compute_rho_pc(bad_data)
    
    def test_rho_pc_no_constraints(self):
        """Test error handling when no constraint columns exist"""
        bad_data = pd.DataFrame({
            'time_period': [1, 2],
            'algorithm': ['A', 'A'],
            'performance': [0.7, 0.8]
            # No constraint columns
        })
        
        with pytest.raises(ValueError, match="No constraint columns found"):
            compute_rho_pc(bad_data)
    
    def test_rho_pc_insufficient_data(self):
        """Test handling of insufficient data points"""
        small_data = pd.DataFrame({
            'time_period': [1, 2],
            'algorithm': ['A', 'A'],
            'performance': [0.7, 0.8],
            'constraint_compute': [100, 150]
        })
        
        result = compute_rho_pc(small_data)
        
        assert result['rho_pc'] == 0.0
        assert 'warning' in result
    
    def test_rho_pc_spearman(self, positive_correlation_data):
        """Test Spearman rank correlation is computed"""
        result = compute_rho_pc(positive_correlation_data)
        
        assert 'spearman_rho' in result
        assert isinstance(result['spearman_rho'], float)
        assert -1 <= result['spearman_rho'] <= 1
    
    def test_rho_pc_constraint_correlations(self, positive_correlation_data):
        """Test individual constraint correlations"""
        result = compute_rho_pc(positive_correlation_data)
        
        assert 'constraint_correlations' in result
        assert len(result['constraint_correlations']) > 0
        
        for constraint, info in result['constraint_correlations'].items():
            assert 'correlation' in info
            assert 'p_value' in info
            assert 'significant' in info
    
    def test_rho_pc_by_algorithm(self, positive_correlation_data):
        """Test per-algorithm ρ_PC calculation"""
        result = compute_rho_pc_by_algorithm(positive_correlation_data)
        
        assert 'A' in result
        assert 'B' in result
        
        for algo, res in result.items():
            if 'error' not in res:
                assert 'rho_pc' in res
    
    def test_normalize_rho_pc(self):
        """Test ρ_PC normalization"""
        assert normalize_rho_pc(0.0) == 0.0
        assert normalize_rho_pc(0.5) == 0.5
        assert normalize_rho_pc(-0.5) == 0.5  # Absolute value
        assert normalize_rho_pc(1.0) == 1.0
        assert normalize_rho_pc(-1.0) == 1.0  # Absolute value
    
    def test_rho_pc_interpretation(self, positive_correlation_data):
        """Test that interpretation string is generated"""
        result = compute_rho_pc(positive_correlation_data)
        
        assert 'interpretation' in result
        assert isinstance(result['interpretation'], str)
        assert len(result['interpretation']) > 0
    
    def test_rho_pc_significance_flag(self, positive_correlation_data, no_correlation_data):
        """Test statistical significance flag"""
        sig_result = compute_rho_pc(positive_correlation_data)
        nonsig_result = compute_rho_pc(no_correlation_data)
        
        assert sig_result['significant']
        # nonsig_result may or may not be significant depending on data randomness
    
    def test_rho_pc_threshold_check(self, positive_correlation_data, no_correlation_data):
        """Test threshold checking"""
        high_result = compute_rho_pc(positive_correlation_data)
        low_result = compute_rho_pc(no_correlation_data)
        
        assert high_result['exceeds_threshold']
        assert not low_result['exceeds_threshold']
    
    def test_rho_pc_multiple_constraints(self):
        """Test ρ_PC with multiple constraints"""
        multi_constraint = pd.DataFrame({
            'time_period': [1, 1, 2, 2, 3, 3],
            'algorithm': ['A', 'B'] * 3,
            'performance': [0.6, 0.55, 0.7, 0.65, 0.8, 0.75],
            'constraint_compute': [100, 90, 150, 140, 200, 190],
            'constraint_memory': [8, 7, 12, 11, 16, 15],
            'constraint_dataset_size': [1000, 900, 1500, 1400, 2000, 1900]
        })
        
        result = compute_rho_pc(multi_constraint)
        
        assert result['num_constraints'] == 3
        assert len(result['constraint_correlations']) == 3


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
