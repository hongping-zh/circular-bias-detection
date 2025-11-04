"""
Custom exceptions for circular bias detection framework.

This module defines all custom exception classes used throughout the framework
to provide clear and specific error messages.
"""


class CircularBiasDetectorError(Exception):
    """Base exception for all circular bias detector errors."""
    
    pass


class ValidationError(CircularBiasDetectorError):
    """Raised when input validation fails."""
    
    def __init__(self, message: str, parameter_name: str = None):
        """
        Initialize validation error.
        
        Parameters
        ----------
        message : str
            Error message describing the validation failure.
        parameter_name : str, optional
            Name of the parameter that failed validation.
        """
        self.parameter_name = parameter_name
        if parameter_name:
            message = f"Validation error for '{parameter_name}': {message}"
        super().__init__(message)


class MatrixShapeError(ValidationError):
    """Raised when matrix dimensions are incompatible."""
    
    def __init__(self, message: str, expected_shape=None, actual_shape=None):
        """
        Initialize matrix shape error.
        
        Parameters
        ----------
        message : str
            Error message.
        expected_shape : tuple, optional
            Expected matrix shape.
        actual_shape : tuple, optional
            Actual matrix shape received.
        """
        self.expected_shape = expected_shape
        self.actual_shape = actual_shape
        
        if expected_shape and actual_shape:
            message = (
                f"{message}. Expected shape {expected_shape}, "
                f"but got {actual_shape}"
            )
        
        super().__init__(message, parameter_name="matrix")


class InsufficientDataError(CircularBiasDetectorError):
    """Raised when insufficient data is provided for analysis."""
    
    def __init__(self, message: str, required_size: int = None, actual_size: int = None):
        """
        Initialize insufficient data error.
        
        Parameters
        ----------
        message : str
            Error message.
        required_size : int, optional
            Minimum required data size.
        actual_size : int, optional
            Actual data size received.
        """
        self.required_size = required_size
        self.actual_size = actual_size
        
        if required_size and actual_size:
            message = (
                f"{message}. Required at least {required_size} samples, "
                f"but got {actual_size}"
            )
        
        super().__init__(message)


class ThresholdError(CircularBiasDetectorError):
    """Raised when threshold values are invalid."""
    
    def __init__(self, message: str, threshold_name: str = None, threshold_value=None):
        """
        Initialize threshold error.
        
        Parameters
        ----------
        message : str
            Error message.
        threshold_name : str, optional
            Name of the threshold parameter.
        threshold_value : float, optional
            Invalid threshold value.
        """
        self.threshold_name = threshold_name
        self.threshold_value = threshold_value
        
        if threshold_name and threshold_value is not None:
            message = (
                f"{message}. Threshold '{threshold_name}' has invalid value: "
                f"{threshold_value}"
            )
        
        super().__init__(message)


class ComputationError(CircularBiasDetectorError):
    """Raised when a computation fails."""
    
    def __init__(self, message: str, metric_name: str = None):
        """
        Initialize computation error.
        
        Parameters
        ----------
        message : str
            Error message.
        metric_name : str, optional
            Name of the metric being computed.
        """
        self.metric_name = metric_name
        
        if metric_name:
            message = f"Error computing {metric_name}: {message}"
        
        super().__init__(message)


class ConfigurationError(CircularBiasDetectorError):
    """Raised when configuration is invalid."""
    
    def __init__(self, message: str, config_key: str = None):
        """
        Initialize configuration error.
        
        Parameters
        ----------
        message : str
            Error message.
        config_key : str, optional
            Name of the configuration key that is invalid.
        """
        self.config_key = config_key
        
        if config_key:
            message = f"Configuration error for '{config_key}': {message}"
        
        super().__init__(message)


class DataLoadError(CircularBiasDetectorError):
    """Raised when data loading fails."""
    
    def __init__(self, message: str, file_path: str = None):
        """
        Initialize data load error.
        
        Parameters
        ----------
        message : str
            Error message.
        file_path : str, optional
            Path to the file that failed to load.
        """
        self.file_path = file_path
        
        if file_path:
            message = f"Failed to load data from '{file_path}': {message}"
        
        super().__init__(message)


class InferenceError(CircularBiasDetectorError):
    """Raised when LLM inference fails."""
    
    def __init__(self, message: str, backend_name: str = None):
        """
        Initialize inference error.
        
        Parameters
        ----------
        message : str
            Error message.
        backend_name : str, optional
            Name of the inference backend that failed.
        """
        self.backend_name = backend_name
        
        if backend_name:
            message = f"Inference error with backend '{backend_name}': {message}"
        
        super().__init__(message)
