#!/usr/bin/env python3
"""
Tests for the Food Truck CLI
"""

import subprocess

import pytest

# Mark all unit tests
pytestmark = pytest.mark.unit


def test_cli_runs(cli_command, project_root):
    """Test that the CLI runs without errors"""
    result = subprocess.run(
        cli_command, capture_output=True, text=True, cwd=project_root
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
        [*cli_command, "--help"], capture_output=True, text=True, cwd=project_root
    )

    assert result.returncode == 0, (
        f"CLI help failed with return code {result.returncode}"
    )
    assert "Food Truck Development CLI" in result.stdout, "Expected CLI help not found"


def test_setup_command_help(cli_command, project_root):
    """Test that the setup command shows help information"""
    result = subprocess.run(
        [*cli_command, "setup", "--help"],
        capture_output=True,
        text=True,
        cwd=project_root,
    )

    assert result.returncode == 0, (
        f"Setup help failed with return code {result.returncode}"
    )
    assert "setup" in result.stdout, "Expected setup help not found"


def test_setup_subcommands_help(cli_command, project_root):
    """Test that setup subcommands show help information"""
    # Test setup api subcommand
    result = subprocess.run(
        [*cli_command, "setup", "api", "--help"],
        capture_output=True,
        text=True,
        cwd=project_root,
    )

    assert result.returncode == 0, (
        f"Setup api help failed with return code {result.returncode}"
    )
    assert "api" in result.stdout, "Expected setup api help not found"

    # Test setup website subcommand
    result = subprocess.run(
        [*cli_command, "setup", "website", "--help"],
        capture_output=True,
        text=True,
        cwd=project_root,
    )

    assert result.returncode == 0, (
        f"Setup website help failed with return code {result.returncode}"
    )
    assert "website" in result.stdout, "Expected setup website help not found"

    # Test setup all subcommand
    result = subprocess.run(
        [*cli_command, "setup", "all", "--help"],
        capture_output=True,
        text=True,
        cwd=project_root,
    )

    assert result.returncode == 0, (
        f"Setup all help failed with return code {result.returncode}"
    )
    assert "all" in result.stdout, "Expected setup all help not found"


def test_api_command_help(cli_command, project_root):
    """Test that the api command shows help information"""
    result = subprocess.run(
        [*cli_command, "api", "--help"],
        capture_output=True,
        text=True,
        cwd=project_root,
    )

    assert result.returncode == 0, (
        f"API help failed with return code {result.returncode}"
    )
    assert "api" in result.stdout, "Expected API help not found"


def test_api_subcommands_help(cli_command, project_root):
    """Test that api subcommands show help information"""
    # Test api setup subcommand
    result = subprocess.run(
        [*cli_command, "api", "setup", "--help"],
        capture_output=True,
        text=True,
        cwd=project_root,
    )

    assert result.returncode == 0, (
        f"API setup help failed with return code {result.returncode}"
    )
    assert "setup" in result.stdout, "Expected API setup help not found"

    # Test api start subcommand
    result = subprocess.run(
        [*cli_command, "api", "start", "--help"],
        capture_output=True,
        text=True,
        cwd=project_root,
    )

    assert result.returncode == 0, (
        f"API start help failed with return code {result.returncode}"
    )
    assert "start" in result.stdout, "Expected API start help not found"


def test_completion_command_help(cli_command, project_root):
    """Test that the completion command shows help information"""
    result = subprocess.run(
        [*cli_command, "completion", "--help"],
        capture_output=True,
        text=True,
        cwd=project_root,
    )

    assert result.returncode == 0, (
        f"Completion help failed with return code {result.returncode}"
    )
    assert "completion" in result.stdout, "Expected completion help not found"


def test_completion_subcommands_help(cli_command, project_root):
    """Test that completion subcommands show help information"""
    # Test completion install subcommand
    result = subprocess.run(
        [*cli_command, "completion", "install", "--help"],
        capture_output=True,
        text=True,
        cwd=project_root,
    )

    assert result.returncode == 0, (
        f"Completion install help failed with return code {result.returncode}"
    )
    assert "install" in result.stdout, "Expected completion install help not found"

    # Test completion refresh subcommand
    result = subprocess.run(
        [*cli_command, "completion", "refresh", "--help"],
        capture_output=True,
        text=True,
        cwd=project_root,
    )

    assert result.returncode == 0, (
        f"Completion refresh help failed with return code {result.returncode}"
    )
    assert "refresh" in result.stdout, "Expected completion refresh help not found"


def test_check_command_help(cli_command, project_root):
    """Test that the check command shows help information"""
    result = subprocess.run(
        [*cli_command, "check", "--help"],
        capture_output=True,
        text=True,
        cwd=project_root,
    )

    assert result.returncode == 0, (
        f"Check help failed with return code {result.returncode}"
    )
    assert "check" in result.stdout, "Expected check help not found"
