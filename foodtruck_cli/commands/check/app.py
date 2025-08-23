"""Check command app configuration."""

from cyclopts import App

from .command import check_dependencies_command

# Create the check app
check_app = App(name="check", help="Check command implementation.")


# Since check is a simple command, we can make it the default command
@check_app.default
def check() -> None:
    """Check all required dependencies."""
    check_dependencies_command()


def check_command() -> None:
    """Check command implementation (legacy compatibility)."""
    check_app()
