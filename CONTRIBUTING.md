# Contributing

Thank you for your interest in contributing to circular-bias-detection!

## Getting Started

### Suggested Next Steps
- File issues for feature requests or bugs
- Fork and open pull requests against `main` or feature branches
- Add tests for new features and follow existing test patterns

## Development Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/hongping-zh/circular-bias-detection.git
   cd circular-bias-detection
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install in editable mode with dev dependencies**:
   ```bash
   pip install -e ".[dev]"
   ```

## Code Style

### Formatting
- **Black** formatting recommended
- Line length: 100 characters
- Run: `black .`

### Type Hints
- Type hints encouraged for public APIs
- Use `typing` module for complex types

### Imports
- Use **isort** for import sorting
- Run: `isort .`

## Testing

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=cbd --cov-report=html

# Run specific test file
pytest tests/test_api.py

# Run with verbose output
pytest -v
```

### Writing Tests
- Place tests in `tests/` directory
- Name test files as `test_*.py`
- Name test functions as `test_*`
- Use descriptive test names
- Include docstrings for complex tests

Example:
```python
def test_detect_bias_with_random_labels():
    """Test that detect_bias returns high p-value for random labels."""
    X, y = make_classification(n_samples=100, random_state=42)
    y_random = np.random.permutation(y)
    
    model = SklearnCBDModel(DummyClassifier().fit(X, y_random))
    result = detect_bias(model, X, y, metric=accuracy_score, n_permutations=100)
    
    assert result["p_value"] > 0.05
```

## Pull Request Process

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**:
   - Write code
   - Add tests
   - Update documentation

3. **Run tests and formatting**:
   ```bash
   black .
   isort .
   pytest
   ```

4. **Commit your changes**:
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

5. **Push and create PR**:
   ```bash
   git push origin feature/your-feature-name
   ```
   Then create a Pull Request on GitHub

## Commit Message Guidelines

Follow conventional commits format:

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `test:` - Test additions or changes
- `refactor:` - Code refactoring
- `style:` - Code style changes (formatting, etc.)
- `chore:` - Maintenance tasks

Examples:
```
feat: add support for PyTorch models
fix: correct p-value calculation in detect_bias
docs: update CBDModel protocol documentation
test: add integration tests for sklearn adapter
```

## Documentation

### Docstring Format
Use NumPy-style docstrings:

```python
def detect_bias(model, X, y, metric, n_permutations=1000):
    """
    Detect circular bias using permutation testing.
    
    Parameters
    ----------
    model : CBDModel
        Model implementing predict() method
    X : array-like
        Feature matrix
    y : array-like
        Target labels
    metric : callable
        Metric function (y_true, y_pred) -> float
    n_permutations : int, default=1000
        Number of permutations for null distribution
        
    Returns
    -------
    result : dict
        Dictionary containing observed_metric, p_value, and conclusion
        
    Examples
    --------
    >>> from cbd import detect_bias, SklearnCBDModel
    >>> model = SklearnCBDModel(clf)
    >>> result = detect_bias(model, X, y, accuracy_score)
    """
```

### Adding Documentation
- Update relevant `.md` files in `docs/`
- Add examples to `examples/` directory
- Update README.md if adding major features

## Issue Guidelines

### Bug Reports
Include:
- Python version
- Package version
- Minimal reproducible example
- Expected vs actual behavior
- Error messages/stack traces

### Feature Requests
Include:
- Use case description
- Proposed API (if applicable)
- Example usage
- Alternatives considered

## Code Review

Pull requests will be reviewed for:
- Code quality and style
- Test coverage
- Documentation completeness
- Backward compatibility
- Performance implications

## Questions?

- Open an issue for questions
- Check existing issues and PRs
- Review documentation in `docs/`

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to circular-bias-detection! 🎉
