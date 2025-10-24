"""
Abstract base interface for LLM inference backends.

This module defines the common interface that all LLM backends must implement,
enabling easy switching between different inference engines (vLLM, TensorRT-LLM, SGLang).
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
import numpy as np


@dataclass
class LLMOutput:
    """
    Standardized output from LLM generation.
    
    Attributes
    ----------
    text : str
        Generated text output
    prompt : str
        Original prompt used for generation
    metadata : dict
        Additional metadata (tokens, latency, etc.)
    performance_score : float, optional
        Computed performance score (e.g., perplexity, coherence)
    """
    text: str
    prompt: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    performance_score: Optional[float] = None
    
    def __repr__(self) -> str:
        return f"LLMOutput(text='{self.text[:50]}...', score={self.performance_score})"


class InferenceBackend(ABC):
    """
    Abstract base class for LLM inference backends.
    
    All backend implementations (vLLM, TensorRT-LLM, SGLang) must implement
    this interface to ensure compatibility with the bias detection framework.
    """
    
    def __init__(self, model: str, **kwargs):
        """
        Initialize the inference backend.
        
        Parameters
        ----------
        model : str
            Model name or path (e.g., "meta-llama/Llama-2-7b-hf")
        **kwargs
            Backend-specific configuration options
        """
        self.model = model
        self.config = kwargs
        self._initialized = False
    
    @abstractmethod
    def initialize(self) -> None:
        """
        Initialize the backend (load model, allocate resources).
        
        This method should be called before generation. It handles:
        - Model loading
        - GPU memory allocation
        - Backend-specific setup
        """
        pass
    
    @abstractmethod
    def generate(self, 
                 prompts: List[str],
                 constraints: Optional[Dict[str, Any]] = None,
                 **kwargs) -> List[LLMOutput]:
        """
        Generate outputs for a batch of prompts.
        
        Parameters
        ----------
        prompts : List[str]
            List of input prompts
        constraints : dict, optional
            Generation constraints (temperature, max_tokens, etc.)
        **kwargs
            Additional generation parameters
            
        Returns
        -------
        List[LLMOutput]
            Generated outputs with metadata
            
        Examples
        --------
        >>> backend = SomeBackend(model="llama2")
        >>> outputs = backend.generate(
        ...     prompts=["Hello, world!"],
        ...     constraints={"temperature": 0.7, "max_tokens": 100}
        ... )
        """
        pass
    
    @abstractmethod
    def compute_performance_score(self, output: LLMOutput) -> float:
        """
        Compute performance score for a generated output.
        
        Parameters
        ----------
        output : LLMOutput
            Generated output to score
            
        Returns
        -------
        float
            Performance score (higher is better)
            
        Notes
        -----
        This can be perplexity, coherence score, task-specific metric, etc.
        """
        pass
    
    def generate_batch(self,
                      prompts: List[str],
                      constraints: Optional[Dict[str, Any]] = None,
                      batch_size: int = 32,
                      **kwargs) -> List[LLMOutput]:
        """
        Generate outputs in batches for efficiency.
        
        Parameters
        ----------
        prompts : List[str]
            List of prompts to process
        constraints : dict, optional
            Generation constraints
        batch_size : int, default=32
            Batch size for processing
        **kwargs
            Additional parameters
            
        Returns
        -------
        List[LLMOutput]
            All generated outputs
        """
        if not self._initialized:
            self.initialize()
        
        all_outputs = []
        
        for i in range(0, len(prompts), batch_size):
            batch_prompts = prompts[i:i + batch_size]
            batch_outputs = self.generate(batch_prompts, constraints, **kwargs)
            all_outputs.extend(batch_outputs)
        
        return all_outputs
    
    def shutdown(self) -> None:
        """
        Clean up resources (optional, for backends that need explicit cleanup).
        """
        pass
    
    def __enter__(self):
        """Context manager entry."""
        self.initialize()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.shutdown()
        return False


class MockBackend(InferenceBackend):
    """
    Mock backend for testing without actual LLM inference.
    
    Useful for:
    - Unit tests
    - Development without GPU
    - CI/CD pipelines
    """
    
    def __init__(self, model: str = "mock-model", **kwargs):
        super().__init__(model, **kwargs)
        self.generation_count = 0
    
    def initialize(self) -> None:
        """Initialize mock backend (no-op)."""
        self._initialized = True
    
    def generate(self,
                 prompts: List[str],
                 constraints: Optional[Dict[str, Any]] = None,
                 **kwargs) -> List[LLMOutput]:
        """Generate mock outputs."""
        self.generation_count += len(prompts)
        
        outputs = []
        for prompt in prompts:
            # Generate deterministic mock output
            mock_text = f"Mock response to: {prompt[:30]}..."
            mock_score = 0.8 + 0.1 * np.random.rand()  # Random score 0.8-0.9
            
            output = LLMOutput(
                text=mock_text,
                prompt=prompt,
                metadata={
                    'backend': 'mock',
                    'constraints': constraints or {},
                    'generation_index': self.generation_count
                },
                performance_score=mock_score
            )
            outputs.append(output)
        
        return outputs
    
    def compute_performance_score(self, output: LLMOutput) -> float:
        """Return pre-computed mock score."""
        return output.performance_score or 0.85
