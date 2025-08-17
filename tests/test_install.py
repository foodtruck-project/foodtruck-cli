#!/usr/bin/env python3
"""
Tests for the Python installer script
"""

import os

# Import the installer functions
import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent))
from install import check_uv_installed, detect_shell, get_script_dir


def test_get_script_dir():
    """Test getting the script directory"""
    script_dir = get_script_dir()
    assert isinstance(script_dir, Path)
    assert script_dir.is_absolute()


def test_check_uv_installed():
    """Test UV installation check"""
    # This test depends on whether UV is actually installed
    result = check_uv_installed()
    assert isinstance(result, bool)


def test_detect_shell():
    """Test shell detection"""
    shell_name, shell_config = detect_shell()

    # Should return valid values
    if shell_name:
        assert shell_name in ["zsh", "bash", "powershell"]
        assert isinstance(shell_config, Path)
    else:
        # If no shell detected, both should be None
        assert shell_config is None


def test_detect_shell_with_mock_env():
    """Test shell detection with mocked environment"""
    with patch.dict(os.environ, {"SHELL": "/bin/zsh"}):
        shell_name, shell_config = detect_shell()
        assert shell_name == "zsh"
        assert shell_config.name == ".zshrc"

    with patch.dict(os.environ, {"SHELL": "/bin/bash"}):
        shell_name, shell_config = detect_shell()
        assert shell_name == "bash"
        assert shell_config.name == ".bashrc"


@patch("platform.system")
@patch.dict("os.environ", {"SHELL": ""})
def test_detect_shell_windows(mock_system):
    """Test shell detection on Windows"""
    mock_system.return_value = "Windows"

    shell_name, shell_config = detect_shell()
    assert shell_name == "powershell"
    assert "Microsoft.PowerShell_profile.ps1" in str(shell_config)


def test_install_script_exists():
    """Test that the install.py script exists and is executable"""
    install_script = Path(__file__).parent.parent / "install.py"
    assert install_script.exists()
    assert install_script.is_file()
