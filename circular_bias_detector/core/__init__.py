"""
Core submodule for circular bias detection.

This submodule contains the fundamental algorithms split into logical components:
- metrics: PSI, CCS, ρ_PC computation
- matrix: Matrix operations and transformations
- validation: Input validation and error checking
- bootstrap: Statistical bootstrap methods
"""

from .metrics import (
    compute_psi,
    compute_ccs,
    compute_rho_pc,
    compute_all_indicators,
    detect_bias_threshold
)

from .bootstrap import (
    bootstrap_psi,
    bootstrap_ccs,
    bootstrap_rho_pc,
    compute_adaptive_thresholds
)

from .matrix import (
    validate_matrices,
    prepare_performance_matrix,
    prepare_constraint_matrix
)

__all__ = [
    # Metrics
    'compute_psi',
    'compute_ccs',
    'compute_rho_pc',
    'compute_all_indicators',
    'detect_bias_threshold',
    # Bootstrap
    'bootstrap_psi',
    'bootstrap_ccs',
    'bootstrap_rho_pc',
    'compute_adaptive_thresholds',
    # Matrix operations
    'validate_matrices',
    'prepare_performance_matrix',
    'prepare_constraint_matrix',
]
