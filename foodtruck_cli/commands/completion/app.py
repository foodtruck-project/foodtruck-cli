"""Completion command app configuration."""

from pathlib import Path

from cyclopts import App

from .command import (
    install_completion_command,
    manual_completion_command,
    refresh_completion_command,
)

# Create the completion app
completion_app = App(
    name="completion", help="Generate shell completion scripts using carapace-bin"
)


@completion_app.command
def install(shell: str = "", output: Path | None = None):
    """Install shell completion."""
    install_completion_command(shell, output)


@completion_app.command
def refresh(shell: str = ""):
    """Refresh shell completion."""
    refresh_completion_command(shell)


@completion_app.command
def manual(shell: str = "", output: Path | None = None):
    """Show manual completion instructions."""
    manual_completion_command(shell, output)


def completion_command() -> None:
    """Generate shell completion scripts using carapace-bin (legacy compatibility)."""
    completion_app()
