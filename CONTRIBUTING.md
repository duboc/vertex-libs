# Contributing to Vertex Libs

We love your input! We want to make contributing to Vertex Libs as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## Development Process

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

1. Fork the repo and create your branch from `main`
2. If you've added code that should be tested, add tests
3. If you've changed APIs, update the documentation
4. Ensure the test suite passes
5. Make sure your code lints
6. Issue that pull request!

## Development Environment Setup

1. Clone your fork:
   ```bash
   git clone https://github.com/your-username/vertex-libs.git
   cd vertex-libs
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

## Running Tests

We use pytest for our test suite. Here are different ways to run tests:

```bash
# Run all tests
pytest

# Run tests with output
pytest -v

# Run tests in a specific file
pytest tests/test_gemini_client.py

# Run a specific test
pytest tests/test_gemini_client.py::test_init_with_project_id

# Run tests with coverage report
pytest --cov=vertex_libs --cov-report=term-missing

# Generate HTML coverage report
pytest --cov=vertex_libs --cov-report=html
```

### Test Coverage Requirements

- All new features must include test coverage
- Patches must maintain 100% code coverage
- Run coverage report to check: `pytest --cov=vertex_libs`

## Writing Tests

1. **Test Structure**
   ```python
   def test_feature_name():
       # Arrange - Set up test data
       client = GeminiClient()
       
       # Act - Perform the action
       result = client.some_method()
       
       # Assert - Check the results
       assert result == expected_value
   ```

2. **Mock Usage**
   ```python
   @patch('vertex_libs.gemini_client.genai')
   def test_with_mock(mock_genai):
       mock_genai.Client.return_value = Mock()
       # Test implementation
   ```

3. **Fixture Usage**
   ```python
   @pytest.fixture
   def client():
       return GeminiClient(project_id="test-project")
   
   def test_with_fixture(client):
       result = client.method()
       assert result
   ```

## Documentation

### Docstring Format

We use Google-style docstrings:

```python
def function_name(param1: str, param2: int) -> bool:
    """Short description of function.

    Longer description if needed.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ValueError: Description of when this error occurs
    """
```

### README Updates

If you change functionality, remember to update:
1. README.md for user-facing changes
2. USAGE.md for detailed API changes
3. Docstrings in the code
4. Example files if relevant

## Code Style

We follow PEP 8 with these additional rules:
- Line length: 88 characters (compatible with black)
- Use type hints for function arguments and return values
- Use descriptive variable names
- Add comments for complex logic

## Pull Request Process

1. Update the README.md with details of changes to the interface
2. Update the USAGE.md with any new features or API changes
3. The PR must pass all tests and maintain code coverage
4. The PR must be reviewed by at least one maintainer
5. Follow the PR template structure

## Issue Reporting

### Bug Reports

When filing an issue, make sure to answer these questions:

1. What version of Python are you using?
2. What operating system are you using?
3. What did you do?
4. What did you expect to see?
5. What did you see instead?

### Feature Requests

Please provide:

1. A clear use case for the feature
2. Expected behavior
3. Example code if possible

## License

By contributing, you agree that your contributions will be licensed under the Apache 2.0 License. 