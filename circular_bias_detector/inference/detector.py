"""
BiasDetector with integrated LLM inference capabilities.

This module extends the base BiasDetector to support real-time bias detection
during LLM generation, enabling end-to-end automated auditing.
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Optional, Union, Any
import warnings

from ..detection import BiasDetector
from ..core.matrix import prepare_performance_matrix, prepare_constraint_matrix
from .base import InferenceBackend, LLMOutput


class BiasDetectorWithInference(BiasDetector):
    """
    BiasDetector with integrated LLM inference for real-time auditing.
    
    This class combines:
    - LLM inference (via configurable backends)
    - Automatic performance scoring
    - Real-time bias detection
    - Matrix construction from generation logs
    
    Parameters
    ----------
    backend : InferenceBackend
        LLM inference backend (vLLM, TensorRT-LLM, etc.)
    psi_threshold : float, default=0.1
        PSI detection threshold
    ccs_threshold : float, default=0.8
        CCS detection threshold
    rho_pc_threshold : float, default=0.3
        ρ_PC detection threshold
    auto_score : bool, default=True
        Automatically compute performance scores from LLM outputs
        
    Examples
    --------
    >>> from circular_bias_detector.inference import VLLMBackend
    >>> backend = VLLMBackend(model="meta-llama/Llama-2-7b-hf")
    >>> detector = BiasDetectorWithInference(backend=backend)
    >>> 
    >>> # Run bias detection on generated outputs
    >>> results = detector.detect_from_prompts(
    ...     prompts=["Explain AI ethics"] * 10,
    ...     constraints={'temperature': 0.7, 'max_tokens': 100}
    ... )
    >>> print(f"Bias detected: {results['overall_bias']}")
    """
    
    def __init__(self,
                 backend: InferenceBackend,
                 psi_threshold: float = 0.1,
                 ccs_threshold: float = 0.8,
                 rho_pc_threshold: float = 0.3,
                 auto_score: bool = True):
        super().__init__(
            psi_threshold=psi_threshold,
            ccs_threshold=ccs_threshold,
            rho_pc_threshold=rho_pc_threshold
        )
        
        self.backend = backend
        self.auto_score = auto_score
        
        # Storage for generation history
        self.generation_history: List[LLMOutput] = []
        self.constraint_history: List[Dict[str, Any]] = []
    
    def detect_from_prompts(self,
                           prompts: List[str],
                           constraints: Optional[Dict[str, Any]] = None,
                           time_periods: Optional[int] = None,
                           enable_bootstrap: bool = False,
                           n_bootstrap: int = 1000,
                           **kwargs) -> Dict:
        """
        Perform bias detection by generating LLM outputs and analyzing them.
        
        This is the main method for end-to-end bias detection:
        1. Generate outputs using the LLM backend
        2. Compute performance scores
        3. Construct performance and constraint matrices
        4. Run bias detection algorithms
        
        Parameters
        ----------
        prompts : List[str]
            Input prompts for LLM generation
        constraints : dict, optional
            Generation constraints (temperature, max_tokens, etc.)
        time_periods : int, optional
            Number of time periods to simulate (default: len(prompts) // 3)
            Prompts are grouped into time periods for temporal analysis
        enable_bootstrap : bool, default=False
            Compute bootstrap confidence intervals
        n_bootstrap : int, default=1000
            Number of bootstrap samples
        **kwargs
            Additional parameters for generation
            
        Returns
        -------
        dict
            Comprehensive bias detection results including:
            - Standard metrics (PSI, CCS, ρ_PC)
            - Bias detection decisions
            - Generation metadata
            - LLM outputs (optionally)
            
        Examples
        --------
        >>> results = detector.detect_from_prompts(
        ...     prompts=["Analyze this"] * 12,
        ...     constraints={'temperature': 0.7},
        ...     time_periods=4
        ... )
        """
        if not prompts:
            raise ValueError("Prompts list cannot be empty")
        
        # Initialize backend if needed
        if not self.backend._initialized:
            self.backend.initialize()
        
        # Set default time periods
        if time_periods is None:
            time_periods = max(len(prompts) // 3, 2)  # At least 2 periods
        
        if len(prompts) < time_periods:
            raise ValueError(
                f"Need at least {time_periods} prompts for {time_periods} time periods"
            )
        
        # Generate outputs
        print(f"Generating outputs for {len(prompts)} prompts...")
        outputs = self.backend.generate(prompts, constraints, **kwargs)
        
        # Store in history
        self.generation_history.extend(outputs)
        self.constraint_history.extend([constraints or {}] * len(outputs))
        
        # Compute performance scores if needed
        if self.auto_score:
            for output in outputs:
                if output.performance_score is None:
                    output.performance_score = self.backend.compute_performance_score(output)
        
        # Construct matrices
        perf_matrix, const_matrix = self._construct_matrices_from_outputs(
            outputs, 
            constraints, 
            time_periods
        )
        
        print(f"Constructed matrices: performance {perf_matrix.shape}, constraints {const_matrix.shape}")
        
        # Run standard bias detection
        results = self.detect_bias(
            performance_matrix=perf_matrix,
            constraint_matrix=const_matrix,
            enable_bootstrap=enable_bootstrap,
            n_bootstrap=n_bootstrap
        )
        
        # Add inference metadata
        results['inference_metadata'] = {
            'backend': self.backend.__class__.__name__,
            'model': self.backend.model,
            'num_prompts': len(prompts),
            'time_periods': time_periods,
            'prompts_per_period': len(prompts) // time_periods,
            'constraints': constraints or {}
        }
        
        return results
    
    def _construct_matrices_from_outputs(self,
                                        outputs: List[LLMOutput],
                                        constraints: Optional[Dict[str, Any]],
                                        time_periods: int) -> tuple:
        """
        Construct performance and constraint matrices from LLM outputs.
        
        Parameters
        ----------
        outputs : List[LLMOutput]
            Generated outputs
        constraints : dict, optional
            Constraints used for generation
        time_periods : int
            Number of time periods for analysis
            
        Returns
        -------
        tuple
            (performance_matrix, constraint_matrix)
        """
        # Group outputs by time period
        period_size = len(outputs) // time_periods
        
        perf_scores = []
        const_values = []
        
        for t in range(time_periods):
            start_idx = t * period_size
            end_idx = start_idx + period_size if t < time_periods - 1 else len(outputs)
            
            period_outputs = outputs[start_idx:end_idx]
            
            # Aggregate performance scores for this period
            period_scores = [out.performance_score for out in period_outputs 
                           if out.performance_score is not None]
            
            if not period_scores:
                warnings.warn(f"No valid performance scores for time period {t}")
                period_scores = [0.5]  # Default
            
            perf_scores.append(np.mean(period_scores))
            
            # Extract constraint values
            # If constraints vary, extract from metadata; otherwise use input
            if constraints:
                const_values.append(list(constraints.values()))
            else:
                # Try to extract from output metadata
                meta_constraints = period_outputs[0].metadata.get('constraints', {})
                const_values.append(list(meta_constraints.values()) or [0.7, 512])
        
        # Convert to numpy arrays
        perf_matrix = np.array(perf_scores).reshape(-1, 1)  # Single "algorithm"
        const_matrix = np.array(const_values)
        
        # Ensure 2D
        if const_matrix.ndim == 1:
            const_matrix = const_matrix.reshape(-1, 1)
        
        return perf_matrix, const_matrix
    
    def detect_from_history(self,
                           time_periods: Optional[int] = None,
                           enable_bootstrap: bool = False) -> Dict:
        """
        Run bias detection on accumulated generation history.
        
        Useful for analyzing multiple generation sessions over time.
        
        Parameters
        ----------
        time_periods : int, optional
            Number of time periods to divide history into
        enable_bootstrap : bool, default=False
            Compute bootstrap confidence intervals
            
        Returns
        -------
        dict
            Bias detection results
            
        Examples
        --------
        >>> # Generate multiple batches
        >>> detector.detect_from_prompts(prompts_batch1, constraints1)
        >>> detector.detect_from_prompts(prompts_batch2, constraints2)
        >>> 
        >>> # Analyze accumulated history
        >>> results = detector.detect_from_history(time_periods=10)
        """
        if not self.generation_history:
            raise ValueError("No generation history available. Generate outputs first.")
        
        if time_periods is None:
            time_periods = max(len(self.generation_history) // 5, 2)
        
        # Use first constraint set as template
        constraints = self.constraint_history[0] if self.constraint_history else {}
        
        perf_matrix, const_matrix = self._construct_matrices_from_outputs(
            self.generation_history,
            constraints,
            time_periods
        )
        
        return self.detect_bias(
            performance_matrix=perf_matrix,
            constraint_matrix=const_matrix,
            enable_bootstrap=enable_bootstrap
        )
    
    def clear_history(self) -> None:
        """Clear generation history."""
        self.generation_history.clear()
        self.constraint_history.clear()
    
    def export_history(self, output_path: str) -> None:
        """
        Export generation history to CSV for offline analysis.
        
        Parameters
        ----------
        output_path : str
            Path to save CSV file
        """
        if not self.generation_history:
            warnings.warn("No history to export")
            return
        
        # Convert to DataFrame
        records = []
        for i, (output, constraints) in enumerate(zip(self.generation_history, self.constraint_history)):
            record = {
                'index': i,
                'prompt': output.prompt,
                'output': output.text,
                'performance_score': output.performance_score,
                **{f'constraint_{k}': v for k, v in constraints.items()},
                **{f'metadata_{k}': v for k, v in output.metadata.items() if isinstance(v, (int, float, str))}
            }
            records.append(record)
        
        df = pd.DataFrame(records)
        df.to_csv(output_path, index=False)
        print(f"✓ Exported {len(records)} records to {output_path}")
