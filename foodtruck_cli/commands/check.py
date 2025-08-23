"""Check command for verifying dependencies."""

import subprocess
import sys

from ..utils.console import (
    print_error,
    print_info,
    print_newline,
    print_separator,
    print_success,
    print_title,
    print_warning,
)


def check_python_version() -> tuple[bool, str]:
    """Check if Python 3.13 is available."""
    try:
        result = subprocess.run(
            [sys.executable, "--version"],
            capture_output=True,
            text=True,
            check=True,
        )
        version = result.stdout.strip()
    except subprocess.CalledProcessError:
        return False, "Python not found or not executable"
    except Exception as e:
        return False, f"Error checking Python: {e}"
    else:
        # Check if it's Python 3.13
        if "Python 3.13" in version:
            return True, version
        return False, f"Found {version}, but Python 3.13 is required"


def check_uv() -> tuple[bool, str]:
    """Check if UV is installed and working."""
    try:
        result = subprocess.run(
            ["uv", "--version"],
            capture_output=True,
            text=True,
            check=True,
        )
        version = result.stdout.strip()
    except subprocess.CalledProcessError:
        return False, "UV not found or not executable"
    except FileNotFoundError:
        return False, "UV not installed"
    except Exception as e:
        return False, f"Error checking UV: {e}"
    else:
        return True, version


def check_git() -> tuple[bool, str]:
    """Check if Git is installed and working."""
    try:
        result = subprocess.run(
            ["git", "--version"],
            capture_output=True,
            text=True,
            check=True,
        )
        version = result.stdout.strip()
    except subprocess.CalledProcessError:
        return False, "Git not found or not executable"
    except FileNotFoundError:
        return False, "Git not installed"
    except Exception as e:
        return False, f"Error checking Git: {e}"
    else:
        return True, version


def check_docker() -> tuple[bool, str]:
    """Check if Docker is installed and working."""
    try:
        result = subprocess.run(
            ["docker", "--version"],
            capture_output=True,
            text=True,
            check=True,
        )
        version = result.stdout.strip()
    except subprocess.CalledProcessError:
        return False, "Docker not found or not executable"
    except FileNotFoundError:
        return False, "Docker not installed"
    except Exception as e:
        return False, f"Error checking Docker: {e}"
    else:
        return True, version


def check_docker_daemon() -> tuple[bool, str]:
    """Check if Docker daemon is running."""
    try:
        subprocess.run(
            ["docker", "info"],
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError:
        return False, "Docker daemon is not running"
    except Exception as e:
        return False, f"Error checking Docker daemon: {e}"
    else:
        return True, "Docker daemon is running"


def check_dependencies() -> dict[str, tuple[bool, str]]:
    """Check all required dependencies."""
    return {
        "Python 3.13": check_python_version(),
        "UV": check_uv(),
        "Git": check_git(),
        "Docker": check_docker(),
        "Docker Daemon": check_docker_daemon(),
    }


def print_dependency_status(name: str, status: tuple[bool, str]) -> None:
    """Print the status of a dependency."""
    is_ok, message = status

    if is_ok:
        print_success(f"{name}: {message}")
    else:
        print_error(f"{name}: {message}")


def check_command() -> None:
    """Check command implementation."""
    print_title("🔍 Checking Dependencies")
    print_info("Verifying all required tools are installed and working...")
    print_newline()

    dependencies = check_dependencies()

    all_ok = True
    for name, status in dependencies.items():
        is_ok, _ = status
        if not is_ok:
            all_ok = False
        print_dependency_status(name, status)

    print_newline()
    print_separator()

    if all_ok:
        print_success("✅ All dependencies are properly installed and working!")
        print_info("You're ready to use Food Truck CLI!")
    else:
        print_warning("⚠️  Some dependencies are missing or not working properly.")
        print_info(
            "Please install the missing dependencies before using Food Truck CLI."
        )
        print_newline()
        print_info("Installation guides:")
        print_info("  • Python 3.13: https://www.python.org/downloads/")
        print_info("  • UV: https://docs.astral.sh/uv/getting-started/installation/")
        print_info("  • Git: https://git-scm.com/downloads")
        print_info("  • Docker: https://docs.docker.com/get-docker/")

        # Exit with error code for CI/CD integration
        sys.exit(1)
