"""Tests for the completion command."""

import subprocess
from pathlib import Path

import pytest

from foodtruck_cli.commands.completion import (
    generate_bash_completion,
    generate_powershell_completion,
    generate_zsh_completion,
    get_completion_file_path,
    get_completion_script,
)


def test_generate_bash_completion():
    """Test bash completion script generation."""
    script = generate_bash_completion()

    assert "bash completion for foodtruck" in script
    assert "_foodtruck_completion()" in script
    assert "check setup completion" in script
    assert "--api-repo" in script
    assert "--skip-api" in script


def test_generate_zsh_completion():
    """Test zsh completion script generation."""
    script = generate_zsh_completion()

    assert "zsh completion for foodtruck" in script
    assert "_foodtruck()" in script
    assert "check:Check dependencies" in script
    assert "setup:Setup development environment" in script


def test_generate_powershell_completion():
    """Test PowerShell completion script generation."""
    script = generate_powershell_completion()

    assert "PowerShell completion for foodtruck" in script
    assert "Register-ArgumentCompleter" in script
    assert "check" in script
    assert "setup" in script


def test_get_completion_script():
    """Test getting completion script for different shells."""
    bash_script = get_completion_script("bash")
    zsh_script = get_completion_script("zsh")
    powershell_script = get_completion_script("powershell")

    assert "bash completion for foodtruck" in bash_script
    assert "zsh completion for foodtruck" in zsh_script
    assert "PowerShell completion for foodtruck" in powershell_script

    with pytest.raises(ValueError, match="Unsupported shell"):
        get_completion_script("unsupported")


def test_get_completion_file_path():
    """Test getting completion file paths."""
    home = Path.home()

    bash_path = get_completion_file_path("bash")
    zsh_path = get_completion_file_path("zsh")
    powershell_path = get_completion_file_path("powershell")

    assert bash_path == home / ".local/share/bash-completion/completions/foodtruck"
    assert zsh_path == home / ".zsh/completions/_foodtruck"
    assert powershell_path == home / "Documents/WindowsPowerShell/Microsoft.PowerShell_profile.ps1"

    with pytest.raises(ValueError, match="Unsupported shell"):
        get_completion_file_path("unsupported")


def test_completion_command_integration(cli_command, project_root):
    """Test the completion command integration."""
    result = subprocess.run(
        [*cli_command, "completion", "--help"],
        capture_output=True,
        text=True,
        cwd=project_root,
    )

    assert result.returncode == 0
    assert "Generate shell completion scripts" in result.stdout


def test_completion_command_generate_bash(cli_command, project_root):
    """Test generating bash completion script."""
    result = subprocess.run(
        [*cli_command, "completion", "bash"],
        capture_output=True,
        text=True,
        cwd=project_root,
    )

    assert result.returncode == 0
    assert "bash completion for foodtruck" in result.stdout
    assert "💡 To install, save to:" in result.stdout


def test_completion_command_generate_all(cli_command, project_root):
    """Test generating all completion scripts."""
    result = subprocess.run(
        [*cli_command, "completion"],
        capture_output=True,
        text=True,
        cwd=project_root,
    )

    assert result.returncode == 0
    assert "bash completion for foodtruck" in result.stdout
    assert "zsh completion for foodtruck" in result.stdout
    assert "PowerShell completion for foodtruck" in result.stdout
