"""
Circular Bias Detection CLI
Command-line interface for detecting circular reasoning bias in algorithm evaluation.
"""

__version__ = "1.0.0"

from .main import CircularBiasCLI, main

__all__ = ['CircularBiasCLI', 'main']
