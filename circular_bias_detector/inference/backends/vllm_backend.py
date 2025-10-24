"""
vLLM backend implementation for high-throughput LLM inference.

This backend leverages vLLM's optimizations:
- PagedAttention for memory efficiency
- Continuous batching for high throughput
- Optimized CUDA kernels
"""

from typing import List, Dict, Optional, Any
import warnings
import numpy as np

from ..base import InferenceBackend, LLMOutput


class VLLMBackend(InferenceBackend):
    """
    vLLM-based inference backend with high throughput optimizations.
    
    Features:
    - Automatic batch processing
    - Memory-efficient attention
    - Support for various sampling parameters
    
    Parameters
    ----------
    model : str
        HuggingFace model name or path
    tensor_parallel_size : int, default=1
        Number of GPUs for tensor parallelism
    trust_remote_code : bool, default=False
        Whether to trust remote code in model
    dtype : str, default="auto"
        Model dtype (auto, float16, bfloat16, float32)
    max_model_len : int, optional
        Maximum model context length
    gpu_memory_utilization : float, default=0.9
        Fraction of GPU memory to use
    **kwargs
        Additional vLLM engine arguments
        
    Examples
    --------
    >>> backend = VLLMBackend(model="meta-llama/Llama-2-7b-hf")
    >>> outputs = backend.generate(
    ...     prompts=["Explain bias detection"],
    ...     constraints={"temperature": 0.7, "max_tokens": 100}
    ... )
    """
    
    def __init__(self,
                 model: str,
                 tensor_parallel_size: int = 1,
                 trust_remote_code: bool = False,
                 dtype: str = "auto",
                 max_model_len: Optional[int] = None,
                 gpu_memory_utilization: float = 0.9,
                 **kwargs):
        super().__init__(model, **kwargs)
        
        self.tensor_parallel_size = tensor_parallel_size
        self.trust_remote_code = trust_remote_code
        self.dtype = dtype
        self.max_model_len = max_model_len
        self.gpu_memory_utilization = gpu_memory_utilization
        
        self.llm = None
        self.tokenizer = None
    
    def initialize(self) -> None:
        """
        Initialize vLLM engine and load model.
        
        Raises
        ------
        ImportError
            If vLLM is not installed
        RuntimeError
            If model loading fails
        """
        if self._initialized:
            return
        
        try:
            from vllm import LLM
        except ImportError:
            raise ImportError(
                "vLLM is not installed. Install with: pip install vllm\n"
                "For more information: https://docs.vllm.ai/"
            )
        
        try:
            # Initialize vLLM engine
            self.llm = LLM(
                model=self.model,
                tensor_parallel_size=self.tensor_parallel_size,
                trust_remote_code=self.trust_remote_code,
                dtype=self.dtype,
                max_model_len=self.max_model_len,
                gpu_memory_utilization=self.gpu_memory_utilization,
                **self.config
            )
            
            self._initialized = True
            print(f"✓ vLLM backend initialized: {self.model}")
            
        except Exception as e:
            raise RuntimeError(f"Failed to initialize vLLM backend: {e}")
    
    def generate(self,
                 prompts: List[str],
                 constraints: Optional[Dict[str, Any]] = None,
                 **kwargs) -> List[LLMOutput]:
        """
        Generate outputs using vLLM engine.
        
        Parameters
        ----------
        prompts : List[str]
            Input prompts
        constraints : dict, optional
            Sampling parameters:
            - temperature: float (default 0.7)
            - max_tokens: int (default 512)
            - top_p: float (default 1.0)
            - top_k: int (default -1, disabled)
            - frequency_penalty: float (default 0.0)
            - presence_penalty: float (default 0.0)
        **kwargs
            Additional vLLM sampling parameters
            
        Returns
        -------
        List[LLMOutput]
            Generated outputs with metadata
        """
        if not self._initialized:
            self.initialize()
        
        try:
            from vllm import SamplingParams
        except ImportError:
            raise ImportError("vLLM is required for this backend")
        
        # Prepare sampling parameters
        default_constraints = {
            'temperature': 0.7,
            'max_tokens': 512,
            'top_p': 1.0,
            'top_k': -1,
        }
        
        if constraints:
            default_constraints.update(constraints)
        
        # Map constraint names to vLLM parameter names
        sampling_params = SamplingParams(
            temperature=default_constraints.get('temperature', 0.7),
            max_tokens=default_constraints.get('max_tokens', 512),
            top_p=default_constraints.get('top_p', 1.0),
            top_k=default_constraints.get('top_k', -1),
            frequency_penalty=default_constraints.get('frequency_penalty', 0.0),
            presence_penalty=default_constraints.get('presence_penalty', 0.0),
            **kwargs
        )
        
        # Generate outputs
        vllm_outputs = self.llm.generate(prompts, sampling_params)
        
        # Convert to LLMOutput format
        outputs = []
        for vllm_out, prompt in zip(vllm_outputs, prompts):
            # Extract generated text (vLLM returns list of outputs per prompt)
            generated_text = vllm_out.outputs[0].text
            
            # Compute performance score
            performance_score = self._compute_score_from_vllm_output(vllm_out)
            
            output = LLMOutput(
                text=generated_text,
                prompt=prompt,
                metadata={
                    'backend': 'vllm',
                    'model': self.model,
                    'constraints': default_constraints,
                    'num_tokens': len(vllm_out.outputs[0].token_ids),
                    'finish_reason': vllm_out.outputs[0].finish_reason,
                    'cumulative_logprob': vllm_out.outputs[0].cumulative_logprob,
                },
                performance_score=performance_score
            )
            outputs.append(output)
        
        return outputs
    
    def _compute_score_from_vllm_output(self, vllm_output) -> float:
        """
        Compute performance score from vLLM output.
        
        Uses negative normalized log-probability as a proxy for quality.
        Higher score = better (more confident) generation.
        """
        try:
            # Extract cumulative log probability
            logprob = vllm_output.outputs[0].cumulative_logprob
            num_tokens = len(vllm_output.outputs[0].token_ids)
            
            if num_tokens > 0:
                # Normalize by length and convert to [0, 1] range
                # Typical logprobs are negative, so we negate and normalize
                avg_logprob = logprob / num_tokens
                
                # Map to [0, 1] using sigmoid-like transform
                # More negative logprob -> lower score
                score = 1.0 / (1.0 + np.exp(-avg_logprob))
                return float(score)
            else:
                return 0.5  # Default for empty output
                
        except Exception as e:
            warnings.warn(f"Failed to compute performance score: {e}")
            return 0.5  # Default fallback
    
    def compute_performance_score(self, output: LLMOutput) -> float:
        """
        Compute performance score for an already-generated output.
        
        Parameters
        ----------
        output : LLMOutput
            Generated output
            
        Returns
        -------
        float
            Performance score [0, 1]
        """
        if output.performance_score is not None:
            return output.performance_score
        
        # If score not pre-computed, use metadata
        if 'cumulative_logprob' in output.metadata and 'num_tokens' in output.metadata:
            logprob = output.metadata['cumulative_logprob']
            num_tokens = output.metadata['num_tokens']
            
            if num_tokens > 0:
                avg_logprob = logprob / num_tokens
                score = 1.0 / (1.0 + np.exp(-avg_logprob))
                return float(score)
        
        # Fallback: simple heuristic based on text length
        return min(len(output.text) / 100.0, 1.0)
    
    def shutdown(self) -> None:
        """
        Clean up vLLM resources.
        """
        if self.llm is not None:
            # vLLM handles cleanup automatically, but we can explicitly delete
            del self.llm
            self.llm = None
            self._initialized = False
            print("✓ vLLM backend shut down")


def create_vllm_backend(model_name: str = "meta-llama/Llama-2-7b-hf",
                       gpu_count: int = 1,
                       **kwargs) -> VLLMBackend:
    """
    Convenience function to create and initialize a vLLM backend.
    
    Parameters
    ----------
    model_name : str, default="meta-llama/Llama-2-7b-hf"
        HuggingFace model to use
    gpu_count : int, default=1
        Number of GPUs for tensor parallelism
    **kwargs
        Additional backend configuration
        
    Returns
    -------
    VLLMBackend
        Initialized backend ready for generation
        
    Examples
    --------
    >>> backend = create_vllm_backend("meta-llama/Llama-2-7b-hf", gpu_count=1)
    >>> outputs = backend.generate(["Hello!"])
    """
    backend = VLLMBackend(
        model=model_name,
        tensor_parallel_size=gpu_count,
        **kwargs
    )
    backend.initialize()
    return backend
