"""Tests for the check command."""

import subprocess
import sys
from unittest.mock import Mock, patch

import pytest

from foodtruck_cli.commands.check import (
    check_command,
    check_dependencies,
    check_docker,
    check_docker_daemon,
    check_git,
    check_python_version,
    check_uv,
    print_dependency_status,
)

# Constants
EXPECTED_DEPENDENCIES_COUNT = 5

# Mark all unit tests
pytestmark = pytest.mark.unit


class TestCheckPythonVersion:
    """Test Python version checking."""

    def test_check_python_version_success(self):
        """Test successful Python 3.13 check."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = Mock(
                stdout="Python 3.13.6\n", stderr="", returncode=0
            )
            mock_run.return_value.check.return_value = None

            result, message = check_python_version()

            assert result is True
            assert "Python 3.13.6" in message
            mock_run.assert_called_once_with(
                [sys.executable, "--version"],
                capture_output=True,
                text=True,
                check=True,
            )

    def test_check_python_version_wrong_version(self):
        """Test Python version check with wrong version."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = Mock(
                stdout="Python 3.12.0\n", stderr="", returncode=0
            )
            mock_run.return_value.check.return_value = None

            result, message = check_python_version()

            assert result is False
            assert "Python 3.12.0" in message
            assert "Python 3.13 is required" in message

    def test_check_python_version_subprocess_error(self):
        """Test Python version check with subprocess error."""
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.CalledProcessError(1, "python")

            result, message = check_python_version()

            assert result is False
            assert "not found or not executable" in message

    def test_check_python_version_exception(self):
        """Test Python version check with general exception."""
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = Exception("Test error")

            result, message = check_python_version()

            assert result is False
            assert "Error checking Python" in message


class TestCheckUV:
    """Test UV checking."""

    def test_check_uv_success(self):
        """Test successful UV check."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = Mock(stdout="uv 0.8.8\n", stderr="", returncode=0)
            mock_run.return_value.check.return_value = None

            result, message = check_uv()

            assert result is True
            assert "uv 0.8.8" in message
            mock_run.assert_called_once_with(
                ["uv", "--version"],
                capture_output=True,
                text=True,
                check=True,
            )

    def test_check_uv_subprocess_error(self):
        """Test UV check with subprocess error."""
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.CalledProcessError(1, "uv")

            result, message = check_uv()

            assert result is False
            assert "not found or not executable" in message

    def test_check_uv_file_not_found(self):
        """Test UV check with file not found."""
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = FileNotFoundError()

            result, message = check_uv()

            assert result is False
            assert "not installed" in message

    def test_check_uv_exception(self):
        """Test UV check with general exception."""
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = Exception("Test error")

            result, message = check_uv()

            assert result is False
            assert "Error checking UV" in message


class TestCheckGit:
    """Test Git checking."""

    def test_check_git_success(self):
        """Test successful Git check."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = Mock(
                stdout="git version 2.34.1\n", stderr="", returncode=0
            )
            mock_run.return_value.check.return_value = None

            result, message = check_git()

            assert result is True
            assert "git version 2.34.1" in message
            mock_run.assert_called_once_with(
                ["git", "--version"],
                capture_output=True,
                text=True,
                check=True,
            )

    def test_check_git_subprocess_error(self):
        """Test Git check with subprocess error."""
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.CalledProcessError(1, "git")

            result, message = check_git()

            assert result is False
            assert "not found or not executable" in message

    def test_check_git_file_not_found(self):
        """Test Git check with file not found."""
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = FileNotFoundError()

            result, message = check_git()

            assert result is False
            assert "not installed" in message

    def test_check_git_exception(self):
        """Test Git check with general exception."""
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = Exception("Test error")

            result, message = check_git()

            assert result is False
            assert "Error checking Git" in message


class TestCheckDocker:
    """Test Docker checking."""

    def test_check_docker_success(self):
        """Test successful Docker check."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = Mock(
                stdout="Docker version 28.3.3\n", stderr="", returncode=0
            )
            mock_run.return_value.check.return_value = None

            result, message = check_docker()

            assert result is True
            assert "Docker version 28.3.3" in message
            mock_run.assert_called_once_with(
                ["docker", "--version"],
                capture_output=True,
                text=True,
                check=True,
            )

    def test_check_docker_subprocess_error(self):
        """Test Docker check with subprocess error."""
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.CalledProcessError(1, "docker")

            result, message = check_docker()

            assert result is False
            assert "not found or not executable" in message

    def test_check_docker_file_not_found(self):
        """Test Docker check with file not found."""
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = FileNotFoundError()

            result, message = check_docker()

            assert result is False
            assert "not installed" in message

    def test_check_docker_exception(self):
        """Test Docker check with general exception."""
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = Exception("Test error")

            result, message = check_docker()

            assert result is False
            assert "Error checking Docker" in message


class TestCheckDockerDaemon:
    """Test Docker daemon checking."""

    def test_check_docker_daemon_success(self):
        """Test successful Docker daemon check."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = Mock(stdout="", stderr="", returncode=0)
            mock_run.return_value.check.return_value = None

            result, message = check_docker_daemon()

            assert result is True
            assert "Docker daemon is running" in message
            mock_run.assert_called_once_with(
                ["docker", "info"],
                capture_output=True,
                text=True,
                check=True,
            )

    def test_check_docker_daemon_subprocess_error(self):
        """Test Docker daemon check with subprocess error."""
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.CalledProcessError(1, "docker")

            result, message = check_docker_daemon()

            assert result is False
            assert "not running" in message

    def test_check_docker_daemon_exception(self):
        """Test Docker daemon check with general exception."""
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = Exception("Test error")

            result, message = check_docker_daemon()

            assert result is False
            assert "Error checking Docker daemon" in message


class TestCheckDependencies:
    """Test dependency checking."""

    def test_check_dependencies_all_success(self):
        """Test all dependencies successful."""
        with (
            patch("foodtruck_cli.commands.check.check_python_version") as mock_python,
            patch("foodtruck_cli.commands.check.check_uv") as mock_uv,
            patch("foodtruck_cli.commands.check.check_git") as mock_git,
            patch("foodtruck_cli.commands.check.check_docker") as mock_docker,
            patch(
                "foodtruck_cli.commands.check.check_docker_daemon"
            ) as mock_docker_daemon,
        ):
            mock_python.return_value = (True, "Python 3.13.6")
            mock_uv.return_value = (True, "uv 0.8.8")
            mock_git.return_value = (True, "git version 2.34.1")
            mock_docker.return_value = (True, "Docker version 28.3.3")
            mock_docker_daemon.return_value = (True, "Docker daemon is running")

            result = check_dependencies()

            assert len(result) == EXPECTED_DEPENDENCIES_COUNT
            assert result["Python 3.13"] == (True, "Python 3.13.6")
            assert result["UV"] == (True, "uv 0.8.8")
            assert result["Git"] == (True, "git version 2.34.1")
            assert result["Docker"] == (True, "Docker version 28.3.3")
            assert result["Docker Daemon"] == (True, "Docker daemon is running")

    def test_check_dependencies_some_failures(self):
        """Test some dependencies failing."""
        with (
            patch("foodtruck_cli.commands.check.check_python_version") as mock_python,
            patch("foodtruck_cli.commands.check.check_uv") as mock_uv,
            patch("foodtruck_cli.commands.check.check_git") as mock_git,
            patch("foodtruck_cli.commands.check.check_docker") as mock_docker,
            patch(
                "foodtruck_cli.commands.check.check_docker_daemon"
            ) as mock_docker_daemon,
        ):
            mock_python.return_value = (True, "Python 3.13.6")
            mock_uv.return_value = (False, "UV not installed")
            mock_git.return_value = (True, "git version 2.34.1")
            mock_docker.return_value = (False, "Docker not installed")
            mock_docker_daemon.return_value = (False, "Docker daemon is not running")

            result = check_dependencies()

            assert len(result) == EXPECTED_DEPENDENCIES_COUNT
            assert result["Python 3.13"] == (True, "Python 3.13.6")
            assert result["UV"] == (False, "UV not installed")
            assert result["Git"] == (True, "git version 2.34.1")
            assert result["Docker"] == (False, "Docker not installed")
            assert result["Docker Daemon"] == (False, "Docker daemon is not running")


class TestPrintDependencyStatus:
    """Test dependency status printing."""

    def test_print_dependency_status_success(self):
        """Test printing successful dependency status."""
        with patch("foodtruck_cli.commands.check.print_success") as mock_success:
            print_dependency_status("Test Tool", (True, "Test Tool v1.0"))

            mock_success.assert_called_once_with("Test Tool: Test Tool v1.0")

    def test_print_dependency_status_failure(self):
        """Test printing failed dependency status."""
        with patch("foodtruck_cli.commands.check.print_error") as mock_error:
            print_dependency_status("Test Tool", (False, "Test Tool not found"))

            mock_error.assert_called_once_with("Test Tool: Test Tool not found")


class TestCheckCommand:
    """Test the main check command."""

    def test_check_command_all_success(self):
        """Test check command with all dependencies successful."""
        with (
            patch("foodtruck_cli.commands.check.check_dependencies") as mock_check,
            patch("foodtruck_cli.commands.check.print_title") as mock_title,
            patch("foodtruck_cli.commands.check.print_info") as mock_info,
            patch("foodtruck_cli.commands.check.print_newline"),
            patch("foodtruck_cli.commands.check.print_separator"),
            patch("foodtruck_cli.commands.check.print_success") as mock_success,
            patch(
                "foodtruck_cli.commands.check.print_dependency_status"
            ) as mock_status,
        ):
            mock_check.return_value = {
                "Python 3.13": (True, "Python 3.13.6"),
                "UV": (True, "uv 0.8.8"),
                "Git": (True, "git version 2.34.1"),
                "Docker": (True, "Docker version 28.3.3"),
                "Docker Daemon": (True, "Docker daemon is running"),
            }

            check_command()

            mock_title.assert_called_once_with("🔍 Checking Dependencies")
            mock_info.assert_any_call(
                "Verifying all required tools are installed and working..."
            )
            mock_success.assert_called_with(
                "✅ All dependencies are properly installed and working!"
            )
            assert mock_status.call_count == EXPECTED_DEPENDENCIES_COUNT

    def test_check_command_some_failures(self):
        """Test check command with some dependencies failing."""
        with (
            patch("foodtruck_cli.commands.check.check_dependencies") as mock_check,
            patch("foodtruck_cli.commands.check.print_title") as mock_title,
            patch("foodtruck_cli.commands.check.print_info"),
            patch("foodtruck_cli.commands.check.print_newline"),
            patch("foodtruck_cli.commands.check.print_separator"),
            patch("foodtruck_cli.commands.check.print_warning") as mock_warning,
            patch(
                "foodtruck_cli.commands.check.print_dependency_status"
            ) as mock_status,
            patch("sys.exit") as mock_exit,
        ):
            mock_check.return_value = {
                "Python 3.13": (True, "Python 3.13.6"),
                "UV": (False, "UV not installed"),
                "Git": (True, "git version 2.34.1"),
                "Docker": (False, "Docker not installed"),
                "Docker Daemon": (False, "Docker daemon is not running"),
            }

            check_command()

            mock_title.assert_called_once_with("🔍 Checking Dependencies")
            mock_warning.assert_called_with(
                "⚠️  Some dependencies are missing or not working properly."
            )
            mock_exit.assert_called_once_with(1)
            assert mock_status.call_count == EXPECTED_DEPENDENCIES_COUNT

    def test_check_command_all_failures(self):
        """Test check command with all dependencies failing."""
        with (
            patch("foodtruck_cli.commands.check.check_dependencies") as mock_check,
            patch("foodtruck_cli.commands.check.print_title") as mock_title,
            patch("foodtruck_cli.commands.check.print_info"),
            patch("foodtruck_cli.commands.check.print_newline"),
            patch("foodtruck_cli.commands.check.print_separator"),
            patch("foodtruck_cli.commands.check.print_warning") as mock_warning,
            patch(
                "foodtruck_cli.commands.check.print_dependency_status"
            ) as mock_status,
            patch("sys.exit") as mock_exit,
        ):
            mock_check.return_value = {
                "Python 3.13": (False, "Python not found"),
                "UV": (False, "UV not installed"),
                "Git": (False, "Git not installed"),
                "Docker": (False, "Docker not installed"),
                "Docker Daemon": (False, "Docker daemon is not running"),
            }

            check_command()

            mock_title.assert_called_once_with("🔍 Checking Dependencies")
            mock_warning.assert_called_with(
                "⚠️  Some dependencies are missing or not working properly."
            )
            mock_exit.assert_called_once_with(1)
            assert mock_status.call_count == EXPECTED_DEPENDENCIES_COUNT
