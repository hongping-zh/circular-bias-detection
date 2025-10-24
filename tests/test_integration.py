"""
Integration tests for the complete BiasDetector workflow.

Tests the full pipeline from data loading to report generation.
"""

import pytest
import numpy as np
import pandas as pd
from pathlib import Path
from circular_bias_detector import (
    BiasDetector,
    compute_psi,
    compute_ccs,
    compute_rho_pc,
    validate_matrices,
    load_data
)


class TestBiasDetectorIntegration:
    """Integration tests for BiasDetector class."""
    
    def test_basic_detection_workflow(self):
        """Test basic bias detection workflow."""
        # Create test data
        perf_matrix = np.array([
            [0.8, 0.75, 0.82],
            [0.81, 0.76, 0.83],
            [0.82, 0.77, 0.84],
            [0.80, 0.75, 0.82]
        ])
        
        const_matrix = np.array([
            [0.7, 100],
            [0.7, 100],
            [0.7, 100],
            [0.7, 100]
        ])
        
        # Initialize detector
        detector = BiasDetector(
            psi_threshold=0.1,
            ccs_threshold=0.8,
            rho_pc_threshold=0.3
        )
        
        # Run detection
        results = detector.detect_bias(
            performance_matrix=perf_matrix,
            constraint_matrix=const_matrix,
            algorithm_names=['Algo1', 'Algo2', 'Algo3']
        )
        
        # Verify results structure
        assert 'psi_score' in results
        assert 'ccs_score' in results
        assert 'rho_pc_score' in results
        assert 'overall_bias' in results
        assert 'metadata' in results
        
        # For this consistent case, should not detect bias
        assert results['overall_bias'] is False
        assert results['ccs_score'] == 1.0  # Perfect consistency
    
    def test_detection_with_bias(self):
        """Test detection when bias is present."""
        # Create data with strong correlation (bias indicator)
        perf_matrix = np.array([
            [0.5, 0.4],
            [0.6, 0.5],
            [0.7, 0.6],
            [0.8, 0.7],
            [0.9, 0.8]
        ])
        
        # Constraints that correlate with performance
        const_matrix = np.array([
            [0.5, 50],
            [0.6, 75],
            [0.7, 100],
            [0.8, 125],
            [0.9, 150]
        ])
        
        detector = BiasDetector(
            psi_threshold=0.05,
            ccs_threshold=0.9,
            rho_pc_threshold=0.3
        )
        
        results = detector.detect_bias(perf_matrix, const_matrix)
        
        # Should detect high correlation
        assert abs(results['rho_pc_score']) > 0.7
        assert results['rho_pc_bias'] is True
    
    def test_detection_with_pandas(self):
        """Test detection with pandas DataFrames."""
        # Create DataFrames
        perf_df = pd.DataFrame({
            'algo1': [0.8, 0.81, 0.82, 0.80],
            'algo2': [0.75, 0.76, 0.77, 0.75]
        })
        
        const_df = pd.DataFrame({
            'temperature': [0.7, 0.7, 0.7, 0.7],
            'max_tokens': [100, 100, 100, 100]
        })
        
        detector = BiasDetector()
        results = detector.detect_bias(perf_df, const_df)
        
        assert results['metadata']['algorithm_names'] == ['algo1', 'algo2']
        assert results['metadata']['num_algorithms'] == 2
    
    def test_detection_with_bootstrap(self):
        """Test detection with bootstrap confidence intervals."""
        perf_matrix = np.random.rand(10, 3)
        const_matrix = np.random.rand(10, 2)
        
        detector = BiasDetector()
        results = detector.detect_bias(
            performance_matrix=perf_matrix,
            constraint_matrix=const_matrix,
            enable_bootstrap=True,
            n_bootstrap=500  # Reduced for speed
        )
        
        # Check bootstrap results
        assert results['bootstrap_enabled'] is True
        assert 'psi_ci_lower' in results
        assert 'psi_ci_upper' in results
        assert 'psi_pvalue' in results
        
        # Confidence intervals should bracket point estimate
        assert results['psi_ci_lower'] <= results['psi_score'] <= results['psi_ci_upper']
        assert results['ccs_ci_lower'] <= results['ccs_score'] <= results['ccs_ci_upper']
        assert results['rho_pc_ci_lower'] <= results['rho_pc_score'] <= results['rho_pc_ci_upper']
    
    def test_detection_with_adaptive_thresholds(self):
        """Test detection with adaptive thresholds."""
        np.random.seed(42)
        perf_matrix = np.random.rand(15, 3)
        const_matrix = np.random.rand(15, 2)
        
        detector = BiasDetector()
        results = detector.detect_bias(
            performance_matrix=perf_matrix,
            constraint_matrix=const_matrix,
            enable_adaptive_thresholds=True
        )
        
        # Check adaptive threshold metadata
        assert results['metadata']['adaptive_thresholds_enabled'] is True
        assert 'adaptive_method' in results['metadata']
        
        # Adaptive thresholds should be used
        thresholds = results['metadata']['thresholds']
        assert 'psi' in thresholds
        assert 'ccs' in thresholds
        assert 'rho_pc' in thresholds
    
    def test_detection_from_file(self, tmp_path):
        """Test detection directly from CSV file."""
        # Create test CSV
        data = {
            'time_period': [1, 2, 3, 4, 5],
            'algo1': [0.8, 0.81, 0.82, 0.83, 0.84],
            'algo2': [0.75, 0.76, 0.77, 0.78, 0.79],
            'temperature': [0.7, 0.7, 0.7, 0.7, 0.7],
            'max_tokens': [100, 100, 100, 100, 100]
        }
        df = pd.DataFrame(data)
        
        csv_file = tmp_path / "test_data.csv"
        df.to_csv(csv_file, index=False)
        
        # Run detection from file
        detector = BiasDetector()
        results = detector.detect_from_file(
            data_file=str(csv_file),
            performance_cols=['algo1', 'algo2'],
            constraint_cols=['temperature', 'max_tokens']
        )
        
        assert results['metadata']['num_algorithms'] == 2
        assert results['metadata']['time_periods'] == 5
    
    def test_result_storage(self):
        """Test that results are stored in detector."""
        perf_matrix = np.random.rand(5, 2)
        const_matrix = np.random.rand(5, 2)
        
        detector = BiasDetector()
        results = detector.detect_bias(perf_matrix, const_matrix)
        
        # Results should be stored
        assert detector.last_results is not None
        assert detector.last_results == results
    
    def test_report_generation(self):
        """Test generating human-readable report."""
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
        
        detector = BiasDetector()
        results = detector.detect_bias(perf_matrix, const_matrix)
        report = detector.generate_report(results)
        
        assert isinstance(report, str)
        assert "BIAS DETECTION REPORT" in report
        assert "PSI" in report
        assert "CCS" in report
        assert "ρ_PC" in report or "rho_PC" in report.lower()


class TestModuleAPIs:
    """Test that all module-level APIs work correctly."""
    
    def test_compute_functions(self):
        """Test standalone compute functions."""
        perf_matrix = np.array([[0.8, 0.75], [0.82, 0.78], [0.79, 0.77]])
        const_matrix = np.array([[0.7, 100], [0.7, 100], [0.7, 100]])
        
        # Test individual functions
        psi = compute_psi(perf_matrix)
        ccs = compute_ccs(const_matrix)
        rho_pc = compute_rho_pc(perf_matrix, const_matrix)
        
        assert 0 <= psi
        assert 0 <= ccs <= 1
        assert -1 <= rho_pc <= 1
    
    def test_validation_function(self):
        """Test validation function."""
        perf_matrix = np.array([[0.8, 0.75], [0.82, 0.78]])
        const_matrix = np.array([[0.7, 100], [0.7, 100]])
        
        # Should not raise
        validate_matrices(perf_matrix, const_matrix)
        
        # Should raise on invalid input
        invalid_perf = np.array([0.8, 0.75])  # 1D
        with pytest.raises(ValueError):
            validate_matrices(invalid_perf, const_matrix)


class TestRealWorldScenarios:
    """Tests simulating real-world usage scenarios."""
    
    def test_llm_evaluation_scenario(self):
        """Simulate LLM evaluation across multiple runs."""
        # Simulate 10 evaluation runs with 3 LLMs
        # Performance gradually improves (potential overfitting signal)
        np.random.seed(42)
        
        time_periods = 10
        num_models = 3
        
        # Performance improves over time (red flag)
        perf_matrix = np.zeros((time_periods, num_models))
        for t in range(time_periods):
            base_perf = 0.6 + 0.03 * t  # Gradual improvement
            perf_matrix[t] = base_perf + np.random.randn(num_models) * 0.02
        
        # Constraints also change over time (adaptation)
        const_matrix = np.zeros((time_periods, 2))
        for t in range(time_periods):
            const_matrix[t] = [0.5 + 0.04 * t, 50 + 10 * t]
        
        detector = BiasDetector(
            psi_threshold=0.05,
            ccs_threshold=0.85,
            rho_pc_threshold=0.3
        )
        
        results = detector.detect_bias(
            performance_matrix=perf_matrix,
            constraint_matrix=const_matrix
        )
        
        # Should detect correlation and constraint inconsistency
        assert abs(results['rho_pc_score']) > 0.5  # High correlation
        assert results['ccs_score'] < 0.9  # Low consistency
        assert results['rho_pc_bias'] is True
        assert results['ccs_bias'] is True
    
    def test_stable_evaluation_scenario(self):
        """Simulate stable, unbiased evaluation."""
        # Performance fluctuates randomly (no trend)
        np.random.seed(42)
        
        time_periods = 10
        perf_matrix = 0.8 + np.random.randn(time_periods, 3) * 0.02
        
        # Constraints remain fixed
        const_matrix = np.tile([0.7, 100], (time_periods, 1))
        
        detector = BiasDetector()
        results = detector.detect_bias(perf_matrix, const_matrix)
        
        # Should not detect bias
        assert results['ccs_score'] == 1.0  # Perfect consistency
        assert results['psi_score'] < 0.05  # Low instability
        assert results['overall_bias'] is False
    
    def test_parameter_tuning_scenario(self):
        """Simulate iterative parameter tuning (bias signal)."""
        # Parameters change significantly (tuning iterations)
        algo_params = np.array([
            [[0.5], [0.4], [0.6]],  # Initial
            [[0.6], [0.5], [0.7]],  # Iteration 1
            [[0.7], [0.6], [0.8]],  # Iteration 2
            [[0.8], [0.7], [0.9]],  # Iteration 3
            [[0.9], [0.8], 1.0],    # Iteration 4
        ])
        
        perf_matrix = np.mean(algo_params, axis=2)
        const_matrix = np.random.rand(5, 2)
        
        detector = BiasDetector(psi_threshold=0.05)
        results = detector.detect_bias(
            performance_matrix=perf_matrix,
            constraint_matrix=const_matrix,
            algorithm_params=algo_params
        )
        
        # Should detect high parameter instability
        assert results['psi_score'] > 0.1
        assert results['psi_bias'] is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
