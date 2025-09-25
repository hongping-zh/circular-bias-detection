"""
Circular Reasoning Bias Detection Framework

A comprehensive statistical framework for detecting circular reasoning bias 
in AI algorithm evaluation.
"""

__version__ = "1.0.0"
__author__ = "Hongping Zhang"
__email__ = "contact@github"

from .core import compute_psi, compute_ccs, compute_rho_pc
from .detection import BiasDetector
from .utils import load_data, validate_matrices, generate_report

__all__ = [
    'compute_psi',
    'compute_ccs', 
    'compute_rho_pc',
    'BiasDetector',
    'load_data',
    'validate_matrices',
    'generate_report'
]
