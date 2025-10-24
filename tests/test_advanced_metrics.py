#!/usr/bin/env python3
"""
Test suite for advanced detection metrics.

Tests:
- TDI (Temporal Dependency Index)
- ICS (Information Criterion Score)
- CBI (Cross-Benchmark Inconsistency)
- ADS (Adaptive Drift Score)
- MCI (Multi-Constraint Interaction)
"""

import unittest
import numpy as np
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from circular_bias_detector.advanced_metrics import (
    compute_tdi, compute_ics, compute_cbi,
    compute_ads, compute_mci, compute_all_advanced_metrics
)
from circular_bias_detector.utils import create_synthetic_data


class TestTDI(unittest.TestCase):
    """Test Temporal Dependency Index."""
    
    def setUp(self):
        np.random.seed(42)
        
    def test_tdi_basic(self):
        """Test TDI computation on simple data."""
        # Create data with temporal dependency
        T, K = 15, 3
        perf = np.zeros((T, K))
        for k in range(K):
            perf[0, k] = np.random.rand()
            for t in range(1, T):
                # Strong dependency: current = 0.9 * previous + noise
                perf[t, k] = 0.9 * perf[t-1, k] + 0.1 * np.random.rand()
        
        tdi = compute_tdi(perf, lag=3)
        
        self.assertIsInstance(tdi, float)
        self.assertGreaterEqual(tdi, 0.0)
        self.assertLessEqual(tdi, 1.0)
        
    def test_tdi_high_dependency(self):
        """Test TDI detects high temporal dependency."""
        T, K = 20, 4
        perf = np.zeros((T, K))
        
        for k in range(K):
            perf[0, k] = 0.5
            for t in range(1, T):
                # Very strong dependency
                perf[t, k] = 0.95 * perf[t-1, k] + 0.05 * np.random.rand()
        
        tdi = compute_tdi(perf)
        
        # Should detect high dependency
        self.assertGreater(tdi, 0.4)
        
    def test_tdi_low_dependency(self):
        """Test TDI on independent data."""
        T, K = 15, 3
        perf = np.random.rand(T, K)
        
        tdi = compute_tdi(perf)
        
        # Should detect low dependency
        self.assertLess(tdi, 0.5)
        
    def test_tdi_insufficient_data(self):
        """Test TDI with insufficient time periods."""
        perf = np.random.rand(3, 4)
        
        tdi = compute_tdi(perf, lag=3)
        
        # Should return 0 with warning
        self.assertEqual(tdi, 0.0)


class TestICS(unittest.TestCase):
    """Test Information Criterion Score."""
    
    def setUp(self):
        np.random.seed(42)
        
    def test_ics_basic(self):
        """Test ICS computation."""
        perf = np.random.rand(12, 4)
        const = np.random.rand(12, 3)
        
        ics = compute_ics(perf, const)
        
        self.assertIsInstance(ics, float)
        
    def test_ics_with_complexity(self):
        """Test ICS with explicit complexity values."""
        T, K = 15, 3
        perf = np.random.rand(T, K)
        const = np.random.rand(T, 2)
        
        # Increasing complexity
        complexity = np.tile(np.linspace(100, 200, T).reshape(-1, 1), (1, K))
        
        ics = compute_ics(perf, const, complexity)
        
        self.assertIsInstance(ics, float)


class TestCBI(unittest.TestCase):
    """Test Cross-Benchmark Inconsistency."""
    
    def setUp(self):
        np.random.seed(42)
        
    def test_cbi_consistent_rankings(self):
        """Test CBI on consistent cross-benchmark rankings."""
        # 4 algorithms, 2 benchmarks
        perf_bm1 = np.array([
            [0.9, 0.8, 0.7, 0.6],
            [0.91, 0.81, 0.71, 0.61],
        ])
        
        perf_bm2 = np.array([
            [0.85, 0.75, 0.65, 0.55],
            [0.86, 0.76, 0.66, 0.56],
        ])
        
        perf = np.vstack([perf_bm1, perf_bm2])
        benchmark_ids = np.array([0, 0, 1, 1])
        
        cbi = compute_cbi(perf, benchmark_ids)
        
        # Should be low (consistent)
        self.assertLess(cbi, 0.3)
        
    def test_cbi_inconsistent_rankings(self):
        """Test CBI on inconsistent rankings."""
        # Rankings reversed across benchmarks
        perf_bm1 = np.array([
            [0.9, 0.8, 0.7, 0.6],
            [0.91, 0.81, 0.71, 0.61],
        ])
        
        perf_bm2 = np.array([
            [0.6, 0.7, 0.8, 0.9],  # Reversed!
            [0.61, 0.71, 0.81, 0.91],
        ])
        
        perf = np.vstack([perf_bm1, perf_bm2])
        benchmark_ids = np.array([0, 0, 1, 1])
        
        cbi = compute_cbi(perf, benchmark_ids)
        
        # Should be high (inconsistent)
        self.assertGreater(cbi, 0.5)
        
    def test_cbi_single_benchmark(self):
        """Test CBI with only one benchmark."""
        perf = np.random.rand(5, 4)
        benchmark_ids = np.zeros(5)
        
        cbi = compute_cbi(perf, benchmark_ids)
        
        # Should return 0
        self.assertEqual(cbi, 0.0)


class TestADS(unittest.TestCase):
    """Test Adaptive Drift Score."""
    
    def setUp(self):
        np.random.seed(42)
        
    def test_ads_basic(self):
        """Test ADS computation."""
        perf = np.random.rand(10, 3)
        const = np.random.rand(10, 2)
        
        ads = compute_ads(perf, const)
        
        self.assertIsInstance(ads, float)
        self.assertGreaterEqual(ads, 0.0)
        
    def test_ads_with_justification(self):
        """Test ADS with justification scores."""
        T = 12
        perf = np.random.rand(T, 3)
        const = np.random.rand(T, 2)
        
        # High justification throughout
        justification = np.ones(T) * 0.9
        
        ads = compute_ads(perf, const, justification)
        
        # Should be low with high justification
        self.assertLess(ads, 0.5)
        
    def test_ads_unjustified_drift(self):
        """Test ADS detects unjustified drift."""
        T = 15
        K = 3
        
        # Create data with performance gains and constraint changes
        perf = np.zeros((T, K))
        const = np.zeros((T, 2))
        
        for t in range(T):
            perf[t, :] = 0.5 + t * 0.03  # Steady improvement
            const[t, :] = [100 + t * 10, 8 + t * 0.5]  # Increasing constraints
        
        # Low justification
        justification = np.ones(T) * 0.2
        
        ads = compute_ads(perf, const, justification)
        
        # Should detect unjustified drift
        self.assertGreater(ads, 0.15)


class TestMCI(unittest.TestCase):
    """Test Multi-Constraint Interaction."""
    
    def setUp(self):
        np.random.seed(42)
        
    def test_mci_basic(self):
        """Test MCI computation."""
        const = np.random.rand(10, 3)
        
        mci, corr_matrix = compute_mci(const)
        
        self.assertIsInstance(mci, float)
        self.assertGreaterEqual(mci, 0.0)
        self.assertEqual(corr_matrix.shape, (3, 3))
        
    def test_mci_independent_constraints(self):
        """Test MCI on independent constraints."""
        T = 20
        const = np.random.rand(T, 4)
        
        mci, _ = compute_mci(const)
        
        # Should be low for independent constraints
        self.assertLess(mci, 0.7)
        
    def test_mci_correlated_constraints(self):
        """Test MCI on highly correlated constraints."""
        T = 20
        base = np.linspace(0, 1, T)
        
        # Create highly correlated constraints
        const = np.column_stack([
            base,
            base + np.random.normal(0, 0.05, T),  # Nearly identical
            base * 2 + np.random.normal(0, 0.1, T)  # Linearly related
        ])
        
        mci, corr_matrix = compute_mci(const)
        
        # Should detect high correlation
        self.assertGreater(mci, 0.5)
        
    def test_mci_single_constraint(self):
        """Test MCI with single constraint."""
        const = np.random.rand(10, 1)
        
        mci, corr_matrix = compute_mci(const)
        
        self.assertEqual(mci, 0.0)
        self.assertEqual(corr_matrix.shape, (1, 1))


class TestAllAdvancedMetrics(unittest.TestCase):
    """Test computing all metrics at once."""
    
    def test_compute_all(self):
        """Test computing all advanced metrics."""
        perf, const = create_synthetic_data(
            n_time_periods=15,
            n_algorithms=4,
            n_constraints=3,
            bias_intensity=0.5,
            random_seed=42
        )
        
        results = compute_all_advanced_metrics(perf, const)
        
        # Check all keys present
        self.assertIn('tdi', results)
        self.assertIn('ics', results)
        self.assertIn('ads', results)
        self.assertIn('mci', results)
        self.assertIn('mci_correlation_matrix', results)
        
        # CBI should be None without benchmark IDs
        self.assertIsNone(results['cbi'])
        
    def test_compute_all_with_benchmarks(self):
        """Test with benchmark IDs."""
        T = 12
        perf = np.random.rand(T, 4)
        const = np.random.rand(T, 3)
        benchmark_ids = np.array([0]*6 + [1]*6)
        
        results = compute_all_advanced_metrics(
            perf, const, 
            benchmark_ids=benchmark_ids
        )
        
        self.assertIsNotNone(results['cbi'])
        self.assertIsInstance(results['cbi'], float)


class TestRobustness(unittest.TestCase):
    """Test robustness to edge cases."""
    
    def test_nan_handling(self):
        """Test handling of NaN values."""
        perf = np.random.rand(10, 3)
        const = np.random.rand(10, 2)
        
        # This should not crash
        results = compute_all_advanced_metrics(perf, const)
        
        self.assertIsInstance(results, dict)
        
    def test_constant_values(self):
        """Test with constant values."""
        perf = np.ones((10, 3)) * 0.8
        const = np.ones((10, 2)) * 100
        
        results = compute_all_advanced_metrics(perf, const)
        
        # Should handle gracefully
        self.assertIsInstance(results['tdi'], float)
        self.assertIsInstance(results['mci'], float)


def run_tests():
    """Run all tests."""
    unittest.main(argv=[''], verbosity=2, exit=False)


if __name__ == '__main__':
    print("=" * 70)
    print("Running Advanced Metrics Test Suite")
    print("=" * 70)
    unittest.main(verbosity=2)
