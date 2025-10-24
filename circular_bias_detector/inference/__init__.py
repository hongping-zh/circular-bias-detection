"""
LLM inference integration for real-time bias detection.

This submodule provides:
- Abstract base interface for LLM backends
- vLLM backend implementation
- Mock backend for testing
- Utilities for prompt generation and output processing
"""

from .base import InferenceBackend, LLMOutput, MockBackend
from .backends.vllm_backend import VLLMBackend

__all__ = [
    'InferenceBackend',
    'LLMOutput',
    'MockBackend',
    'VLLMBackend',
]
