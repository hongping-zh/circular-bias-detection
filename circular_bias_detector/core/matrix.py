"""
Matrix operations and validation for circular bias detection.

This module provides utilities for:
- Input validation
- Matrix preparation and transformation
- Data type conversions
"""

import numpy as np
import pandas as pd
from typing import Optional, Tuple, Union
import warnings


def validate_matrices(performance_matrix: np.ndarray,
                     constraint_matrix: np.ndarray,
                     algorithm_params: Optional[np.ndarray] = None) -> None:
    """
    Validate input matrices for bias detection.
    
    Parameters
    ----------
    performance_matrix : np.ndarray
        Shape (T, K) where T is time periods, K is algorithms
    constraint_matrix : np.ndarray
        Shape (T, p) where T is time periods, p is constraint types
    algorithm_params : np.ndarray, optional
        Shape (T, K, p) where p is parameter dimensions
    
    Raises
    ------
    ValueError
        If matrices have invalid shapes or contain invalid values
        
    Examples
    --------
    >>> perf = np.random.rand(10, 3)
    >>> const = np.random.rand(10, 2)
    >>> validate_matrices(perf, const)  # No exception raised
    """
    
    # Check performance matrix
    if not isinstance(performance_matrix, np.ndarray):
        raise ValueError("performance_matrix must be numpy array")
    
    if performance_matrix.ndim != 2:
        raise ValueError("performance_matrix must be 2D (T, K)")
    
    T_perf, K = performance_matrix.shape
    
    if T_perf < 2:
        raise ValueError("Need at least 2 time periods")
    
    if K < 1:
        raise ValueError("Need at least 1 algorithm")
    
    # Check for NaN/inf
    if not np.isfinite(performance_matrix).all():
        raise ValueError("performance_matrix contains NaN or infinite values")
    
    # Check constraint matrix
    if not isinstance(constraint_matrix, np.ndarray):
        raise ValueError("constraint_matrix must be numpy array")
    
    if constraint_matrix.ndim != 2:
        raise ValueError("constraint_matrix must be 2D (T, p)")
    
    T_const, p = constraint_matrix.shape
    
    if T_const != T_perf:
        raise ValueError(
            f"Time dimension mismatch: performance={T_perf}, constraints={T_const}"
        )
    
    if p < 1:
        raise ValueError("Need at least 1 constraint type")
    
    if not np.isfinite(constraint_matrix).all():
        raise ValueError("constraint_matrix contains NaN or infinite values")
    
    # Check algorithm parameters if provided
    if algorithm_params is not None:
        if not isinstance(algorithm_params, np.ndarray):
            raise ValueError("algorithm_params must be numpy array")
        
        if algorithm_params.ndim != 3:
            raise ValueError("algorithm_params must be 3D (T, K, p)")
        
        T_params, K_params, p_params = algorithm_params.shape
        
        if T_params != T_perf:
            raise ValueError(
                f"Time dimension mismatch in algorithm_params: {T_params} vs {T_perf}"
            )
        
        if K_params != K:
            raise ValueError(
                f"Algorithm dimension mismatch in algorithm_params: {K_params} vs {K}"
            )
        
        if not np.isfinite(algorithm_params).all():
            raise ValueError("algorithm_params contains NaN or infinite values")


def prepare_performance_matrix(data: Union[np.ndarray, pd.DataFrame, list],
                               algorithm_names: Optional[list] = None) -> Tuple[np.ndarray, Optional[list]]:
    """
    Convert input data to standardized performance matrix format.
    
    Parameters
    ----------
    data : array-like
        Performance data in various formats
    algorithm_names : list, optional
        Names of algorithms (extracted from DataFrame columns if available)
        
    Returns
    -------
    tuple
        (performance_matrix, algorithm_names)
        - performance_matrix: np.ndarray of shape (T, K)
        - algorithm_names: list of algorithm names or None
        
    Examples
    --------
    >>> df = pd.DataFrame({'algo1': [0.8, 0.82], 'algo2': [0.75, 0.78]})
    >>> matrix, names = prepare_performance_matrix(df)
    >>> print(matrix.shape, names)
    (2, 2) ['algo1', 'algo2']
    """
    if isinstance(data, pd.DataFrame):
        matrix = data.values
        if algorithm_names is None:
            algorithm_names = list(data.columns)
    elif isinstance(data, list):
        matrix = np.array(data)
    elif isinstance(data, np.ndarray):
        matrix = data
    else:
        raise TypeError(f"Unsupported data type: {type(data)}")
    
    # Ensure 2D
    if matrix.ndim == 1:
        matrix = matrix.reshape(-1, 1)
    elif matrix.ndim != 2:
        raise ValueError(f"Performance matrix must be 2D, got {matrix.ndim}D")
    
    return matrix, algorithm_names


def prepare_constraint_matrix(data: Union[np.ndarray, pd.DataFrame, list],
                              constraint_names: Optional[list] = None) -> Tuple[np.ndarray, Optional[list]]:
    """
    Convert input data to standardized constraint matrix format.
    
    Parameters
    ----------
    data : array-like
        Constraint data in various formats
    constraint_names : list, optional
        Names of constraints (extracted from DataFrame columns if available)
        
    Returns
    -------
    tuple
        (constraint_matrix, constraint_names)
        - constraint_matrix: np.ndarray of shape (T, p)
        - constraint_names: list of constraint names or None
        
    Examples
    --------
    >>> df = pd.DataFrame({'temperature': [0.7, 0.7], 'max_tokens': [100, 100]})
    >>> matrix, names = prepare_constraint_matrix(df)
    >>> print(matrix.shape, names)
    (2, 2) ['temperature', 'max_tokens']
    """
    if isinstance(data, pd.DataFrame):
        matrix = data.values
        if constraint_names is None:
            constraint_names = list(data.columns)
    elif isinstance(data, list):
        matrix = np.array(data)
    elif isinstance(data, np.ndarray):
        matrix = data
    else:
        raise TypeError(f"Unsupported data type: {type(data)}")
    
    # Ensure 2D
    if matrix.ndim == 1:
        matrix = matrix.reshape(-1, 1)
    elif matrix.ndim != 2:
        raise ValueError(f"Constraint matrix must be 2D, got {matrix.ndim}D")
    
    return matrix, constraint_names


def normalize_matrix(matrix: np.ndarray, 
                     method: str = 'minmax',
                     axis: Optional[int] = None) -> np.ndarray:
    """
    Normalize matrix values for improved numerical stability.
    
    Parameters
    ----------
    matrix : np.ndarray
        Input matrix to normalize
    method : str, default='minmax'
        Normalization method: 'minmax', 'zscore', or 'none'
    axis : int, optional
        Axis along which to normalize (None for global)
        
    Returns
    -------
    np.ndarray
        Normalized matrix
        
    Examples
    --------
    >>> matrix = np.array([[1, 2], [3, 4]])
    >>> normalized = normalize_matrix(matrix, method='minmax')
    >>> print(normalized.min(), normalized.max())
    0.0 1.0
    """
    if method == 'none':
        return matrix
    
    if method == 'minmax':
        min_val = np.min(matrix, axis=axis, keepdims=True)
        max_val = np.max(matrix, axis=axis, keepdims=True)
        
        # Avoid division by zero
        range_val = max_val - min_val
        range_val = np.where(range_val == 0, 1, range_val)
        
        return (matrix - min_val) / range_val
    
    elif method == 'zscore':
        mean_val = np.mean(matrix, axis=axis, keepdims=True)
        std_val = np.std(matrix, axis=axis, keepdims=True)
        
        # Avoid division by zero
        std_val = np.where(std_val == 0, 1, std_val)
        
        return (matrix - mean_val) / std_val
    
    else:
        raise ValueError(f"Unknown normalization method: {method}")


def check_matrix_quality(matrix: np.ndarray, 
                        name: str = "matrix") -> dict:
    """
    Perform quality checks on input matrix and return diagnostics.
    
    Parameters
    ----------
    matrix : np.ndarray
        Matrix to check
    name : str, default="matrix"
        Name for reporting
        
    Returns
    -------
    dict
        Quality diagnostics including:
        - has_nan: bool
        - has_inf: bool
        - has_negative: bool
        - rank: int (matrix rank)
        - condition_number: float
        - sparsity: float (fraction of zeros)
        
    Examples
    --------
    >>> matrix = np.array([[1, 2], [3, 4]])
    >>> quality = check_matrix_quality(matrix, name="performance")
    >>> print(quality['rank'], quality['has_nan'])
    2 False
    """
    diagnostics = {
        'name': name,
        'shape': matrix.shape,
        'has_nan': bool(np.isnan(matrix).any()),
        'has_inf': bool(np.isinf(matrix).any()),
        'has_negative': bool((matrix < 0).any()),
        'min_value': float(np.min(matrix)),
        'max_value': float(np.max(matrix)),
        'mean_value': float(np.mean(matrix)),
        'std_value': float(np.std(matrix)),
        'sparsity': float(np.sum(matrix == 0) / matrix.size),
    }
    
    # Compute rank for 2D matrices
    if matrix.ndim == 2:
        try:
            diagnostics['rank'] = int(np.linalg.matrix_rank(matrix))
            
            # Condition number (numerical stability indicator)
            singular_values = np.linalg.svd(matrix, compute_uv=False)
            if singular_values[-1] > 1e-10:
                diagnostics['condition_number'] = float(singular_values[0] / singular_values[-1])
            else:
                diagnostics['condition_number'] = float('inf')
        except:
            diagnostics['rank'] = None
            diagnostics['condition_number'] = None
    
    return diagnostics
