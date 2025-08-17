#!/usr/bin/env python3
"""
Simple tests for the Food Truck CLI
"""

import subprocess
from pathlib import Path


def test_cli_runs():
    """Test that the CLI runs without errors"""
    result = subprocess.run(
        ["uv", "run", "foodtruck"],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent
    )

    assert result.returncode == 0, f"CLI failed with return code {result.returncode}"
    assert "Hello from foodtruck-cli!" in result.stdout, "Expected output not found"


def test_main_function():
    """Test the main function directly"""
    from foodtruck_cli.main import main
    main()


if __name__ == "__main__":
    print("🧪 Running Food Truck CLI tests...")
    test_cli_runs()
    test_main_function()
    print("🎉 All tests passed!")
