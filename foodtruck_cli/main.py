"""
Food Truck CLI - Main entry point
"""

import sys

import cyclopts

from .commands import setup_command
from .console import print_error

# Create cyclopts app
app = cyclopts.App(
    name="foodtruck",
    help="Food Truck Development CLI",
    version="0.1.0",
)

# Register commands
app.command(setup_command, name="setup")


def main() -> None:
    """Main CLI entry point."""
    try:
        # Parse and execute commands
        app()
    except Exception as e:
        print_error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
