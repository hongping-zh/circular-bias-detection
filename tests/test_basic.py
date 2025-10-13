#!/usr/bin/env python3
"""
Basic test suite for the Circular Reasoning Bias Detection Framework.
Tests core functionality of the BiasDetector and utility functions.
"""

import unittest
import numpy as np
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from circular_bias_detector import BiasDetector
from circular_bias_detector.core import compute_psi, compute_ccs, compute_rho_pc
from circular_bias_detector.utils import create_synthetic_data


class TestCoreMetrics(unittest.TestCase):
    """Test core statistical metrics."""
    
    def setUp(self):
        """Set up test fixtures."""
        np.random.seed(42)
        
    def test_compute_psi_stable(self):
        """Test PSI computation with stable parameters."""
        # Create stable parameter matrix
        theta = np.array([
            [0.7, 0.8, 0.75],
            [0.71, 0.81, 0.76],
            [0.70, 0.79, 0.75],
            [0.72, 0.80, 0.77]
        ])
        
        psi_score = compute_psi(theta)
        
        # PSI should be low for stable parameters
        self.assertIsInstance(psi_score, float)
        self.assertGreaterEqual(psi_score, 0)
        self.assertLess(psi_score, 0.1)  # Stable = low PSI
        
    def test_compute_psi_unstable(self):
        """Test PSI computation with unstable parameters."""
        # Create unstable parameter matrix
        theta = np.array([
            [0.5, 0.6, 0.55],
            [0.7, 0.8, 0.75],
            [0.4, 0.5, 0.45],
            [0.8, 0.9, 0.85]
        ])
        
        psi_score = compute_psi(theta)
        
        # PSI should be high for unstable parameters
        self.assertGreater(psi_score, 0.1)
        
    def test_compute_ccs_consistent(self):
        """Test CCS computation with consistent constraints."""
        # Create consistent constraint matrix
        constraints = np.array([
            [100, 8, 50000],
            [102, 8.1, 50500],
            [101, 8.0, 50200],
            [103, 8.2, 50800]
        ])
        
        ccs_score = compute_ccs(constraints)
        
        # CCS should be high for consistent constraints
        self.assertIsInstance(ccs_score, float)
        self.assertGreaterEqual(ccs_score, 0)
        self.assertLessEqual(ccs_score, 1)
        self.assertGreater(ccs_score, 0.8)  # Consistent = high CCS
        
    def test_compute_ccs_inconsistent(self):
        """Test CCS computation with inconsistent constraints."""
        # Create inconsistent constraint matrix
        constraints = np.array([
            [100, 8, 50000],
            [200, 12, 80000],
            [50, 4, 20000],
            [300, 16, 100000]
        ])
        
        ccs_score = compute_ccs(constraints)
        
        # CCS should be low for inconsistent constraints
        self.assertLess(ccs_score, 0.5)
        
    def test_compute_rho_pc(self):
        """Test performance-constraint correlation computation."""
        performance = np.array([
            [0.7, 0.6, 0.65],
            [0.8, 0.7, 0.75],
            [0.85, 0.75, 0.80],
            [0.9, 0.8, 0.85]
        ])
        
        constraints = np.array([
            [100, 8, 50000],
            [150, 10, 60000],
            [200, 12, 70000],
            [250, 14, 80000]
        ])
        
        rho_pc = compute_rho_pc(performance, constraints)
        
        # Should return a correlation value
        self.assertIsInstance(rho_pc, float)
        self.assertGreaterEqual(rho_pc, -1)
        self.assertLessEqual(rho_pc, 1)


class TestBiasDetector(unittest.TestCase):
    """Test the BiasDetector class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.detector = BiasDetector()
        np.random.seed(42)
        
    def test_detector_initialization(self):
        """Test BiasDetector initialization."""
        self.assertIsInstance(self.detector, BiasDetector)
        
    def test_detect_bias_clean_data(self):
        """Test bias detection on clean (unbiased) data."""
        perf, const = create_synthetic_data(
            n_time_periods=10,
            n_algorithms=3,
            n_constraints=3,
            bias_intensity=0.0,  # No bias
            random_seed=42
        )
        
        results = self.detector.detect_bias(
            performance_matrix=perf,
            constraint_matrix=const,
            algorithm_names=['A1', 'A2', 'A3']
        )
        
        # Check result structure
        self.assertIn('psi_score', results)
        self.assertIn('ccs_score', results)
        self.assertIn('rho_pc_score', results)
        self.assertIn('overall_bias', results)
        self.assertIn('confidence', results)
        
        # Check types
        self.assertIsInstance(results['psi_score'], float)
        self.assertIsInstance(results['ccs_score'], float)
        self.assertIsInstance(results['rho_pc_score'], float)
        self.assertIsInstance(results['overall_bias'], bool)
        self.assertIsInstance(results['confidence'], float)
        
    def test_detect_bias_biased_data(self):
        """Test bias detection on biased data."""
        perf, const = create_synthetic_data(
            n_time_periods=10,
            n_algorithms=3,
            n_constraints=3,
            bias_intensity=0.8,  # High bias
            random_seed=123
        )
        
        results = self.detector.detect_bias(
            performance_matrix=perf,
            constraint_matrix=const,
            algorithm_names=['A1', 'A2', 'A3']
        )
        
        # Biased data should be detected
        self.assertTrue(results['overall_bias'] or results['confidence'] > 0.5)
        
    def test_invalid_input_dimensions(self):
        """Test handling of invalid input dimensions."""
        perf = np.random.rand(10, 3)
        const = np.random.rand(5, 3)  # Wrong dimension
        
        with self.assertRaises(ValueError):
            self.detector.detect_bias(
                performance_matrix=perf,
                constraint_matrix=const,
                algorithm_names=['A1', 'A2', 'A3']
            )
            
    def test_generate_report(self):
        """Test report generation."""
        perf, const = create_synthetic_data(
            n_time_periods=10,
            n_algorithms=3,
            n_constraints=3,
            bias_intensity=0.5,
            random_seed=42
        )
        
        results = self.detector.detect_bias(
            performance_matrix=perf,
            constraint_matrix=const,
            algorithm_names=['A1', 'A2', 'A3']
        )
        
        report = self.detector.generate_report(results)
        
        self.assertIsInstance(report, str)
        self.assertGreater(len(report), 0)
        self.assertIn('PSI', report)
        self.assertIn('CCS', report)


class TestUtilityFunctions(unittest.TestCase):
    """Test utility functions."""
    
    def test_create_synthetic_data(self):
        """Test synthetic data generation."""
        perf, const = create_synthetic_data(
            n_time_periods=15,
            n_algorithms=4,
            n_constraints=3,
            bias_intensity=0.5,
            random_seed=42
        )
        
        # Check dimensions
        self.assertEqual(perf.shape, (15, 4))
        self.assertEqual(const.shape, (15, 3))
        
        # Check value ranges
        self.assertTrue(np.all(perf >= 0))
        self.assertTrue(np.all(perf <= 1))
        self.assertTrue(np.all(const >= 0))
        
    def test_synthetic_data_reproducibility(self):
        """Test that synthetic data is reproducible with same seed."""
        perf1, const1 = create_synthetic_data(
            n_time_periods=10,
            n_algorithms=3,
            n_constraints=3,
            bias_intensity=0.5,
            random_seed=42
        )
        
        perf2, const2 = create_synthetic_data(
            n_time_periods=10,
            n_algorithms=3,
            n_constraints=3,
            bias_intensity=0.5,
            random_seed=42
        )
        
        np.testing.assert_array_equal(perf1, perf2)
        np.testing.assert_array_equal(const1, const2)


def run_tests():
    """Run all tests."""
    unittest.main(argv=[''], verbosity=2, exit=False)


if __name__ == '__main__':
    print("=" * 70)
    print("Running Circular Bias Detection Framework Test Suite")
    print("=" * 70)
    unittest.main(verbosity=2)
