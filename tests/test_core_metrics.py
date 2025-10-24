"""
Unit tests for core metrics computation.

Tests PSI, CCS, ρ_PC, and threshold-based bias detection.
"""

import pytest
import numpy as np
from circular_bias_detector.core.metrics import (
    compute_psi,
    compute_ccs,
    compute_rho_pc,
    compute_all_indicators,
    detect_bias_threshold
)


class TestComputePSI:
    """Tests for PSI (Parameter Stability Index) computation."""
    
    def test_psi_stable_parameters(self):
        """PSI should be low for stable parameters."""
        # Constant performance across time
        perf_matrix = np.array([
            [0.8, 0.75],
            [0.8, 0.75],
            [0.8, 0.75]
        ])
        
        psi = compute_psi(perf_matrix)
        assert psi == 0.0, "Constant parameters should give PSI=0"
    
    def test_psi_unstable_parameters(self):
        """PSI should be high for unstable parameters."""
        # Varying performance across time
        perf_matrix = np.array([
            [0.5, 0.4],
            [0.8, 0.9],
            [0.3, 0.2]
        ])
        
        psi = compute_psi(perf_matrix)
        assert psi > 0.1, "Unstable parameters should give high PSI"
    
    def test_psi_with_algorithm_params(self):
        """Test PSI with explicit algorithm parameters."""
        perf_matrix = np.array([[0.8, 0.75], [0.82, 0.78]])
        algo_params = np.array([
            [[0.5, 0.6], [0.4, 0.7]],  # Time 0
            [[0.5, 0.6], [0.4, 0.7]]   # Time 1 (same)
        ])
        
        psi = compute_psi(perf_matrix, algo_params)
        assert psi == 0.0, "Constant algorithm params should give PSI=0"
    
    def test_psi_single_time_period(self):
        """PSI should return 0 for single time period with warning."""
        perf_matrix = np.array([[0.8, 0.75]])
        
        with pytest.warns(UserWarning, match="at least 2 time periods"):
            psi = compute_psi(perf_matrix)
            assert psi == 0.0


class TestComputeCCS:
    """Tests for CCS (Constraint Consistency Score) computation."""
    
    def test_ccs_perfect_consistency(self):
        """CCS should be 1.0 for constant constraints."""
        const_matrix = np.array([
            [0.7, 100],
            [0.7, 100],
            [0.7, 100]
        ])
        
        ccs = compute_ccs(const_matrix)
        assert ccs == 1.0, "Constant constraints should give CCS=1.0"
    
    def test_ccs_low_consistency(self):
        """CCS should be low for varying constraints."""
        const_matrix = np.array([
            [0.5, 50],
            [0.9, 200],
            [0.3, 10]
        ])
        
        ccs = compute_ccs(const_matrix)
        assert ccs < 0.8, "Varying constraints should give low CCS"
    
    def test_ccs_single_time_period(self):
        """CCS should return 1.0 for single time period with warning."""
        const_matrix = np.array([[0.7, 100]])
        
        with pytest.warns(UserWarning, match="at least 2 time periods"):
            ccs = compute_ccs(const_matrix)
            assert ccs == 1.0
    
    def test_ccs_zero_mean_constraint(self):
        """Test handling of zero mean constraints."""
        const_matrix = np.array([
            [0.0, 100],
            [0.0, 100]
        ])
        
        with pytest.warns(UserWarning, match="Zero mean constraint"):
            ccs = compute_ccs(const_matrix)
            assert 0 <= ccs <= 1


class TestComputeRhoPC:
    """Tests for ρ_PC (Performance-Constraint Correlation) computation."""
    
    def test_rho_pc_positive_correlation(self):
        """Test positive correlation between performance and constraints."""
        perf_matrix = np.array([
            [0.5, 0.4],
            [0.7, 0.6],
            [0.9, 0.8]
        ])
        const_matrix = np.array([
            [0.5, 50],
            [0.7, 100],
            [0.9, 150]
        ])
        
        rho_pc = compute_rho_pc(perf_matrix, const_matrix)
        assert rho_pc > 0.5, "Should detect strong positive correlation"
    
    def test_rho_pc_negative_correlation(self):
        """Test negative correlation."""
        perf_matrix = np.array([
            [0.9, 0.8],
            [0.7, 0.6],
            [0.5, 0.4]
        ])
        const_matrix = np.array([
            [0.5, 50],
            [0.7, 100],
            [0.9, 150]
        ])
        
        rho_pc = compute_rho_pc(perf_matrix, const_matrix)
        assert rho_pc < -0.5, "Should detect strong negative correlation"
    
    def test_rho_pc_no_correlation(self):
        """Test independence (no correlation)."""
        np.random.seed(42)
        perf_matrix = np.random.rand(10, 2)
        const_matrix = np.random.rand(10, 2)
        
        rho_pc = compute_rho_pc(perf_matrix, const_matrix)
        assert abs(rho_pc) < 0.5, "Random data should have low correlation"
    
    def test_rho_pc_constant_constraints(self):
        """Test with constant constraints (all variance = 0)."""
        perf_matrix = np.array([
            [0.8, 0.75],
            [0.82, 0.78],
            [0.79, 0.77],
            [0.80, 0.76]
        ])
        # All constraints are constant
        const_matrix = np.array([
            [0.7, 100],
            [0.7, 100],
            [0.7, 100],
            [0.7, 100]
        ])
        
        # Should handle gracefully without error
        rho_pc = compute_rho_pc(perf_matrix, const_matrix)
        assert rho_pc == 0.0, "Constant constraints should give ρ_PC=0"
    
    def test_rho_pc_dimension_mismatch(self):
        """Test error on dimension mismatch."""
        perf_matrix = np.array([[0.8, 0.75], [0.82, 0.78]])
        const_matrix = np.array([[0.7, 100]])
        
        with pytest.raises(ValueError, match="same time dimension"):
            compute_rho_pc(perf_matrix, const_matrix)
    
    def test_rho_pc_few_time_periods(self):
        """Test warning for few time periods."""
        perf_matrix = np.array([[0.8, 0.75], [0.82, 0.78]])
        const_matrix = np.array([[0.7, 100], [0.7, 100]])
        
        with pytest.warns(UserWarning, match="at least 3 time periods"):
            rho_pc = compute_rho_pc(perf_matrix, const_matrix)
            assert rho_pc == 0.0


class TestDetectBiasThreshold:
    """Tests for threshold-based bias detection."""
    
    def test_no_bias_detected(self):
        """Test case with no bias indicators."""
        result = detect_bias_threshold(
            psi_score=0.05,  # Below threshold
            ccs_score=0.95,  # Above threshold
            rho_pc_score=0.1,  # Below threshold
        )
        
        assert result['overall_bias'] is False
        assert result['bias_votes'] == 0
        assert result['confidence'] == 0.0
    
    def test_all_bias_detected(self):
        """Test case with all bias indicators triggered."""
        result = detect_bias_threshold(
            psi_score=0.5,   # Above threshold (0.1)
            ccs_score=0.5,   # Below threshold (0.8)
            rho_pc_score=0.8,  # Above threshold (0.3)
        )
        
        assert result['overall_bias'] is True
        assert result['bias_votes'] == 3
        assert result['confidence'] == 1.0
        assert result['psi_bias'] is True
        assert result['ccs_bias'] is True
        assert result['rho_pc_bias'] is True
    
    def test_majority_vote_bias(self):
        """Test majority voting (2 out of 3)."""
        result = detect_bias_threshold(
            psi_score=0.15,  # Above threshold -> bias
            ccs_score=0.7,   # Below threshold -> bias
            rho_pc_score=0.1,  # Below threshold -> no bias
        )
        
        assert result['overall_bias'] is True
        assert result['bias_votes'] == 2
        assert result['confidence'] == pytest.approx(2/3)
    
    def test_custom_thresholds(self):
        """Test with custom thresholds."""
        result = detect_bias_threshold(
            psi_score=0.15,
            ccs_score=0.85,
            rho_pc_score=0.4,
            psi_threshold=0.2,   # Higher threshold
            ccs_threshold=0.9,   # Higher threshold
            rho_pc_threshold=0.5  # Higher threshold
        )
        
        assert result['overall_bias'] is False
        assert result['bias_votes'] == 0


class TestComputeAllIndicators:
    """Tests for combined indicator computation."""
    
    def test_compute_all_indicators(self):
        """Test computing all indicators at once."""
        perf_matrix = np.array([
            [0.8, 0.75],
            [0.82, 0.78],
            [0.79, 0.77]
        ])
        const_matrix = np.array([
            [0.7, 100],
            [0.7, 100],
            [0.7, 100]
        ])
        
        results = compute_all_indicators(perf_matrix, const_matrix)
        
        # Check all metrics present
        assert 'psi_score' in results
        assert 'ccs_score' in results
        assert 'rho_pc_score' in results
        assert 'overall_bias' in results
        assert 'bias_votes' in results
        
        # Check ranges
        assert 0 <= results['psi_score'] <= 1
        assert 0 <= results['ccs_score'] <= 1
        assert -1 <= results['rho_pc_score'] <= 1
        
        # For this stable case, should detect no bias
        assert results['overall_bias'] is False
    
    def test_compute_all_with_bias(self):
        """Test with data that should trigger bias detection."""
        # High correlation and instability
        perf_matrix = np.array([
            [0.5, 0.4],
            [0.7, 0.6],
            [0.9, 0.8]
        ])
        const_matrix = np.array([
            [0.5, 50],
            [0.7, 100],
            [0.9, 150]
        ])
        
        results = compute_all_indicators(
            perf_matrix,
            const_matrix,
            psi_threshold=0.05,
            ccs_threshold=0.9,
            rho_pc_threshold=0.3
        )
        
        # Should detect high correlation at minimum
        assert abs(results['rho_pc_score']) > 0.5
        assert results['rho_pc_bias'] is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
