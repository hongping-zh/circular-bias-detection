# Contributing Guide
## How to Report Issues
- Use GitHub Issues with a minimal reproducible example and environment info.
- Labels: bug, question, enhancement.
## Feature Requests
- Describe use-case and expected behavior; add sample data if possible.
## Development Setup
- Python >= 3.8
- pip install -r requirements.txt
- pip install -e .[cli]
- python -m pytest tests/
## Code Style & Tests
- Follow PEP8/black (if configured). Ensure tests pass locally.
## Pull Requests
- Small, focused PRs. Link related issues. CI must pass.
## Security/Privacy
- Do not include sensitive data in issues or PRs.
