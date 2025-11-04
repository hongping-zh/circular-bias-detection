"""
Unified logging system for circular bias detection framework.

This module provides a centralized logging configuration that can be used
across all modules in the framework.
"""

import logging
import sys
from pathlib import Path
from typing import Optional

from .config import get_config


class ColoredFormatter(logging.Formatter):
    """
    Custom formatter with color support for console output.
    
    Uses ANSI color codes to highlight different log levels.
    """
    
    # ANSI color codes
    COLORS = {
        "DEBUG": "\033[36m",      # Cyan
        "INFO": "\033[32m",       # Green
        "WARNING": "\033[33m",    # Yellow
        "ERROR": "\033[31m",      # Red
        "CRITICAL": "\033[35m",   # Magenta
    }
    RESET = "\033[0m"
    
    def format(self, record):
        """Format log record with color codes."""
        if record.levelname in self.COLORS:
            record.levelname = (
                f"{self.COLORS[record.levelname]}{record.levelname}{self.RESET}"
            )
        return super().format(record)


def setup_logger(
    name: str = "circular_bias_detector",
    level: Optional[str] = None,
    log_file: Optional[Path] = None,
    use_colors: bool = True,
) -> logging.Logger:
    """
    Set up a logger with consistent formatting.
    
    Parameters
    ----------
    name : str, optional
        Logger name. Default: "circular_bias_detector"
    level : str, optional
        Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        If None, uses level from config. Default: None
    log_file : Path, optional
        Path to log file. If provided, logs will also be written to file.
        Default: None (console only)
    use_colors : bool, optional
        Whether to use colored output for console. Default: True
    
    Returns
    -------
    logging.Logger
        Configured logger instance.
    
    Examples
    --------
    >>> from circular_bias_detector.logging import setup_logger
    >>> logger = setup_logger("my_module")
    >>> logger.info("Starting bias detection")
    >>> logger.warning("Low sample size detected")
    """
    # Get logger
    logger = logging.getLogger(name)
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    # Set level
    config = get_config()
    log_level = level or config.log_level
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, log_level.upper()))
    
    # Format
    if use_colors:
        console_formatter = ColoredFormatter(config.log_format)
    else:
        console_formatter = logging.Formatter(config.log_format)
    
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # File handler (optional)
    if log_file:
        log_file = Path(log_file)
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(getattr(logging, log_level.upper()))
        
        # File logs don't need colors
        file_formatter = logging.Formatter(config.log_format)
        file_handler.setFormatter(file_formatter)
        
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get an existing logger or create a new one.
    
    Parameters
    ----------
    name : str
        Logger name (typically __name__ of the calling module).
    
    Returns
    -------
    logging.Logger
        Logger instance.
    
    Examples
    --------
    >>> from circular_bias_detector.logging import get_logger
    >>> logger = get_logger(__name__)
    >>> logger.debug("Detailed debug information")
    """
    logger = logging.getLogger(name)
    
    # If logger has no handlers, set it up
    if not logger.handlers:
        setup_logger(name)
    
    return logger


def disable_logging():
    """Disable all logging output (useful for tests)."""
    logging.disable(logging.CRITICAL)


def enable_logging():
    """Re-enable logging after calling disable_logging()."""
    logging.disable(logging.NOTSET)


# Module-level logger for this module
_logger = get_logger(__name__)


def log_function_call(func):
    """
    Decorator to log function calls with arguments.
    
    Parameters
    ----------
    func : callable
        Function to wrap with logging.
    
    Returns
    -------
    callable
        Wrapped function.
    
    Examples
    --------
    >>> from circular_bias_detector.logging import log_function_call
    >>> 
    >>> @log_function_call
    >>> def compute_psi(matrix):
    ...     return 0.15
    """
    def wrapper(*args, **kwargs):
        logger = get_logger(func.__module__)
        logger.debug(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
        
        try:
            result = func(*args, **kwargs)
            logger.debug(f"{func.__name__} returned {result}")
            return result
        except Exception as e:
            logger.error(f"{func.__name__} raised {type(e).__name__}: {e}")
            raise
    
    return wrapper
