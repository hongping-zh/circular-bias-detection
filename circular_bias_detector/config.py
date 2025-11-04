"""
Configuration management for circular bias detection framework.

This module centralizes all configuration parameters, default thresholds,
and environment-based overrides for the bias detection system.
"""

import os
from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class BiasDetectionConfig:
    """
    Configuration for bias detection thresholds and parameters.
    
    Attributes
    ----------
    psi_threshold : float
        Threshold for PSI (Performance-Structure Independence).
        Higher values indicate more parameter instability.
        Default: 0.15
    ccs_threshold : float
        Threshold for CCS (Constraint-Consistency Score).
        Lower values indicate more inconsistency.
        Default: 0.85
    rho_pc_threshold : float
        Threshold for ρ_PC (Performance-Constraint Correlation).
        Higher absolute values indicate stronger dependency.
        Default: 0.5
    n_bootstrap : int
        Number of bootstrap iterations for confidence intervals.
        Default: 1000
    confidence_level : float
        Confidence level for statistical tests (0-1).
        Default: 0.95
    random_seed : Optional[int]
        Random seed for reproducibility.
        Default: None (no fixed seed)
    """
    
    # Bias detection thresholds
    psi_threshold: float = 0.15
    ccs_threshold: float = 0.85
    rho_pc_threshold: float = 0.5
    
    # Bootstrap parameters
    n_bootstrap: int = 1000
    confidence_level: float = 0.95
    
    # Reproducibility
    random_seed: Optional[int] = None
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Validation parameters
    min_time_periods: int = 2
    min_algorithms: int = 1
    min_constraints: int = 1
    
    def __post_init__(self):
        """Validate configuration parameters after initialization."""
        self.validate()
    
    def validate(self):
        """
        Validate configuration parameters.
        
        Raises
        ------
        ValueError
            If any configuration parameter is invalid.
        """
        if not 0 < self.psi_threshold < 1:
            raise ValueError(f"psi_threshold must be in (0, 1), got {self.psi_threshold}")
        
        if not 0 < self.ccs_threshold <= 1:
            raise ValueError(f"ccs_threshold must be in (0, 1], got {self.ccs_threshold}")
        
        if not 0 <= self.rho_pc_threshold <= 1:
            raise ValueError(
                f"rho_pc_threshold must be in [0, 1], got {self.rho_pc_threshold}"
            )
        
        if self.n_bootstrap < 100:
            raise ValueError(
                f"n_bootstrap should be >= 100 for reliable estimates, got {self.n_bootstrap}"
            )
        
        if not 0 < self.confidence_level < 1:
            raise ValueError(
                f"confidence_level must be in (0, 1), got {self.confidence_level}"
            )
        
        if self.min_time_periods < 2:
            raise ValueError(
                f"min_time_periods must be >= 2, got {self.min_time_periods}"
            )
    
    def to_dict(self) -> Dict:
        """Convert configuration to dictionary."""
        return {
            "psi_threshold": self.psi_threshold,
            "ccs_threshold": self.ccs_threshold,
            "rho_pc_threshold": self.rho_pc_threshold,
            "n_bootstrap": self.n_bootstrap,
            "confidence_level": self.confidence_level,
            "random_seed": self.random_seed,
            "log_level": self.log_level,
            "min_time_periods": self.min_time_periods,
            "min_algorithms": self.min_algorithms,
            "min_constraints": self.min_constraints,
        }
    
    @classmethod
    def from_env(cls) -> "BiasDetectionConfig":
        """
        Load configuration from environment variables.
        
        Environment variables:
        - CBD_PSI_THRESHOLD: PSI threshold (float)
        - CBD_CCS_THRESHOLD: CCS threshold (float)
        - CBD_RHO_PC_THRESHOLD: ρ_PC threshold (float)
        - CBD_N_BOOTSTRAP: Number of bootstrap iterations (int)
        - CBD_CONFIDENCE_LEVEL: Confidence level (float)
        - CBD_RANDOM_SEED: Random seed (int)
        - CBD_LOG_LEVEL: Logging level (str)
        
        Returns
        -------
        BiasDetectionConfig
            Configuration object with values from environment.
        """
        return cls(
            psi_threshold=float(os.getenv("CBD_PSI_THRESHOLD", "0.15")),
            ccs_threshold=float(os.getenv("CBD_CCS_THRESHOLD", "0.85")),
            rho_pc_threshold=float(os.getenv("CBD_RHO_PC_THRESHOLD", "0.5")),
            n_bootstrap=int(os.getenv("CBD_N_BOOTSTRAP", "1000")),
            confidence_level=float(os.getenv("CBD_CONFIDENCE_LEVEL", "0.95")),
            random_seed=int(os.getenv("CBD_RANDOM_SEED"))
            if os.getenv("CBD_RANDOM_SEED")
            else None,
            log_level=os.getenv("CBD_LOG_LEVEL", "INFO"),
        )


# Global default configuration instance
DEFAULT_CONFIG = BiasDetectionConfig()


def get_config() -> BiasDetectionConfig:
    """
    Get the current configuration.
    
    This function returns the default configuration, which can be
    overridden by environment variables using BiasDetectionConfig.from_env().
    
    Returns
    -------
    BiasDetectionConfig
        Current configuration instance.
    """
    return DEFAULT_CONFIG


def set_config(config: BiasDetectionConfig):
    """
    Set a new global configuration.
    
    Parameters
    ----------
    config : BiasDetectionConfig
        New configuration to use globally.
    """
    global DEFAULT_CONFIG
    DEFAULT_CONFIG = config
