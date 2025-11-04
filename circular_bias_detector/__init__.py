"""
Circular Reasoning Bias Detection Framework

A comprehensive statistical framework for detecting circular reasoning bias 
in AI algorithm evaluation.

New in v1.2:
- Unified configuration management (config.py)
- Centralized logging system (logging.py)
- Custom exception hierarchy (exceptions.py)
- Modern dependency management (pyproject.toml)
- Code quality tools (black, flake8, mypy, pre-commit)
- Enhanced testing infrastructure with 80%+ coverage target

Previous (v1.1):
- Modular code structure with core/, inference/ submodules
- LLM inference integration (vLLM backend)
- Real-time bias detection during generation
"""

__version__ = "1.2.0"
__author__ = "Hongping Zhang"
__email__ = "yujjam@uest.edu.gr"

# Configuration and utilities
from .config import BiasDetectionConfig, get_config, set_config
from .logging import setup_logger, get_logger
from . import exceptions

# Core metrics (backward compatible - now from core.metrics)
from .core.metrics import (
    compute_psi, 
    compute_ccs, 
    compute_rho_pc,
    compute_all_indicators,
    detect_bias_threshold
)

# Bootstrap methods
from .core.bootstrap import (
    bootstrap_psi,
    bootstrap_ccs,
    bootstrap_rho_pc,
    compute_adaptive_thresholds
)

# Matrix operations
from .core.matrix import (
    validate_matrices,
    prepare_performance_matrix,
    prepare_constraint_matrix
)

# Main detector class
from .detection import BiasDetector

# Utilities (backward compatible)
from .utils import load_data, generate_report

# New: Inference capabilities (optional, requires vLLM)
try:
    from .inference import (
        InferenceBackend,
        VLLMBackend,
        MockBackend,
        LLMOutput
    )
    from .inference.detector import BiasDetectorWithInference
    _INFERENCE_AVAILABLE = True
except ImportError:
    _INFERENCE_AVAILABLE = False
    InferenceBackend = None
    VLLMBackend = None
    MockBackend = None
    LLMOutput = None
    BiasDetectorWithInference = None

__all__ = [
    # Configuration and logging
    'BiasDetectionConfig',
    'get_config',
    'set_config',
    'setup_logger',
    'get_logger',
    'exceptions',
    
    # Core metrics
    'compute_psi',
    'compute_ccs', 
    'compute_rho_pc',
    'compute_all_indicators',
    'detect_bias_threshold',
    
    # Bootstrap methods
    'bootstrap_psi',
    'bootstrap_ccs',
    'bootstrap_rho_pc',
    'compute_adaptive_thresholds',
    
    # Matrix operations
    'validate_matrices',
    'prepare_performance_matrix',
    'prepare_constraint_matrix',
    
    # Main detector
    'BiasDetector',
    
    # Utilities
    'load_data',
    'generate_report',
    
    # Inference (if available)
    'InferenceBackend',
    'VLLMBackend',
    'MockBackend',
    'LLMOutput',
    'BiasDetectorWithInference',
]
