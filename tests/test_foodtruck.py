#!/usr/bin/env python3
"""
Tests for the Food Truck CLI
"""

import subprocess


def test_cli_runs(cli_command, project_root):
    """Test that the CLI runs without errors"""
    result = subprocess.run(
        cli_command,
        capture_output=True,
        text=True,
        cwd=project_root
    )

    assert result.returncode == 0, f"CLI failed with return code {result.returncode}"
    assert "Food Truck Development CLI" in result.stdout, "Expected CLI help not found"


def test_main_function():
    """Test the main function directly"""
    from foodtruck_cli.main import app
    # Call with empty args to avoid Cyclopts warning
    app([])


def test_cli_help(cli_command, project_root):
    """Test that the CLI shows help information"""
    result = subprocess.run(
        [*cli_command, "--help"],
        capture_output=True,
        text=True,
        cwd=project_root
    )

    assert result.returncode == 0, f"CLI help failed with return code {result.returncode}"
    assert "Food Truck Development CLI" in result.stdout, "Expected CLI help not found"


def test_setup_command_help(cli_command, project_root):
    """Test that the setup command shows help information"""
    result = subprocess.run(
        [*cli_command, "setup", "--help"],
        capture_output=True,
        text=True,
        cwd=project_root
    )

    assert result.returncode == 0, f"Setup help failed with return code {result.returncode}"
    assert "setup" in result.stdout, "Expected setup help not found"
