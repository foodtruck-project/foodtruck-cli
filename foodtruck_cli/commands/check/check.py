"""Core dependency checking logic for Food Truck CLI."""

import sys

from ...utils.run_command import run_command
from .models import CheckResult, DependencyStatus


def check_python_version() -> DependencyStatus:
    """Check if Python 3.13 is available."""
    result = run_command([sys.executable, "--version"], timeout=30)

    if not result.success:
        return DependencyStatus(
            False, f"Python not found or not executable: {result.stderr}"
        )

    # Check if it's Python 3.13
    if "Python 3.13" in result.stdout:
        return DependencyStatus(True, result.stdout)
    return DependencyStatus(
        False, f"Found {result.stdout}, but Python 3.13 is required"
    )


def check_uv() -> DependencyStatus:
    """Check if UV is installed and working."""
    result = run_command(["uv", "--version"], timeout=30)

    if not result.success:
        if "not found" in result.stderr:
            return DependencyStatus(False, "UV not installed")
        return DependencyStatus(False, f"UV error: {result.stderr}")

    return DependencyStatus(True, result.stdout)


def check_git() -> DependencyStatus:
    """Check if Git is installed and working."""
    result = run_command(["git", "--version"], timeout=30)

    if not result.success:
        if "not found" in result.stderr:
            return DependencyStatus(False, "Git not installed")
        return DependencyStatus(False, f"Git error: {result.stderr}")

    return DependencyStatus(True, result.stdout)


def check_docker() -> DependencyStatus:
    """Check if Docker is installed and working."""
    result = run_command(["docker", "--version"], timeout=30)

    if not result.success:
        if "not found" in result.stderr:
            return DependencyStatus(False, "Docker not installed")
        return DependencyStatus(False, f"Docker error: {result.stderr}")

    return DependencyStatus(True, result.stdout)


def check_docker_daemon() -> DependencyStatus:
    """Check if Docker daemon is running."""
    result = run_command(["docker", "info"], timeout=30)

    if not result.success:
        if "Cannot connect" in result.stderr or "daemon" in result.stderr.lower():
            return DependencyStatus(False, "Docker daemon is not running")
        return DependencyStatus(False, f"Docker daemon error: {result.stderr}")

    return DependencyStatus(True, "Docker daemon is running")


def perform_dependency_checks() -> CheckResult:
    """Perform all dependency checks and return results."""
    dependency_results = {
        "Python 3.13": check_python_version(),
        "UV": check_uv(),
        "Git": check_git(),
        "Docker": check_docker(),
        "Docker Daemon": check_docker_daemon(),
    }

    return CheckResult.from_results(dependency_results)
