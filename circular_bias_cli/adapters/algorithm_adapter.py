"""
Algorithm Adapter - Bridge between CLI and core library.

This adapter provides a unified interface for running detection algorithms,
bridging the CLI's AlgorithmManager interface to the core BiasDetector library.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional
import logging


class AlgorithmAdapter:
    """
    Adapter that bridges CLI algorithm management to core detection library.
    
    This allows the CLI to use a consistent interface while delegating
    actual computation to the core circular_bias_detector library.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.detector = None
        self._available_algorithms = {
            'psi': {
                'description': 'Performance-Structure Independence - detects parameter instability',
                'parameters': ['alpha', 'threshold'],
                'function': self._run_psi
            },
            'ccs': {
                'description': 'Constraint-Consistency Score - detects evaluation inconsistency',
                'parameters': ['threshold'],
                'function': self._run_ccs
            },
            'rho_pc': {
                'description': 'Performance-Constraint Correlation - detects suspicious dependencies',
                'parameters': ['threshold'],
                'function': self._run_rho_pc
            },
            'decision_framework': {
                'description': 'Integrated Decision Framework - combines all indicators',
                'parameters': ['psi_threshold', 'ccs_threshold', 'rho_pc_threshold'],
                'function': self._run_decision
            }
        }
    
    def run(self, algorithm_name: str, data: pd.DataFrame, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run specified algorithm on data.
        
        Args:
            algorithm_name: Algorithm identifier (psi, ccs, rho_pc, decision_framework)
            data: DataFrame with evaluation data containing columns:
                - time_period: evaluation period
                - algorithm: algorithm name
                - performance: performance metric [0-1]
                - constraint_compute: computational constraint
                - constraint_memory: memory constraint
                - constraint_dataset_size: dataset size constraint
            params: Algorithm-specific parameters
        
        Returns:
            Dictionary with results:
                - algorithm: algorithm name
                - score: computed score
                - threshold: detection threshold
                - detected: whether bias was detected
                - interpretation: human-readable interpretation
                - details: additional details
        
        Raises:
            ValueError: If algorithm name is unknown
            KeyError: If required data columns are missing
        """
        if algorithm_name not in self._available_algorithms:
            raise ValueError(f"Unknown algorithm: {algorithm_name}. "
                           f"Available: {list(self._available_algorithms.keys())}")
        
        self._validate_data(data)
        
        algo_func = self._available_algorithms[algorithm_name]['function']
        self.logger.info(f"Running {algorithm_name} algorithm")
        
        try:
            result = algo_func(data, params)
            self.logger.info(f"{algorithm_name} completed: bias_detected={result.get('detected', False)}")
            return result
        except Exception as e:
            self.logger.error(f"Algorithm {algorithm_name} failed: {e}")
            raise
    
    def _validate_data(self, data: pd.DataFrame) -> None:
        """Validate that data has required columns."""
        required_cols = [
            'time_period', 'algorithm', 'performance',
            'constraint_compute', 'constraint_memory', 'constraint_dataset_size'
        ]
        missing = [col for col in required_cols if col not in data.columns]
        if missing:
            raise KeyError(f"Missing required columns: {missing}")
        
        # Validate performance range
        if not data['performance'].between(0, 1).all():
            self.logger.warning("Performance values outside [0, 1] range")
    
    def _prepare_matrices(self, data: pd.DataFrame):
        """Convert DataFrame to matrices for core library."""
        # Performance matrix (T x K)
        perf_matrix = data.pivot(
            index='time_period',
            columns='algorithm',
            values='performance'
        ).values
        
        # Constraint matrix (T x p)
        const_matrix = data.groupby('time_period')[[
            'constraint_compute',
            'constraint_memory',
            'constraint_dataset_size'
        ]].first().values
        
        algorithms = data['algorithm'].unique().tolist()
        
        return perf_matrix, const_matrix, algorithms
    
    def _run_psi(self, data: pd.DataFrame, params: Dict[str, Any]) -> Dict[str, Any]:
        """Run PSI algorithm."""
        from circular_bias_detector.core import compute_psi
        
        perf_matrix, _, _ = self._prepare_matrices(data)
        
        # Compute PSI score
        psi_score = compute_psi(perf_matrix)
        threshold = params.get('threshold', 0.15)
        
        return {
            'algorithm': 'PSI',
            'score': float(psi_score),
            'threshold': threshold,
            'detected': psi_score > threshold,
            'interpretation': self._interpret_psi(psi_score, threshold),
            'details': {
                'time_periods': perf_matrix.shape[0],
                'algorithms': perf_matrix.shape[1],
                'stability': 'unstable' if psi_score > threshold else 'stable'
            }
        }
    
    def _run_ccs(self, data: pd.DataFrame, params: Dict[str, Any]) -> Dict[str, Any]:
        """Run CCS algorithm."""
        from circular_bias_detector.core import compute_ccs
        
        _, const_matrix, _ = self._prepare_matrices(data)
        
        # Compute CCS score
        ccs_score = compute_ccs(const_matrix)
        threshold = params.get('threshold', 0.85)
        
        return {
            'algorithm': 'CCS',
            'score': float(ccs_score),
            'threshold': threshold,
            'detected': ccs_score < threshold,
            'interpretation': self._interpret_ccs(ccs_score, threshold),
            'details': {
                'time_periods': const_matrix.shape[0],
                'constraints': const_matrix.shape[1],
                'consistency': 'inconsistent' if ccs_score < threshold else 'consistent'
            }
        }
    
    def _run_rho_pc(self, data: pd.DataFrame, params: Dict[str, Any]) -> Dict[str, Any]:
        """Run ρ_PC algorithm."""
        from circular_bias_detector.core import compute_rho_pc
        
        perf_matrix, const_matrix, _ = self._prepare_matrices(data)
        
        # Compute ρ_PC score
        rho_pc_score = compute_rho_pc(perf_matrix, const_matrix)
        threshold = params.get('threshold', 0.5)
        
        return {
            'algorithm': 'ρ_PC',
            'score': float(rho_pc_score),
            'threshold': threshold,
            'detected': abs(rho_pc_score) > threshold,
            'interpretation': self._interpret_rho_pc(rho_pc_score, threshold),
            'details': {
                'correlation_type': 'positive' if rho_pc_score > 0 else 'negative',
                'strength': 'strong' if abs(rho_pc_score) > threshold else 'weak'
            }
        }
    
    def _run_decision(self, data: pd.DataFrame, params: Dict[str, Any]) -> Dict[str, Any]:
        """Run integrated decision framework."""
        from circular_bias_detector import BiasDetector
        
        perf_matrix, const_matrix, algorithms = self._prepare_matrices(data)
        
        # Initialize detector with thresholds
        if not self.detector:
            self.detector = BiasDetector(
                psi_threshold=params.get('psi_threshold', 0.15),
                ccs_threshold=params.get('ccs_threshold', 0.85),
                rho_pc_threshold=params.get('rho_pc_threshold', 0.5)
            )
        
        # Run comprehensive detection
        results = self.detector.detect_bias(
            performance_matrix=perf_matrix,
            constraint_matrix=const_matrix,
            algorithm_names=algorithms
        )
        
        return {
            'algorithm': 'Decision Framework',
            'psi': float(results['psi_score']),
            'ccs': float(results['ccs_score']),
            'rho_pc': float(results['rho_pc_score']),
            'overall_bias': results['overall_bias'],
            'confidence': float(results['confidence']),
            'detected': results['overall_bias'],
            'interpretation': self._interpret_decision(results),
            'details': {
                'algorithms_evaluated': algorithms,
                'time_periods': perf_matrix.shape[0],
                'indicators_triggered': sum([
                    results['psi_score'] > params.get('psi_threshold', 0.15),
                    results['ccs_score'] < params.get('ccs_threshold', 0.85),
                    abs(results['rho_pc_score']) > params.get('rho_pc_threshold', 0.5)
                ])
            }
        }
    
    def _interpret_psi(self, score: float, threshold: float) -> str:
        """Interpret PSI score."""
        if score < threshold * 0.5:
            return f"Parameters are highly stable (PSI={score:.3f}). No instability detected."
        elif score < threshold:
            return f"Parameters show moderate stability (PSI={score:.3f}). Within acceptable range."
        elif score < threshold * 1.5:
            return f"Parameters are unstable (PSI={score:.3f}). Potential bias detected."
        else:
            return f"Parameters are highly unstable (PSI={score:.3f}). Strong bias signal."
    
    def _interpret_ccs(self, score: float, threshold: float) -> str:
        """Interpret CCS score."""
        if score > 0.95:
            return f"Constraints are highly consistent (CCS={score:.3f}). No issues detected."
        elif score >= threshold:
            return f"Constraints are consistent (CCS={score:.3f}). Within acceptable range."
        elif score >= threshold * 0.9:
            return f"Constraints show inconsistency (CCS={score:.3f}). Potential bias detected."
        else:
            return f"Constraints are highly inconsistent (CCS={score:.3f}). Strong bias signal."
    
    def _interpret_rho_pc(self, score: float, threshold: float) -> str:
        """Interpret ρ_PC score."""
        abs_score = abs(score)
        direction = "positive" if score > 0 else "negative"
        
        if abs_score < threshold * 0.5:
            return f"Performance and constraints are independent (ρ_PC={score:+.3f}). No correlation detected."
        elif abs_score < threshold:
            return f"Performance shows weak {direction} correlation with constraints (ρ_PC={score:+.3f}). Acceptable."
        elif abs_score < threshold * 1.5:
            return f"Performance shows strong {direction} correlation with constraints (ρ_PC={score:+.3f}). Potential bias."
        else:
            return f"Performance is highly correlated with constraints (ρ_PC={score:+.3f}). Strong bias signal."
    
    def _interpret_decision(self, results: Dict[str, Any]) -> str:
        """Interpret integrated decision results."""
        if not results['overall_bias']:
            return f"No circular bias detected (confidence: {results['confidence']:.1%}). Evaluation appears sound."
        
        triggered = []
        if results.get('psi_detected', False):
            triggered.append("parameter instability (PSI)")
        if results.get('ccs_detected', False):
            triggered.append("constraint inconsistency (CCS)")
        if results.get('rho_pc_detected', False):
            triggered.append("suspicious correlation (ρ_PC)")
        
        indicators = ", ".join(triggered) if triggered else "multiple indicators"
        return f"Circular bias detected via {indicators} (confidence: {results['confidence']:.1%}). Review evaluation methodology."
    
    def list_algorithms(self) -> Dict[str, Dict[str, Any]]:
        """List available algorithms and their metadata."""
        return self._available_algorithms.copy()
    
    def get_algorithm_info(self, algorithm_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific algorithm."""
        return self._available_algorithms.get(algorithm_name)
