"""API command implementation functions."""

import sys

from ...utils.console import (
    print_error,
    print_info,
    print_success,
    print_warning,
)
from .api import (
    exec_api_command,
    get_api_logs,
    get_api_status,
    restart_api_service,
    run_migration,
    start_api_service,
    stop_api_service,
)


def api_setup_command() -> None:
    """Setup API project."""
    # For now, setup might just involve starting the service or checking status
    print_info("Setting up API project...")
    result = start_api_service()
    if result.success:
        print_success(result.message)
    else:
        print_error(result.message)
        if result.details:
            print_error(f"Details: {result.details}")
        sys.exit(1)


def api_install_command() -> None:
    """Install API dependencies."""
    print_info("Installing API dependencies...")
    # This could be expanded if there are specific install steps
    result = start_api_service()  # Starting will install dependencies if needed
    if result.success:
        print_success(result.message)
    else:
        print_error(result.message)
        if result.details:
            print_error(f"Details: {result.details}")
        sys.exit(1)


def api_start_command(build: bool = False) -> None:
    """Start API services.

    Args:
        build: If True, rebuild the Docker image before starting the service.
    """
    print_info("Starting API services...")
    result = start_api_service(build=build)
    if result.success:
        print_success(result.message)
        print_info("Expected Service URLs:")
        print_info("  - API Documentation: http://localhost:3000/docs")
        print_info("  - API ReDoc: http://localhost:3000/redoc")
        print_info("Note: Service may take a moment to fully start up.")
        print_info("Check status with: foodtruck api status")
    else:
        print_error(result.message)
        if result.details:
            print_error(f"Details: {result.details}")
        sys.exit(1)


def api_stop_command() -> None:
    """Stop API services."""
    print_info("Stopping API services...")
    result = stop_api_service()
    if result.success:
        print_success(result.message)
    else:
        print_error(result.message)
        if result.details:
            print_error(f"Details: {result.details}")
        sys.exit(1)


def api_restart_command() -> None:
    """Restart API services."""
    print_info("Restarting API services...")
    result = restart_api_service()
    if result.success:
        print_success(result.message)
    else:
        print_error(result.message)
        if result.details:
            print_error(f"Details: {result.details}")
        sys.exit(1)


def api_status_command() -> None:
    """Check API service status."""
    print_info("Checking API service status...")
    status = get_api_status()
    if status.is_running:
        pid_text = f" with PID {status.pid}" if status.pid is not None else ""
        print_success(f"API service is running on port {status.port}{pid_text}")
    else:
        print_warning("API service is not running")
        print_info("Start it with: foodtruck api start")


def api_logs_command(lines: int = 50, follow: bool = False) -> None:
    """Show API service logs.

    Args:
        lines: Number of lines to retrieve (default: 50)
        follow: If True, follow logs in real-time (default: False)
    """
    print_info("Showing API service logs...")
    result = get_api_logs(lines, follow)
    if result.success:
        print_success(result.message)
        if result.details:
            print(result.details)
    else:
        print_error(result.message)
        if result.details:
            print_error(f"Details: {result.details}")
        sys.exit(1)


def api_exec_command(command: list[str]) -> None:
    """Execute a command within the API container."""
    print_info("Executing command in API container...")
    result = exec_api_command(command)
    if result.success:
        print_success(result.message)
        if result.details:
            print(result.details)
    else:
        print_error(result.message)
        if result.details:
            print_error(f"Details: {result.details}")
        sys.exit(1)


def api_migrate_command() -> None:
    """Run database migrations in the API container."""
    print_info("Running database migrations...")
    result = run_migration()
    if result.success:
        print_success(result.message)
        if result.details:
            print(result.details)
    else:
        print_error(result.message)
        if result.details:
            print_error(f"Details: {result.details}")
        sys.exit(1)
