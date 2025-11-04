"""
Pytest configuration and shared fixtures.

This module provides common test fixtures and configuration
for the entire test suite.
"""

import numpy as np
import pytest

from circular_bias_detector.config import BiasDetectionConfig
from circular_bias_detector.logging import disable_logging, enable_logging


@pytest.fixture(scope="session", autouse=True)
def configure_test_environment():
    """Configure test environment (disable logging, set random seed)."""
    # Disable logging during tests to reduce noise
    disable_logging()
    
    # Set numpy random seed for reproducibility
    np.random.seed(42)
    
    yield
    
    # Re-enable logging after tests
    enable_logging()


@pytest.fixture
def default_config():
    """Provide default configuration for tests."""
    return BiasDetectionConfig()


@pytest.fixture
def strict_config():
    """Provide strict configuration with lower thresholds."""
    return BiasDetectionConfig(
        psi_threshold=0.10,
        ccs_threshold=0.90,
        rho_pc_threshold=0.40,
    )


@pytest.fixture
def simple_performance_matrix():
    """
    Provide a simple 3x2 performance matrix.
    
    Returns
    -------
    np.ndarray
        Shape (3, 2): 3 time periods, 2 algorithms
    """
    return np.array([
        [0.85, 0.78],
        [0.87, 0.80],
        [0.91, 0.84]
    ])


@pytest.fixture
def simple_constraint_matrix():
    """
    Provide a simple 3x2 constraint matrix.
    
    Returns
    -------
    np.ndarray
        Shape (3, 2): 3 time periods, 2 constraints
    """
    return np.array([
        [512, 0.7],
        [550, 0.75],
        [600, 0.8]
    ])


@pytest.fixture
def biased_performance_matrix():
    """
    Provide a performance matrix with clear circular bias.
    
    Performance increases monotonically with time, suggesting
    iterative optimization.
    
    Returns
    -------
    np.ndarray
        Shape (5, 3): 5 time periods, 3 algorithms
    """
    return np.array([
        [0.70, 0.68, 0.65],
        [0.75, 0.72, 0.70],
        [0.80, 0.77, 0.75],
        [0.85, 0.82, 0.80],
        [0.90, 0.87, 0.85]
    ])


@pytest.fixture
def biased_constraint_matrix():
    """
    Provide a constraint matrix with inconsistent values.
    
    Constraints vary significantly across time periods.
    
    Returns
    -------
    np.ndarray
        Shape (5, 2): 5 time periods, 2 constraints
    """
    return np.array([
        [100, 1.0],
        [200, 1.5],
        [300, 2.0],
        [400, 2.5],
        [500, 3.0]
    ])


@pytest.fixture
def clean_performance_matrix():
    """
    Provide a performance matrix without bias.
    
    Performance is relatively stable with random variation.
    
    Returns
    -------
    np.ndarray
        Shape (5, 3): 5 time periods, 3 algorithms
    """
    np.random.seed(42)
    base = np.array([0.80, 0.75, 0.78])
    noise = np.random.normal(0, 0.02, (5, 3))
    return base + noise


@pytest.fixture
def clean_constraint_matrix():
    """
    Provide a constraint matrix with consistent values.
    
    Constraints remain stable across time periods.
    
    Returns
    -------
    np.ndarray
        Shape (5, 2): 5 time periods, 2 constraints
    """
    return np.array([
        [512, 8.0],
        [512, 8.0],
        [512, 8.0],
        [512, 8.0],
        [512, 8.0]
    ])


@pytest.fixture
def large_performance_matrix():
    """
    Provide a large performance matrix for stress testing.
    
    Returns
    -------
    np.ndarray
        Shape (20, 10): 20 time periods, 10 algorithms
    """
    np.random.seed(42)
    return np.random.uniform(0.6, 0.95, (20, 10))


@pytest.fixture
def large_constraint_matrix():
    """
    Provide a large constraint matrix for stress testing.
    
    Returns
    -------
    np.ndarray
        Shape (20, 5): 20 time periods, 5 constraints
    """
    np.random.seed(42)
    return np.random.uniform(100, 1000, (20, 5))


@pytest.fixture
def algorithm_names():
    """Provide a list of algorithm names."""
    return ["ModelA", "ModelB", "ModelC"]


@pytest.fixture
def invalid_matrix():
    """Provide an invalid matrix (contains NaN/Inf)."""
    return np.array([
        [0.8, np.nan],
        [0.85, 0.9],
        [np.inf, 0.88]
    ])


# Markers for test categorization
def pytest_configure(config):
    """Configure custom pytest markers."""
    config.addinivalue_line("markers", "unit: mark test as a unit test")
    config.addinivalue_line("markers", "integration: mark test as an integration test")
    config.addinivalue_line("markers", "slow: mark test as slow running")
