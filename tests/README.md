# Food Truck CLI Tests

This directory contains the test suite for the Food Truck CLI.

## Test Structure

- `test_foodtruck.py` - Main test file containing CLI functionality tests
- `test_install.py` - Tests for the Python installer script (cross-platform)
- `test_windows_simple.py` - Windows-specific installation tests
- `conftest.py` - Pytest configuration and shared fixtures
- `__init__.py` - Makes this directory a Python package

## Running Tests

### Using pytest (recommended)
```bash
# Run all tests
pytest tests/

# Run with verbose output
pytest -v tests/

# Run a specific test
pytest tests/test_foodtruck.py::test_cli_runs
```

### Running directly
```bash
# Run the test file directly
python tests/test_foodtruck.py
```

## Test Coverage

The current test suite covers:
- CLI basic functionality
- Main function execution
- Help command functionality
- Installer script functionality (cross-platform support)
- Windows-specific installation verification

## Adding New Tests

When adding new tests:
1. Follow the naming convention `test_*.py`
2. Use pytest fixtures from `conftest.py` when possible
3. Add descriptive docstrings to test functions
4. Ensure tests can run both with pytest and directly
