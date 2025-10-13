# Contributing to Circular Bias Detection Framework

Thank you for your interest in contributing!

## 🚀 Quick Start

```bash
# Fork and clone
git clone https://github.com/YOUR_USERNAME/circular-bias-detection.git
cd circular-bias-detection

# Install dependencies
pip install -r requirements.txt
pip install pytest black flake8

# Create branch
git checkout -b feature/your-feature
```

## 📝 Code Standards

- **Style**: Follow PEP 8, format with `black`
- **Line length**: 88 characters
- **Tests**: Add tests for new features
- **Docstrings**: Use Google style

```bash
# Before committing
black circular_bias_detector/ tests/
flake8 circular_bias_detector/ --max-line-length=88
pytest
```

## 🧪 Testing

```bash
# Run all tests
pytest

# With coverage
pytest --cov=circular_bias_detector --cov-report=html
```

## 📦 Pull Request Process

1. **Commit format**: `<type>: <description>`
   - Types: `feat`, `fix`, `docs`, `test`, `refactor`
   - Example: `feat: Add confidence intervals for PSI`

2. **Before PR**:
   - [ ] Tests pass
   - [ ] Code formatted with Black
   - [ ] Documentation updated
   - [ ] Clear commit messages

3. **PR Template**:
   - Description of changes
   - Type of change (bug fix, feature, docs)
   - Testing performed
   - Related issues

## 🐛 Reporting Bugs

Use [GitHub Issues](https://github.com/hongping-zh/circular-bias-detection/issues):

**Include**:
- Clear description
- Steps to reproduce
- Expected vs. actual behavior
- Environment (OS, Python version)
- Code snippet (if applicable)

## 🌟 Feature Requests

Open an issue with:
- Use case description
- Proposed API (if applicable)
- Why it's useful
- Alternative solutions considered

## 🌍 Code of Conduct

- Use welcoming and inclusive language
- Respect differing viewpoints
- Accept constructive criticism gracefully
- Focus on what's best for the community

**Unacceptable**: Harassment, trolling, personal attacks, or discrimination.

## 📚 Documentation

- Update docstrings for new functions
- Add examples for complex features
- Update README if adding major functionality
- Include type hints

**Docstring example**:
```python
def compute_psi(theta_matrix: np.ndarray) -> float:
    """
    Compute Performance-Structure Independence score.
    
    Args:
        theta_matrix: Parameter matrix, shape (T, K)
    
    Returns:
        PSI score (0-1), higher = more unstable
    
    Example:
        >>> theta = np.array([[0.7, 0.8], [0.71, 0.81]])
        >>> psi = compute_psi(theta)
    """
```

## 🎯 Priority Areas

Help needed with:
- Additional test cases
- Real-world case studies
- Documentation improvements
- Performance optimizations
- Integration examples

## 📞 Contact

- **Issues**: https://github.com/hongping-zh/circular-bias-detection/issues
- **Email**: yujjam@uest.edu.gr
- **Dataset**: https://doi.org/10.5281/zenodo.17201032

---

Thank you for contributing! 🙏
