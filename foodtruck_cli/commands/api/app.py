"""API command app configuration."""

from cyclopts import App

from .command import (
    api_install_command,
    api_logs_command,
    api_restart_command,
    api_setup_command,
    api_start_command,
    api_status_command,
    api_stop_command,
)

# Create the api app
api_app = App(name="api", help="Manage the Food Truck API project")


@api_app.command
def setup():
    """Setup API project."""
    api_setup_command()


@api_app.command
def install():
    """Install API dependencies."""
    api_install_command()


@api_app.command
def start(build: bool = False):
    """Start API services."""
    api_start_command(build)


@api_app.command
def stop():
    """Stop API services."""
    api_stop_command()


@api_app.command
def restart():
    """Restart API services."""
    api_restart_command()


@api_app.command
def status():
    """Check API service status."""
    api_status_command()


@api_app.command
def logs(lines: int = 50, follow: bool = False):
    """Show API service logs."""
    api_logs_command(lines, follow)


def api_command() -> None:
    """Manage the Food Truck API project."""
    api_app()
