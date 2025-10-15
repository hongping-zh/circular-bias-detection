"""
Unit tests for PSI Calculator
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import pandas as pd
import numpy as np
from core.psi_calculator import compute_psi, compute_psi_per_algorithm, normalize_psi


class TestPSICalculator:
    """Test suite for PSI calculation"""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample evaluation data"""
        return pd.DataFrame({
            'time_period': [1, 1, 2, 2, 3, 3],
            'algorithm': ['A', 'B', 'A', 'B', 'A', 'B'],
            'performance': [0.7, 0.6, 0.72, 0.65, 0.74, 0.67],
            'constraint_compute': [100, 150, 105, 155, 110, 160],
            'constraint_memory': [8.0, 12.0, 8.5, 12.5, 9.0, 13.0]
        })
    
    @pytest.fixture
    def stable_data(self):
        """Create data with stable parameters (low PSI expected)"""
        return pd.DataFrame({
            'time_period': [1, 1, 2, 2, 3, 3],
            'algorithm': ['A', 'B', 'A', 'B', 'A', 'B'],
            'performance': [0.7, 0.6, 0.71, 0.61, 0.72, 0.62],
            'constraint_compute': [100, 150, 100, 150, 100, 150],  # No change
            'constraint_memory': [8.0, 12.0, 8.0, 12.0, 8.0, 12.0]  # No change
        })
    
    @pytest.fixture
    def unstable_data(self):
        """Create data with unstable parameters (high PSI expected)"""
        return pd.DataFrame({
            'time_period': [1, 1, 2, 2, 3, 3],
            'algorithm': ['A', 'B', 'A', 'B', 'A', 'B'],
            'performance': [0.7, 0.6, 0.72, 0.65, 0.74, 0.67],
            'constraint_compute': [100, 150, 200, 250, 300, 350],  # Large change
            'constraint_memory': [8.0, 12.0, 16.0, 20.0, 24.0, 28.0]  # Large change
        })
    
    def test_psi_basic_calculation(self, sample_data):
        """Test basic PSI calculation"""
        result = compute_psi(sample_data)
        
        assert 'psi_score' in result
        assert 'psi_by_period' in result
        assert isinstance(result['psi_score'], float)
        assert result['psi_score'] >= 0
        
        # Should have 2 distances for 3 time periods
        assert len(result['psi_by_period']) == 2
    
    def test_psi_stable_parameters(self, stable_data):
        """Test PSI with stable parameters (should be low)"""
        result = compute_psi(stable_data)
        
        # Stable parameters should give PSI ≈ 0
        assert result['psi_score'] < 0.01, f"Expected low PSI for stable data, got {result['psi_score']}"
        assert not result['exceeds_threshold']
    
    def test_psi_unstable_parameters(self, unstable_data):
        """Test PSI with unstable parameters (should be high)"""
        result = compute_psi(unstable_data)
        
        # Unstable parameters should give higher PSI
        assert result['psi_score'] > 0.15, f"Expected high PSI for unstable data, got {result['psi_score']}"
        assert result['exceeds_threshold']
    
    def test_psi_missing_columns(self):
        """Test error handling for missing columns"""
        bad_data = pd.DataFrame({
            'time_period': [1, 2],
            'algorithm': ['A', 'A']
            # Missing 'performance' column
        })
        
        with pytest.raises(ValueError, match="Missing required column"):
            compute_psi(bad_data)
    
    def test_psi_no_constraints(self):
        """Test error handling when no constraint columns exist"""
        bad_data = pd.DataFrame({
            'time_period': [1, 2],
            'algorithm': ['A', 'A'],
            'performance': [0.7, 0.8]
            # No constraint columns
        })
        
        with pytest.raises(ValueError, match="No constraint columns found"):
            compute_psi(bad_data)
    
    def test_psi_single_period(self):
        """Test handling of single time period"""
        single_period = pd.DataFrame({
            'time_period': [1, 1],
            'algorithm': ['A', 'B'],
            'performance': [0.7, 0.6],
            'constraint_compute': [100, 150]
        })
        
        result = compute_psi(single_period)
        
        assert result['psi_score'] == 0.0
        assert 'warning' in result
    
    def test_psi_per_algorithm(self, sample_data):
        """Test per-algorithm PSI calculation"""
        result = compute_psi_per_algorithm(sample_data)
        
        assert 'A' in result
        assert 'B' in result
        assert 'psi_score' in result['A']
        assert 'psi_score' in result['B']
    
    def test_normalize_psi(self):
        """Test PSI normalization"""
        assert normalize_psi(0.0) == 0.0
        assert normalize_psi(0.5) == 0.5
        assert normalize_psi(1.0) == 1.0
        assert normalize_psi(2.0) == 1.0  # Caps at 1.0
    
    def test_psi_interpretation(self, sample_data):
        """Test that interpretation string is generated"""
        result = compute_psi(sample_data)
        
        assert 'interpretation' in result
        assert isinstance(result['interpretation'], str)
        assert len(result['interpretation']) > 0
    
    def test_psi_threshold_check(self, stable_data, unstable_data):
        """Test threshold checking"""
        stable_result = compute_psi(stable_data)
        unstable_result = compute_psi(unstable_data)
        
        assert not stable_result['exceeds_threshold']
        assert unstable_result['exceeds_threshold']


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
