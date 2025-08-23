"""
API command for Food Truck CLI
"""

import time
from contextlib import suppress
from pathlib import Path

from ...utils.console import print_error, print_info, print_success
from ...utils.run_command import run_command
from .models import ApiOperationResult, ApiStatus

API_PROJECT_DIR = Path(__file__).parent.parent.parent / "foodtruck-api"
API_PORT = 3000
DOCKER_COMPOSE_FILE_YML = API_PROJECT_DIR / "docker-compose.yml"
DOCKER_COMPOSE_FILE_YAML = API_PROJECT_DIR / "docker-compose.yaml"


def _create_operation_result(
    success: bool, message: str, details: str = ""
) -> ApiOperationResult:
    """Helper function to create standardized ApiOperationResult."""
    return ApiOperationResult(success=success, message=message, details=details)


def get_api_status() -> ApiStatus:
    """Check if the API service is running within a Docker container and return its status."""
    try:
        # Check if Docker container for API is running
        result = run_command(
            [
                "docker",
                "ps",
                "--filter",
                "name=foodtruck-api",
                "--format",
                "{{.ID}} {{.Status}}",
            ]
        )
        if result.success and result.stdout:
            lines = result.stdout.splitlines()
            if lines:
                container_id = lines[0].split()[0]
                # Extract PID if possible (not directly available from docker ps, so we use inspect)
                pid_result = run_command(
                    ["docker", "inspect", "-f", "{{.State.Pid}}", container_id]
                )
                pid = None
                if pid_result.success and pid_result.stdout:
                    with suppress(ValueError):
                        pid = int(pid_result.stdout.strip())
                return ApiStatus(is_running=True, pid=pid, port=API_PORT)

    except Exception as e:
        print_error(f"Error checking API status: {e}")

    return ApiStatus(is_running=False)


def _check_and_setup_project() -> ApiOperationResult | None:
    """Check if project exists and setup if needed. Returns None if setup successful."""
    if not API_PROJECT_DIR.exists():
        print_info("API project directory not found, setting up the project...")
        setup_result = run_command(
            ["foodtruck", "setup", "api"], cwd=API_PROJECT_DIR.parent
        )
        if not setup_result.success:
            return _create_operation_result(
                False, "Failed to setup API project", setup_result.stderr
            )
        print_success("API project setup completed, proceeding to start the service.")
    return None


def _check_docker_compose_file() -> ApiOperationResult | None:
    """Check if Docker Compose file exists. Returns None if file exists."""
    docker_compose_file = (
        DOCKER_COMPOSE_FILE_YAML
        if DOCKER_COMPOSE_FILE_YAML.exists()
        else DOCKER_COMPOSE_FILE_YML
    )
    if not docker_compose_file.exists():
        return _create_operation_result(
            False, "Docker Compose file not found", str(docker_compose_file)
        )
    return None


def _create_default_env_file() -> ApiOperationResult | None:
    """Create default .env file if it doesn't exist. Returns None if successful."""
    env_file = API_PROJECT_DIR / ".env"
    env_example_file = API_PROJECT_DIR / ".env.example"

    if not env_file.exists():
        print_info(
            ".env file not found, creating a default one with placeholder values..."
        )
        try:
            # TODO: In the future, this will be replaced by fetching environment variables
            # from an AWS S3 bucket or similar service for dynamic configuration management
            if env_example_file.exists():
                # Copy from .env.example if it exists
                with (
                    env_example_file.open("r", encoding="utf-8") as src,
                    env_file.open("w", encoding="utf-8") as dst,
                ):
                    dst.write(src.read())
                print_success(
                    "Default .env file created from .env.example. Please update it with actual values if needed."
                )
            else:
                # Create .env.example with only sensitive settings
                with env_example_file.open("w", encoding="utf-8") as f:
                    f.write("# .env.example - Sensitive settings for foodtruck-api\n")
                    f.write(
                        "# TODO: This will be replaced by dynamic configuration from AWS S3 bucket\n"
                    )
                    f.write(
                        "# Copy this file to .env and update with actual values\n\n"
                    )
                    f.write("# Database credentials\n")
                    f.write("POSTGRES_PASSWORD=your_password_here\n")
                    f.write("POSTGRES_USER=your_username_here\n\n")
                    f.write("# JWT settings\n")
                    f.write("JWT_SECRET_KEY=your_jwt_secret_key_here\n")
                    f.write("JWT_ALGORITHM=HS256\n")
                    f.write("JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30\n")

                # Copy the example to create the actual .env file
                with (
                    env_example_file.open("r", encoding="utf-8") as src,
                    env_file.open("w", encoding="utf-8") as dst,
                ):
                    dst.write(src.read())
                print_success(
                    "Default .env file created from .env.example. Please update it with actual values if needed."
                )
        except Exception as e:
            return _create_operation_result(
                False, "Failed to create default .env file", str(e)
            )
    return None


def _start_docker_compose(build: bool) -> ApiOperationResult:
    """Start Docker Compose service. Returns operation result."""
    print_info("Starting API service using Docker Compose...")
    command = ["docker", "compose", "up", "-d"]
    if build:
        command.append("--build")
    start_result = run_command(command, cwd=API_PROJECT_DIR)
    if not start_result.success:
        return _create_operation_result(
            False, "Failed to start API service", start_result.stderr
        )

    # Wait a few seconds to confirm it started
    time.sleep(3)
    status = get_api_status()
    success = status.is_running
    if status.is_running:
        message = f"API service started successfully on port {status.port}" + (
            f" with PID {status.pid}" if status.pid else ""
        )
        error_msg = ""
    else:
        message = "API service failed to start"
        error_msg = "Process did not start or is not listening on expected port"
    return _create_operation_result(success, message, error_msg)


def start_api_service(build: bool = False) -> ApiOperationResult:
    """Start the API service within a Docker container if it's not already running.

    Args:
        build: If True, rebuild the Docker image before starting the service.
    """
    status = get_api_status()
    if status.is_running:
        return _create_operation_result(
            True,
            f"API service already running on port {status.port}"
            + (f" with PID {status.pid}" if status.pid else ""),
        )

    # Check and setup project if needed
    result = _check_and_setup_project()
    if result is not None:
        return result

    # Check Docker Compose file
    result = _check_docker_compose_file()
    if result is not None:
        return result

    # Create default .env file if needed
    result = _create_default_env_file()
    if result is not None:
        return result

    # Start the service
    try:
        return _start_docker_compose(build)
    except Exception as e:
        return _create_operation_result(
            False, "Unexpected error starting API service", str(e)
        )


def stop_api_service() -> ApiOperationResult:
    """Stop the API service if it's running within a Docker container."""
    status = get_api_status()
    if not status.is_running:
        return _create_operation_result(True, "API service is not running")

    try:
        print_info("Stopping API service...")
        stop_result = run_command(["docker", "compose", "down"], cwd=API_PROJECT_DIR)

        if not stop_result.success:
            return _create_operation_result(
                False, "Failed to stop API service", stop_result.stderr
            )

        # Wait a moment to ensure process terminates
        time.sleep(1)
        updated_status = get_api_status()
        if not updated_status.is_running:
            return _create_operation_result(True, "API service stopped successfully")
        return _create_operation_result(
            False,
            "Failed to stop API service",
            "Container is still running after stop command",
        )

    except Exception as e:
        return _create_operation_result(
            False, "Unexpected error stopping API service", str(e)
        )


def restart_api_service() -> ApiOperationResult:
    """Restart the API service within a Docker container."""
    stop_result = stop_api_service()
    if not stop_result.success:
        return stop_result

    # Wait briefly to ensure the port is released
    time.sleep(2)
    start_result = start_api_service()
    if not start_result.success:
        return start_result

    return _create_operation_result(True, "API service restarted successfully")


def get_api_logs(lines: int = 50, follow: bool = False) -> ApiOperationResult:
    """Get the latest logs from the API service within a Docker container.

    Args:
        lines: Number of lines to retrieve (default: 50)
        follow: If True, follow logs in real-time (default: False)
    """
    status = get_api_status()
    if not status.is_running:
        return _create_operation_result(False, "API service is not running")

    try:
        # Use docker compose logs to get the last N lines
        command = ["docker", "compose", "logs", f"--tail={lines}"]
        if follow:
            command.append("-f")
        result = run_command(command, cwd=API_PROJECT_DIR)
        if result.success:
            return _create_operation_result(
                True, f"Last {lines} lines of API logs", result.stdout
            )
        return _create_operation_result(False, "Failed to retrieve logs", result.stderr)

    except Exception as e:
        return _create_operation_result(
            False, "Unexpected error retrieving API logs", str(e)
        )


def exec_api_command(command: list[str]) -> ApiOperationResult:
    """Execute a command within the running API Docker container."""
    status = get_api_status()
    if not status.is_running:
        return _create_operation_result(False, "API service is not running")

    try:
        print_info(f"Executing command in API container: {' '.join(command)}")
        result = run_command(
            ["docker", "compose", "exec", "api", *command], cwd=API_PROJECT_DIR
        )
        if result.success:
            return _create_operation_result(
                True, "Command executed successfully", result.stdout
            )
        return _create_operation_result(
            False, "Failed to execute command", result.stderr
        )

    except Exception as e:
        return _create_operation_result(
            False, "Unexpected error executing command in API container", str(e)
        )


def run_migration() -> ApiOperationResult:
    """Execute database migrations within the API Docker container using Alembic."""
    status = get_api_status()
    if not status.is_running:
        return _create_operation_result(False, "API service is not running")

    try:
        print_info("Running database migrations with Alembic...")
        result = run_command(
            ["docker", "compose", "exec", "api", "alembic", "upgrade", "head"],
            cwd=API_PROJECT_DIR,
        )
        if result.success:
            return _create_operation_result(
                True, "Database migrations completed successfully", result.stdout
            )
        return _create_operation_result(
            False, "Failed to run database migrations", result.stderr
        )

    except Exception as e:
        return _create_operation_result(
            False, "Unexpected error running database migrations", str(e)
        )
