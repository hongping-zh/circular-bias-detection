"""
Unit tests for matrix operations and validation.
"""

import pytest
import numpy as np
import pandas as pd
from circular_bias_detector.core.matrix import (
    validate_matrices,
    prepare_performance_matrix,
    prepare_constraint_matrix,
    normalize_matrix,
    check_matrix_quality
)


class TestValidateMatrices:
    """Tests for matrix validation."""
    
    def test_valid_matrices(self):
        """Test validation of valid matrices."""
        perf = np.array([[0.8, 0.75], [0.82, 0.78]])
        const = np.array([[0.7, 100], [0.7, 100]])
        
        # Should not raise
        validate_matrices(perf, const)
    
    def test_invalid_performance_shape(self):
        """Test error on invalid performance matrix shape."""
        perf = np.array([0.8, 0.75])  # 1D
        const = np.array([[0.7, 100], [0.7, 100]])
        
        with pytest.raises(ValueError, match="must be 2D"):
            validate_matrices(perf, const)
    
    def test_invalid_constraint_shape(self):
        """Test error on invalid constraint matrix shape."""
        perf = np.array([[0.8, 0.75], [0.82, 0.78]])
        const = np.array([0.7, 100])  # 1D
        
        with pytest.raises(ValueError, match="must be 2D"):
            validate_matrices(perf, const)
    
    def test_time_dimension_mismatch(self):
        """Test error on time dimension mismatch."""
        perf = np.array([[0.8, 0.75], [0.82, 0.78]])
        const = np.array([[0.7, 100]])  # Only 1 time period
        
        with pytest.raises(ValueError, match="Time dimension mismatch"):
            validate_matrices(perf, const)
    
    def test_insufficient_time_periods(self):
        """Test error on insufficient time periods."""
        perf = np.array([[0.8, 0.75]])  # Only 1 time period
        const = np.array([[0.7, 100]])
        
        with pytest.raises(ValueError, match="at least 2 time periods"):
            validate_matrices(perf, const)
    
    def test_nan_values(self):
        """Test error on NaN values."""
        perf = np.array([[0.8, np.nan], [0.82, 0.78]])
        const = np.array([[0.7, 100], [0.7, 100]])
        
        with pytest.raises(ValueError, match="NaN or infinite"):
            validate_matrices(perf, const)
    
    def test_inf_values(self):
        """Test error on infinite values."""
        perf = np.array([[0.8, 0.75], [0.82, 0.78]])
        const = np.array([[0.7, np.inf], [0.7, 100]])
        
        with pytest.raises(ValueError, match="NaN or infinite"):
            validate_matrices(perf, const)
    
    def test_algorithm_params_validation(self):
        """Test validation of algorithm parameters."""
        perf = np.array([[0.8, 0.75], [0.82, 0.78]])
        const = np.array([[0.7, 100], [0.7, 100]])
        params = np.array([
            [[0.5, 0.6], [0.4, 0.7]],
            [[0.5, 0.6], [0.4, 0.7]]
        ])
        
        # Should not raise
        validate_matrices(perf, const, params)
    
    def test_algorithm_params_wrong_shape(self):
        """Test error on wrong algorithm params shape."""
        perf = np.array([[0.8, 0.75], [0.82, 0.78]])
        const = np.array([[0.7, 100], [0.7, 100]])
        params = np.array([[0.5, 0.6], [0.4, 0.7]])  # 2D instead of 3D
        
        with pytest.raises(ValueError, match="must be 3D"):
            validate_matrices(perf, const, params)


class TestPrepareMatrices:
    """Tests for matrix preparation utilities."""
    
    def test_prepare_performance_from_dataframe(self):
        """Test preparing performance matrix from DataFrame."""
        df = pd.DataFrame({
            'algo1': [0.8, 0.82, 0.79],
            'algo2': [0.75, 0.78, 0.77]
        })
        
        matrix, names = prepare_performance_matrix(df)
        
        assert matrix.shape == (3, 2)
        assert names == ['algo1', 'algo2']
        assert np.array_equal(matrix, df.values)
    
    def test_prepare_performance_from_numpy(self):
        """Test preparing performance matrix from numpy array."""
        arr = np.array([[0.8, 0.75], [0.82, 0.78]])
        
        matrix, names = prepare_performance_matrix(arr)
        
        assert matrix.shape == (2, 2)
        assert names is None
        assert np.array_equal(matrix, arr)
    
    def test_prepare_performance_from_list(self):
        """Test preparing performance matrix from list."""
        data = [[0.8, 0.75], [0.82, 0.78]]
        
        matrix, names = prepare_performance_matrix(data)
        
        assert matrix.shape == (2, 2)
        assert names is None
    
    def test_prepare_performance_1d(self):
        """Test automatic reshaping of 1D data."""
        arr = np.array([0.8, 0.82, 0.79])
        
        matrix, names = prepare_performance_matrix(arr)
        
        assert matrix.shape == (3, 1)  # Should be reshaped to 2D
    
    def test_prepare_constraint_from_dataframe(self):
        """Test preparing constraint matrix from DataFrame."""
        df = pd.DataFrame({
            'temperature': [0.7, 0.7, 0.7],
            'max_tokens': [100, 100, 100]
        })
        
        matrix, names = prepare_constraint_matrix(df)
        
        assert matrix.shape == (3, 2)
        assert names == ['temperature', 'max_tokens']
    
    def test_prepare_invalid_type(self):
        """Test error on invalid data type."""
        with pytest.raises(TypeError, match="Unsupported data type"):
            prepare_performance_matrix("invalid")


class TestNormalizeMatrix:
    """Tests for matrix normalization."""
    
    def test_minmax_normalization(self):
        """Test min-max normalization."""
        matrix = np.array([[1, 2], [3, 4]])
        
        normalized = normalize_matrix(matrix, method='minmax')
        
        assert normalized.min() == 0.0
        assert normalized.max() == 1.0
    
    def test_zscore_normalization(self):
        """Test z-score normalization."""
        matrix = np.array([[1, 2], [3, 4]])
        
        normalized = normalize_matrix(matrix, method='zscore')
        
        assert np.abs(normalized.mean()) < 1e-10  # Mean should be ~0
        assert np.abs(normalized.std() - 1.0) < 0.1  # Std should be ~1
    
    def test_no_normalization(self):
        """Test that 'none' method returns unchanged matrix."""
        matrix = np.array([[1, 2], [3, 4]])
        
        normalized = normalize_matrix(matrix, method='none')
        
        assert np.array_equal(normalized, matrix)
    
    def test_normalization_constant_values(self):
        """Test handling of constant values (avoid division by zero)."""
        matrix = np.array([[5, 5], [5, 5]])
        
        # Should not raise, should handle gracefully
        normalized = normalize_matrix(matrix, method='minmax')
        assert np.all(normalized == 0.0)  # All same value -> all zero after normalization
    
    def test_invalid_method(self):
        """Test error on invalid normalization method."""
        matrix = np.array([[1, 2], [3, 4]])
        
        with pytest.raises(ValueError, match="Unknown normalization method"):
            normalize_matrix(matrix, method='invalid')


class TestCheckMatrixQuality:
    """Tests for matrix quality checking."""
    
    def test_quality_check_normal_matrix(self):
        """Test quality check on normal matrix."""
        matrix = np.array([[0.8, 0.75], [0.82, 0.78]])
        
        quality = check_matrix_quality(matrix, name="test")
        
        assert quality['name'] == "test"
        assert quality['shape'] == (2, 2)
        assert quality['has_nan'] is False
        assert quality['has_inf'] is False
        assert quality['has_negative'] is False
        assert quality['rank'] == 2
        assert 'condition_number' in quality
    
    def test_quality_check_with_nan(self):
        """Test detection of NaN values."""
        matrix = np.array([[0.8, np.nan], [0.82, 0.78]])
        
        quality = check_matrix_quality(matrix)
        
        assert quality['has_nan'] is True
    
    def test_quality_check_with_inf(self):
        """Test detection of infinite values."""
        matrix = np.array([[0.8, 0.75], [np.inf, 0.78]])
        
        quality = check_matrix_quality(matrix)
        
        assert quality['has_inf'] is True
    
    def test_quality_check_negative_values(self):
        """Test detection of negative values."""
        matrix = np.array([[0.8, -0.75], [0.82, 0.78]])
        
        quality = check_matrix_quality(matrix)
        
        assert quality['has_negative'] is True
        assert quality['min_value'] < 0
    
    def test_quality_check_sparse_matrix(self):
        """Test sparsity detection."""
        matrix = np.array([[0.8, 0], [0, 0.78], [0, 0]])
        
        quality = check_matrix_quality(matrix)
        
        assert quality['sparsity'] > 0.3  # More than 30% zeros
    
    def test_quality_check_low_rank(self):
        """Test rank detection for rank-deficient matrix."""
        # Create rank-1 matrix (linearly dependent rows)
        matrix = np.array([[1, 2], [2, 4], [3, 6]])
        
        quality = check_matrix_quality(matrix)
        
        assert quality['rank'] == 1  # Should be rank-deficient
        assert quality['condition_number'] > 100  # High condition number


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
