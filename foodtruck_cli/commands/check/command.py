"""Check command implementation functions."""

import sys

from ...utils.console import (
    print_error,
    print_info,
    print_newline,
    print_separator,
    print_success,
    print_title,
    print_warning,
)
from .check import perform_dependency_checks
from .models import DependencyStatus


def print_dependency_status(name: str, status: DependencyStatus) -> None:
    """Print the status of a dependency."""
    if status.is_ok:
        print_success(f"{name}: {status.message}")
    else:
        print_error(f"{name}: {status.message}")


def print_installation_guides() -> None:
    """Print installation guides for missing dependencies."""
    print_info("Installation guides:")
    print_info("  • Python 3.13: https://www.python.org/downloads/")
    print_info("  • UV: https://docs.astral.sh/uv/getting-started/installation/")
    print_info("  • Git: https://git-scm.com/downloads")
    print_info("  • Docker: https://docs.docker.com/get-docker/")


def check_dependencies_command() -> None:
    """Main check dependencies command implementation."""
    print_title("🔍 Checking Dependencies")
    print_info("Verifying all required tools are installed and working...")
    print_newline()

    # Perform dependency checks
    check_result = perform_dependency_checks()

    # Print individual dependency statuses
    for name, status in check_result.results.items():
        print_dependency_status(name, status)

    print_newline()
    print_separator()

    if check_result.all_ok:
        print_success("✅ All dependencies are properly installed and working!")
        print_info("You're ready to use Food Truck CLI!")
    else:
        print_warning("⚠️  Some dependencies are missing or not working properly.")
        print_info(
            "Please install the missing dependencies before using Food Truck CLI."
        )
        print_newline()
        print_installation_guides()

        # Exit with error code for CI/CD integration
        sys.exit(1)
