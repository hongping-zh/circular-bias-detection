# Development Guide

This guide explains how to set up your development environment and contribute to the Circular Bias Detection framework.

## Table of Contents

- [Setup Development Environment](#setup-development-environment)
- [Code Quality Tools](#code-quality-tools)
- [Testing](#testing)
- [Documentation](#documentation)
- [Git Workflow](#git-workflow)

---

## Setup Development Environment

### 1. Clone the Repository

```bash
git clone https://github.com/hongping-zh/circular-bias-detection.git
cd circular-bias-detection
```

### 2. Create Virtual Environment

```bash
# Using venv
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Or using conda
conda create -n cbd python=3.10
conda activate cbd
```

### 3. Install Development Dependencies

```bash
# Install package in editable mode with all development dependencies
pip install -e ".[dev]"

# Or install from pyproject.toml
pip install -e .
pip install pytest pytest-cov black flake8 mypy isort pre-commit
```

### 4. Install Pre-commit Hooks

Pre-commit hooks automatically run code quality checks before each commit:

```bash
pre-commit install
```

Now every `git commit` will automatically:
- Format code with Black
- Sort imports with isort
- Check code with flake8
- Run type checking with mypy

To run hooks manually on all files:

```bash
pre-commit run --all-files
```

---

## Code Quality Tools

### Black (Code Formatter)

Format all Python files:

```bash
black circular_bias_detector tests
```

Check formatting without modifying files:

```bash
black --check circular_bias_detector tests
```

### isort (Import Sorter)

Sort imports in all files:

```bash
isort circular_bias_detector tests
```

### flake8 (Linter)

Check code for style issues:

```bash
flake8 circular_bias_detector tests
```

Configuration is in `.flake8` file.

### mypy (Type Checker)

Run static type checking:

```bash
mypy circular_bias_detector
```

Configuration is in `pyproject.toml` under `[tool.mypy]`.

### Run All Checks Together

```bash
# Format code
black circular_bias_detector tests

# Sort imports
isort circular_bias_detector tests

# Check linting
flake8 circular_bias_detector tests

# Check types
mypy circular_bias_detector
```

---

## Testing

### Run All Tests

```bash
pytest
```

### Run with Coverage Report

```bash
pytest --cov=circular_bias_detector --cov-report=html
```

View coverage report:

```bash
# Open htmlcov/index.html in browser
open htmlcov/index.html  # macOS
start htmlcov/index.html  # Windows
xdg-open htmlcov/index.html  # Linux
```

### Run Specific Test Categories

```bash
# Unit tests only
pytest -m unit

# Integration tests only
pytest -m integration

# Skip slow tests
pytest -m "not slow"
```

### Run Specific Test Files

```bash
pytest tests/test_core_metrics.py
pytest tests/test_detection.py -v
```

### Run Tests in Parallel

```bash
pytest -n auto
```

### Coverage Requirements

- Minimum coverage: **80%**
- Target coverage: **90%+**
- Critical modules (core/, detection.py) should have **95%+** coverage

---

## Documentation

### Writing Docstrings

Follow NumPy docstring style:

```python
def compute_psi(performance_matrix: np.ndarray) -> float:
    """
    Compute Performance-Structure Independence (PSI) score.
    
    PSI measures parameter stability across evaluation periods by computing
    the average parameter difference between consecutive time steps.
    
    Parameters
    ----------
    performance_matrix : np.ndarray
        Shape (T, K) where T is time periods, K is algorithms
    
    Returns
    -------
    float
        PSI score (higher values indicate more instability/bias)
    
    Raises
    ------
    ValidationError
        If matrix shape is invalid or contains NaN/Inf values
    
    Examples
    --------
    >>> perf_matrix = np.array([[0.8, 0.75], [0.82, 0.78]])
    >>> psi = compute_psi(perf_matrix)
    >>> print(f"PSI: {psi:.4f}")
    PSI: 0.0200
    
    Notes
    -----
    Higher PSI values indicate that algorithm parameters changed
    significantly during evaluation, suggesting circular bias.
    
    References
    ----------
    .. [1] Zhang, H. (2024). "Circular Bias Detection Framework"
    """
    pass
```

### Type Annotations

Always include type hints:

```python
from typing import Optional, Dict, List, Tuple
import numpy as np

def detect_bias(
    performance_matrix: np.ndarray,
    constraint_matrix: np.ndarray,
    thresholds: Optional[Dict[str, float]] = None
) -> Tuple[bool, Dict[str, float]]:
    """Function with proper type annotations."""
    pass
```

---

## Git Workflow

### Branch Naming

```bash
# Feature branches
git checkout -b feature/add-new-metric

# Bug fixes
git checkout -b fix/psi-computation-error

# Documentation
git checkout -b docs/update-api-reference

# Refactoring
git checkout -b refactor/modernize-config
```

### Commit Messages

Follow conventional commits format:

```
type(scope): subject

body (optional)

footer (optional)
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Adding or updating tests
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `chore`: Maintenance tasks

Examples:

```bash
git commit -m "feat(core): add adaptive threshold computation"
git commit -m "fix(detection): correct PSI calculation for edge cases"
git commit -m "docs(api): update BiasDetector docstrings"
git commit -m "test(bootstrap): add tests for confidence intervals"
```

### Pull Request Checklist

Before submitting a PR, ensure:

- [ ] All tests pass (`pytest`)
- [ ] Coverage is ≥80% (`pytest --cov`)
- [ ] Code is formatted (`black`, `isort`)
- [ ] No linting errors (`flake8`)
- [ ] Type checking passes (`mypy`)
- [ ] Documentation is updated
- [ ] CHANGELOG.md is updated
- [ ] Pre-commit hooks pass

---

## Configuration Management

### Using Config Module

```python
from circular_bias_detector.config import BiasDetectionConfig, get_config

# Get default config
config = get_config()

# Create custom config
custom_config = BiasDetectionConfig(
    psi_threshold=0.10,
    n_bootstrap=2000,
    random_seed=42
)

# Use environment variables
config = BiasDetectionConfig.from_env()
```

### Environment Variables

```bash
export CBD_PSI_THRESHOLD=0.12
export CBD_N_BOOTSTRAP=2000
export CBD_LOG_LEVEL=DEBUG
export CBD_RANDOM_SEED=42
```

---

## Logging

### Using Logger

```python
from circular_bias_detector.logging import get_logger

logger = get_logger(__name__)

def my_function():
    logger.debug("Detailed debug information")
    logger.info("Function started")
    logger.warning("Parameter value is close to threshold")
    logger.error("Computation failed")
```

### Log Levels

- `DEBUG`: Detailed diagnostic information
- `INFO`: General informational messages
- `WARNING`: Warning messages for potential issues
- `ERROR`: Error messages for failures
- `CRITICAL`: Critical errors requiring immediate attention

---

## Exception Handling

### Using Custom Exceptions

```python
from circular_bias_detector.exceptions import (
    ValidationError,
    MatrixShapeError,
    InsufficientDataError,
)

def validate_input(matrix):
    if matrix.ndim != 2:
        raise MatrixShapeError(
            "Expected 2D matrix",
            expected_shape=(None, None),
            actual_shape=matrix.shape
        )
    
    if matrix.shape[0] < 2:
        raise InsufficientDataError(
            "Need at least 2 time periods",
            required_size=2,
            actual_size=matrix.shape[0]
        )
```

---

## Performance Optimization

### Profiling

```python
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# Your code here
detector.detect_bias(perf_matrix, const_matrix)

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumtime')
stats.print_stats(20)  # Top 20 functions
```

### Memory Profiling

```bash
pip install memory_profiler

python -m memory_profiler your_script.py
```

---

## Troubleshooting

### Common Issues

**Pre-commit hooks fail**

```bash
# Update hooks
pre-commit autoupdate

# Clear cache and reinstall
pre-commit uninstall
pre-commit clean
pre-commit install
```

**Tests fail with import errors**

```bash
# Reinstall package in editable mode
pip install -e .
```

**Coverage is below 80%**

```bash
# Generate detailed report
pytest --cov=circular_bias_detector --cov-report=term-missing

# Focus on untested files
```

---

## Resources

- [NumPy Docstring Guide](https://numpydoc.readthedocs.io/)
- [PEP 8 Style Guide](https://pep8.org/)
- [Type Hints (PEP 484)](https://www.python.org/dev/peps/pep-0484/)
- [pytest Documentation](https://docs.pytest.org/)
- [Black Documentation](https://black.readthedocs.io/)
