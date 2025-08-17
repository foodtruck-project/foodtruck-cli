"""Integration tests for the check command - tests with real system calls."""

import platform
import subprocess
import sys

import pytest

from foodtruck_cli.commands.check import (
    check_docker,
    check_docker_daemon,
    check_git,
    check_python_version,
    check_uv,
)

# Mark all integration tests for easy skipping
pytestmark = pytest.mark.integration


class TestCheckPythonVersionIntegration:
    """Integration tests for Python version checking."""

    @pytest.mark.skipif(platform.system() != "Linux", reason="Test only runs on Linux")
    def test_check_python_version_linux(self):
        """Test Python version check on Linux."""
        result, message = check_python_version()

        # Should always pass on Linux since we're running Python
        assert result is True
        assert "Python" in message
        assert platform.python_version() in message

    @pytest.mark.skipif(
        platform.system() != "Windows", reason="Test only runs on Windows"
    )
    def test_check_python_version_windows(self):
        """Test Python version check on Windows."""
        result, message = check_python_version()

        # Should always pass on Windows since we're running Python
        assert result is True
        assert "Python" in message
        assert platform.python_version() in message

    @pytest.mark.skipif(platform.system() != "Darwin", reason="Test only runs on macOS")
    def test_check_python_version_macos(self):
        """Test Python version check on macOS."""
        result, message = check_python_version()

        # Should always pass on macOS since we're running Python
        assert result is True
        assert "Python" in message
        assert platform.python_version() in message


class TestCheckUVIntegration:
    """Integration tests for UV checking."""

    @pytest.mark.skipif(platform.system() != "Linux", reason="Test only runs on Linux")
    def test_check_uv_linux(self):
        """Test UV check on Linux."""
        result, message = check_uv()

        # This will pass if UV is installed, fail if not
        if result:
            assert "uv" in message.lower()
            # UV output format is "uv 0.8.8" (no "version" word)
        else:
            assert "not installed" in message or "not found" in message

    @pytest.mark.skipif(
        platform.system() != "Windows", reason="Test only runs on Windows"
    )
    def test_check_uv_windows(self):
        """Test UV check on Windows."""
        result, message = check_uv()

        # This will pass if UV is installed, fail if not
        if result:
            assert "uv" in message.lower()
            # UV output format is "uv 0.8.8" (no "version" word)
        else:
            assert "not installed" in message or "not found" in message

    @pytest.mark.skipif(platform.system() != "Darwin", reason="Test only runs on macOS")
    def test_check_uv_macos(self):
        """Test UV check on macOS."""
        result, message = check_uv()

        # This will pass if UV is installed, fail if not
        if result:
            assert "uv" in message.lower()
            # UV output format is "uv 0.8.8" (no "version" word)
        else:
            assert "not installed" in message or "not found" in message


class TestCheckGitIntegration:
    """Integration tests for Git checking."""

    @pytest.mark.skipif(platform.system() != "Linux", reason="Test only runs on Linux")
    def test_check_git_linux(self):
        """Test Git check on Linux."""
        result, message = check_git()

        # Git is usually installed on Linux
        if result:
            assert "git" in message.lower()
            assert "version" in message.lower()
        else:
            assert "not installed" in message or "not found" in message

    @pytest.mark.skipif(
        platform.system() != "Windows", reason="Test only runs on Windows"
    )
    def test_check_git_windows(self):
        """Test Git check on Windows."""
        result, message = check_git()

        # Git might not be installed on Windows
        if result:
            assert "git" in message.lower()
            assert "version" in message.lower()
        else:
            assert "not installed" in message or "not found" in message

    @pytest.mark.skipif(platform.system() != "Darwin", reason="Test only runs on macOS")
    def test_check_git_macos(self):
        """Test Git check on macOS."""
        result, message = check_git()

        # Git is usually installed on macOS
        if result:
            assert "git" in message.lower()
            assert "version" in message.lower()
        else:
            assert "not installed" in message or "not found" in message


class TestCheckDockerIntegration:
    """Integration tests for Docker checking."""

    @pytest.mark.skipif(platform.system() != "Linux", reason="Test only runs on Linux")
    def test_check_docker_linux(self):
        """Test Docker check on Linux."""
        result, message = check_docker()

        # Docker might or might not be installed
        if result:
            assert "docker" in message.lower()
            assert "version" in message.lower()
        else:
            assert "not installed" in message or "not found" in message

    @pytest.mark.skipif(
        platform.system() != "Windows", reason="Test only runs on Windows"
    )
    def test_check_docker_windows(self):
        """Test Docker check on Windows."""
        result, message = check_docker()

        # Docker might or might not be installed
        if result:
            assert "docker" in message.lower()
            assert "version" in message.lower()
        else:
            assert "not installed" in message or "not found" in message

    @pytest.mark.skipif(platform.system() != "Darwin", reason="Test only runs on macOS")
    def test_check_docker_macos(self):
        """Test Docker check on macOS."""
        result, message = check_docker()

        # Docker might or might not be installed
        if result:
            assert "docker" in message.lower()
            assert "version" in message.lower()
        else:
            assert "not installed" in message or "not found" in message


class TestCheckDockerDaemonIntegration:
    """Integration tests for Docker daemon checking."""

    @pytest.mark.skipif(platform.system() != "Linux", reason="Test only runs on Linux")
    def test_check_docker_daemon_linux(self):
        """Test Docker daemon check on Linux."""
        result, message = check_docker_daemon()

        # Docker daemon might or might not be running
        if result:
            assert "docker daemon is running" in message.lower()
        else:
            assert "not running" in message.lower()

    @pytest.mark.skipif(
        platform.system() != "Windows", reason="Test only runs on Windows"
    )
    def test_check_docker_daemon_windows(self):
        """Test Docker daemon check on Windows."""
        result, message = check_docker_daemon()

        # Docker daemon might or might not be running
        if result:
            assert "docker daemon is running" in message.lower()
        else:
            assert "not running" in message.lower()

    @pytest.mark.skipif(platform.system() != "Darwin", reason="Test only runs on macOS")
    def test_check_docker_daemon_macos(self):
        """Test Docker daemon check on macOS."""
        result, message = check_docker_daemon()

        # Docker daemon might or might not be running
        if result:
            assert "docker daemon is running" in message.lower()
        else:
            assert "not running" in message.lower()


class TestSystemCommandsIntegration:
    """Integration tests for actual system commands."""

    @pytest.mark.skipif(platform.system() != "Linux", reason="Test only runs on Linux")
    def test_python_version_command_linux(self):
        """Test actual Python version command on Linux."""
        try:
            result = subprocess.run(
                [sys.executable, "--version"],
                capture_output=True,
                text=True,
                check=True,
            )
            assert result.returncode == 0
            assert "Python" in result.stdout
            assert platform.python_version() in result.stdout
        except subprocess.CalledProcessError:
            pytest.fail("Python version command failed on Linux")

    @pytest.mark.skipif(platform.system() != "Linux", reason="Test only runs on Linux")
    def test_uv_version_command_linux(self):
        """Test actual UV version command on Linux."""
        try:
            result = subprocess.run(
                ["uv", "--version"],
                capture_output=True,
                text=True,
                check=True,
            )
            assert result.returncode == 0
            assert "uv" in result.stdout.lower()
        except (subprocess.CalledProcessError, FileNotFoundError):
            # UV might not be installed, which is fine
            pass

    @pytest.mark.skipif(platform.system() != "Linux", reason="Test only runs on Linux")
    def test_git_version_command_linux(self):
        """Test actual Git version command on Linux."""
        try:
            result = subprocess.run(
                ["git", "--version"],
                capture_output=True,
                text=True,
                check=True,
            )
            assert result.returncode == 0
            assert "git" in result.stdout.lower()
            assert "version" in result.stdout.lower()
        except (subprocess.CalledProcessError, FileNotFoundError):
            # Git might not be installed, which is fine
            pass

    @pytest.mark.skipif(platform.system() != "Linux", reason="Test only runs on Linux")
    def test_docker_version_command_linux(self):
        """Test actual Docker version command on Linux."""
        try:
            result = subprocess.run(
                ["docker", "--version"],
                capture_output=True,
                text=True,
                check=True,
            )
            assert result.returncode == 0
            assert "docker" in result.stdout.lower()
            assert "version" in result.stdout.lower()
        except (subprocess.CalledProcessError, FileNotFoundError):
            # Docker might not be installed, which is fine
            pass

    @pytest.mark.skipif(platform.system() != "Linux", reason="Test only runs on Linux")
    def test_docker_info_command_linux(self):
        """Test actual Docker info command on Linux."""
        try:
            result = subprocess.run(
                ["docker", "info"],
                capture_output=True,
                text=True,
                check=True,
            )
            assert result.returncode == 0
            # Docker info should return some output
            assert len(result.stdout) > 0
        except (subprocess.CalledProcessError, FileNotFoundError):
            # Docker might not be installed or daemon not running, which is fine
            pass


class TestCrossPlatformIntegration:
    """Cross-platform integration tests."""

    def test_python_version_cross_platform(self):
        """Test Python version check works on all platforms."""
        result, message = check_python_version()

        # Should always pass since we're running Python
        assert result is True
        assert "Python" in message
        assert platform.python_version() in message

    def test_platform_detection(self):
        """Test that platform detection works correctly."""
        system = platform.system()
        assert system in ["Linux", "Windows", "Darwin"], (
            f"Unexpected platform: {system}"
        )

    @pytest.mark.skipif(
        platform.system() == "Windows",
        reason="Skip on Windows - test Unix-like systems",
    )
    def test_unix_like_systems(self):
        """Test that works on Unix-like systems (Linux, macOS)."""
        # This test will only run on Linux and macOS
        assert platform.system() in ["Linux", "Darwin"]

    @pytest.mark.skipif(
        platform.system() != "Windows",
        reason="Skip on Unix-like systems - test Windows",
    )
    def test_windows_system(self):
        """Test that works on Windows."""
        # This test will only run on Windows
        assert platform.system() == "Windows"
