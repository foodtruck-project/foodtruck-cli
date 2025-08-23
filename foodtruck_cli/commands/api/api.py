"""
API command for Food Truck CLI
"""

import subprocess
import sys
from pathlib import Path

from cyclopts import App

from ...utils.console import (
    print_command,
    print_error,
    print_info,
    print_newline,
    print_separator,
    print_step,
    print_subtitle,
    print_success,
    print_title,
    print_warning,
)
from ...utils.run_command import run_command


def find_api_project() -> Path | None:
    """Find the API project directory."""
    # Check current directory and parent directories
    current = Path.cwd()

    # Check if we're already in the API project
    if (current / "pyproject.toml").exists() and (
        current / "docker-compose.yaml"
    ).exists():
        return current

    # Check for foodtruck-api directory
    api_paths = [
        current / "foodtruck-api",
        current / "foodtruck" / "foodtruck-api",
        current.parent / "foodtruck-api",
        current.parent / "foodtruck" / "foodtruck-api",
    ]

    for api_path in api_paths:
        if api_path.exists() and (api_path / "pyproject.toml").exists():
            return api_path

    return None


def setup_venv(api_path: Path) -> bool:
    """Create a virtual environment for the API project."""
    print_step("Creating virtual environment...")

    venv_path = api_path / ".venv"

    if venv_path.exists():
        print_warning("Virtual environment already exists. Skipping creation.")
        return True

    # Create virtual environment using uv
    if not run_command(["uv", "venv"], cwd=api_path):
        print_error("Failed to create virtual environment.")
        return False

    print_success("Virtual environment created successfully!")
    return True


def install_dependencies(api_path: Path) -> bool:
    """Install API dependencies using uv."""
    print_step("Installing dependencies...")

    # Sync dependencies using uv
    if not run_command(["uv", "sync"], cwd=api_path):
        print_error("Failed to install dependencies.")
        return False

    print_success("Dependencies installed successfully!")
    return True


def run_docker_compose(api_path: Path, build: bool = False) -> bool:
    """Run Docker Compose for the API project."""
    print_step("Starting Docker Compose services...")

    # Check if docker-compose.yaml exists
    compose_file = api_path / "docker-compose.yaml"
    if not compose_file.exists():
        print_error("docker-compose.yaml not found in API project.")
        return False

    # Build and start services
    cmd = ["docker", "compose", "up", "-d"]
    if build:
        cmd.append("--build")

    if not run_command(cmd, cwd=api_path, show_output=False):
        print_error("Failed to start Docker Compose services.")
        return False

    print_success("Docker Compose services started successfully!")
    return True


def stop_docker_compose(api_path: Path) -> bool:
    """Stop Docker Compose services."""
    print_step("Stopping Docker Compose services...")

    if not run_command(["docker", "compose", "down"], cwd=api_path, show_output=False):
        print_error("Failed to stop Docker Compose services.")
        return False

    print_success("Docker Compose services stopped successfully!")
    return True


def show_status(api_path: Path) -> bool:
    """Show Docker Compose service status."""
    print_step("Checking service status...")

    result = subprocess.run(
        ["docker", "compose", "ps"],
        cwd=api_path,
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode == 0:
        print_info("Service Status:")
        print(result.stdout)
        return True
    else:
        print_error("Failed to get service status.")
        return False


def _get_api_project() -> Path:
    """Get and validate API project path"""
    print_title("Food Truck API Management")
    print_separator()

    # Find API project
    api_path = find_api_project()
    if not api_path:
        print_error("API project not found.")
        print_info(
            "Please run this command from the API project directory or a parent directory."
        )
        print_info("Expected locations:")
        print_info("  - ./foodtruck-api/")
        print_info("  - ./foodtruck/foodtruck-api/")
        print_info("  - ../foodtruck-api/")
        sys.exit(1)

    print_info(f"Found API project at: {api_path}")
    print_newline()

    return api_path


def api_setup_command() -> None:
    """Setup API project"""
    api_path = _get_api_project()

    print_subtitle("Setting up API project...")
    success = setup_venv(api_path) and install_dependencies(api_path)

    if success:
        print_newline()
        print_success("API project setup completed!")
        print_info("Next steps:")
        print_command("  foodtruck api start --build  # Start with Docker Compose")
        print_command("  foodtruck api status         # Check service status")
    else:
        print_newline()
        print_error("API setup failed. Please check the errors above.")
        sys.exit(1)


def api_install_command() -> None:
    """Install API dependencies"""
    api_path = _get_api_project()

    print_subtitle("Installing API dependencies...")
    success = setup_venv(api_path) and install_dependencies(api_path)

    if success:
        print_newline()
        print_success("Dependencies installed successfully!")
    else:
        print_newline()
        print_error("API install failed. Please check the errors above.")
        sys.exit(1)


def api_start_command(build: bool = False) -> None:
    """Start API services"""
    api_path = _get_api_project()

    print_subtitle("Starting API services...")
    success = run_docker_compose(api_path, build=build)

    if success:
        print_newline()
        print_success("API services started!")
        print_info("Expected Service URLs:")
        print_info("  - API Documentation: http://localhost:8000/docs")
        print_info("  - API ReDoc: http://localhost:8000/redoc")
        print_info("  - Traefik Dashboard: http://localhost:8080")
        print_info("  - API (via Traefik): http://foodtruck.docker.localhost")
        print_info("  - PostgreSQL: localhost:5432")
        print_info("  - Redis: localhost:6379")
        print_newline()
        print_info("Note: Services may take a moment to fully start up.")
        print_info("Check status with: foodtruck api status")
    else:
        print_newline()
        print_error("API start failed. Please check the errors above.")
        sys.exit(1)


def api_stop_command() -> None:
    """Stop API services"""
    api_path = _get_api_project()

    print_subtitle("Stopping API services...")
    success = stop_docker_compose(api_path)

    if not success:
        print_newline()
        print_error("API stop failed. Please check the errors above.")
        sys.exit(1)


def api_status_command() -> None:
    """Check API service status"""
    api_path = _get_api_project()

    print_subtitle("Checking API service status...")
    success = show_status(api_path)

    if not success:
        print_newline()
        print_error("API status check failed. Please check the errors above.")
        sys.exit(1)


def api_logs_command(follow: bool = False) -> None:
    """Show API service logs"""
    api_path = _get_api_project()

    print_subtitle("Showing API service logs...")
    cmd = ["docker", "compose", "logs"]
    if follow:
        cmd.append("-f")

    # For logs, we want to see the output directly
    try:
        subprocess.run(cmd, cwd=api_path, check=True)
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to show logs: {e}")
        sys.exit(1)


# Create API sub-app
api_app = App(name="api", help="Manage the Food Truck API project")


@api_app.command
def setup():
    """Setup API project"""
    api_setup_command()


@api_app.command
def install():
    """Install API dependencies"""
    api_install_command()


@api_app.command
def start(build: bool = False):
    """Start API services"""
    api_start_command(build)


@api_app.command
def stop():
    """Stop API services"""
    api_stop_command()


@api_app.command
def status():
    """Check API service status"""
    api_status_command()


@api_app.command
def logs(follow: bool = False):
    """Show API service logs"""
    api_logs_command(follow)


def api_command() -> None:
    """Manage the Food Truck API project"""
    api_app()
