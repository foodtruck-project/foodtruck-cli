# Food Truck CLI Tests

This directory contains comprehensive tests for the Food Truck CLI project.

## Test Structure

### Unit Tests (Mocked)
- **`test_foodtruck.py`** - Basic CLI functionality tests
- **`test_install.py`** - Installer script tests (mocked)
- **`test_windows_simple.py`** - Windows-specific installer tests (mocked)
- **`test_check.py`** - Check command tests (mocked)

### Integration Tests (Real System Calls)
- **`test_check_integration.py`** - Real dependency checks on actual system

## Running Tests

### All Tests
```bash
uv run task test
```

### Specific Test Files
```bash
# Unit tests only
uv run pytest tests/test_check.py

# Integration tests only
uv run pytest tests/test_check_integration.py

# Installer tests
uv run pytest tests/test_install.py
```

### Platform-Specific Tests

The integration tests use pytest decorators to run only on specific platforms:

#### Linux Tests
```bash
# Run only Linux tests
uv run pytest tests/test_check_integration.py -k "linux" -v
```

#### Windows Tests (skipped on Linux)
```bash
# This will be skipped on Linux
uv run pytest tests/test_check_integration.py -k "windows" -v
```

#### macOS Tests (skipped on Linux)
```bash
# This will be skipped on Linux
uv run pytest tests/test_check_integration.py -k "macos" -v
```

### Cross-Platform Tests
```bash
# Run tests that work on all platforms
uv run pytest tests/test_check_integration.py::TestCrossPlatformIntegration -v
```

## Test Coverage

### Unit Tests (Mocked)
- ✅ **22 tests** for check command functionality
- ✅ **5 tests** for CLI integration
- ✅ **7 tests** for installer functionality
- ✅ **5 tests** for Windows installer
- **Total: 39 unit tests**

### Integration Tests (Real System)
- ✅ **13 tests** for Linux (real system calls)
- ⏭️ **11 tests** skipped (Windows/macOS specific)
- **Total: 24 integration tests**

### Complete Test Suite
- **67 total tests** (56 passed, 11 skipped on Linux)

## Test Types Explained

### Unit Tests with Mocks
```python
# Tests YOUR code logic, but mocks external dependencies
with patch("subprocess.run") as mock_run:
    mock_run.return_value = Mock(stdout="uv 0.8.8\n")
    result = check_uv()  # Your real function
    assert result[0] is True  # Tests your logic
```

**Pros:**
- Fast and reliable
- Tests your code logic
- Can test error scenarios easily

**Cons:**
- Doesn't test real system integration
- Might miss real-world issues

### Integration Tests (Real System)
```python
# Tests YOUR code + REAL system dependencies
@pytest.mark.skipif(platform.system() != "Linux", reason="Linux only")
def test_check_uv_linux():
    result = check_uv()  # Actually runs "uv --version"
    if result[0]:
        assert "uv" in result[1]  # Real UV output
```

**Pros:**
- Tests real system integration
- Catches real-world issues
- Verifies actual tool availability

**Cons:**
- Slower (real system calls)
- Depends on system state
- May fail if tools aren't installed

## Platform-Specific Testing

### Pytest Decorators Used

```python
# Linux only
@pytest.mark.skipif(platform.system() != "Linux", reason="Linux only")

# Windows only  
@pytest.mark.skipif(platform.system() != "Windows", reason="Windows only")

# macOS only
@pytest.mark.skipif(platform.system() != "Darwin", reason="macOS only")

# Skip Windows, run on Unix-like systems
@pytest.mark.skipif(platform.system() == "Windows", reason="Unix-like only")

# Skip Unix-like, run on Windows
@pytest.mark.skipif(platform.system() != "Windows", reason="Windows only")
```

### Running Platform-Specific Tests

```bash
# Run only tests that work on current platform
uv run pytest tests/test_check_integration.py -v

# Force run all tests (will skip platform-specific ones)
uv run pytest tests/test_check_integration.py --tb=short

# Run specific platform tests (will be skipped if not on that platform)
uv run pytest tests/test_check_integration.py -k "windows" -v
```

## Adding New Tests

### For Unit Tests
1. Add to existing test files or create new ones
2. Use `unittest.mock.patch` for external dependencies
3. Test your logic, not external tools

### For Integration Tests
1. Add to `test_check_integration.py`
2. Use platform decorators for platform-specific tests
3. Handle cases where tools might not be installed
4. Test real system integration

### Example: Adding a New Dependency Check

```python
# Unit test (mocked)
def test_check_new_tool():
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = Mock(stdout="tool v1.0\n")
        result = check_new_tool()
        assert result[0] is True

# Integration test (real)
@pytest.mark.skipif(platform.system() != "Linux", reason="Linux only")
def test_check_new_tool_linux():
    result = check_new_tool()  # Real system call
    if result[0]:
        assert "tool" in result[1]
    else:
        assert "not installed" in result[1]
```

## Best Practices

1. **Always have both unit and integration tests**
2. **Use platform decorators for system-specific tests**
3. **Handle missing tools gracefully in integration tests**
4. **Keep unit tests fast and reliable**
5. **Use integration tests to catch real-world issues**
