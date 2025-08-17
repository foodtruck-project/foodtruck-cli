#!/usr/bin/env python3
"""
Windows installation tests for the installer
Focuses on checking if the app is installed correctly on Windows
"""

import os
import sys
from pathlib import Path
from unittest.mock import mock_open, patch

import pytest

# Mark all unit tests
pytestmark = pytest.mark.unit

# Import the installer functions
sys.path.insert(0, str(Path(__file__).parent.parent))

from install import (  # noqa: E402
    check_uv_installed,
    create_wrapper_script,
    detect_shell,
    install_package,
)


def test_windows_shell_detection():
    """Test Windows shell detection with mocking"""
    with (
        patch("platform.system", return_value="Windows"),
        patch.dict(os.environ, {"SHELL": ""}),
    ):
        shell_name, shell_config = detect_shell()

        assert shell_name == "powershell"
        assert "Microsoft.PowerShell_profile.ps1" in str(shell_config)


def test_windows_wrapper_script():
    """Test Windows batch script creation"""
    with (
        patch("platform.system", return_value="Windows"),
        patch("pathlib.Path.open", new_callable=mock_open) as mock_file,
    ):
        script_dir = Path("C:/foodtruck-cli")
        create_wrapper_script(script_dir)

        # Verify file was opened for writing
        mock_file.assert_called()

        # Verify content contains Windows batch syntax
        write_calls = mock_file.return_value.write.call_args_list
        batch_content = "".join(str(call) for call in write_calls)
        assert "@echo off" in batch_content
        assert "cd /d" in batch_content
        assert "%*" in batch_content


def test_windows_uv_check():
    """Test UV installation check on Windows"""
    with patch("platform.system", return_value="Windows"):
        # Test with UV installed
        with patch("shutil.which", return_value="C:/Users/TestUser/.cargo/bin/uv.exe"):
            result = check_uv_installed()
            assert result is True

        # Test with UV not installed
        with patch("shutil.which", return_value=None):
            result = check_uv_installed()
            assert result is False


def test_windows_installation_complete():
    """Test complete Windows installation process"""
    with (
        patch("platform.system", return_value="Windows"),
        patch.dict(os.environ, {"SHELL": ""}),
        patch("shutil.which", return_value="C:/Users/TestUser/.cargo/bin/uv.exe"),
        patch("pathlib.Path.open", new_callable=mock_open),
        patch("subprocess.run") as mock_run,
    ):
        # Mock successful package installation
        mock_run.return_value.returncode = 0

        # Test shell detection
        shell_name, shell_config = detect_shell()
        assert shell_name == "powershell"

        # Test UV check
        assert check_uv_installed() is True

        # Test package installation
        install_package()
        mock_run.assert_called_with(
            ["uv", "pip", "install", "-e", "."],
            capture_output=True,
            text=True,
            check=True,
        )


def test_windows_installation_without_uv():
    """Test Windows installation when UV is not available"""
    with (
        patch("platform.system", return_value="Windows"),
        patch("shutil.which", return_value=None),
    ):
        # Test UV check
        assert check_uv_installed() is False
