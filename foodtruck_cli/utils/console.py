"""
Unified console utility for Food Truck CLI
Provides consistent styling and output across all commands
"""

import sys
from enum import Enum
from pathlib import Path
from typing import Any

from pydantic import BaseModel
from rich.console import Console
from rich.theme import Theme

# Theme configuration
THEME_CONFIG = {
    "success": "green",
    "error": "red",
    "warning": "yellow",
    "info": "blue",
    "muted": "dim",
    "title": "bold blue",
    "subtitle": "bold",
    "code": "cyan",
    "path": "cyan",
    "command": "bold cyan",
    "highlight": "bold white",
    "dim": "dim white",
}

# Global console instance
console = Console(theme=Theme(THEME_CONFIG))


class MessageStyle(BaseModel):
    """Represents a message style with color and icon."""

    style: str
    icon: str = ""
    prefix: str = ""
    suffix: str = ""

    class Config:
        frozen = True


class MessageType(Enum):
    """Message types with their styling configuration."""

    # Status messages
    SUCCESS = MessageStyle(style="success", icon="✅")
    ERROR = MessageStyle(style="error", icon="❌")
    WARNING = MessageStyle(style="warning", icon="⚠️ ")
    INFO = MessageStyle(style="info", icon="ℹ️ ")

    # Action messages
    STEP = MessageStyle(style="info", icon="🔧")
    CLONE = MessageStyle(style="info", icon="🚀")
    SKIP = MessageStyle(style="muted", icon="⏭️ ")
    RUN = MessageStyle(style="info", icon="▶️ ")
    STOP = MessageStyle(style="warning", icon="⏹️ ")

    # Structure messages
    TITLE = MessageStyle(style="title")
    SUBTITLE = MessageStyle(style="subtitle")
    SECTION = MessageStyle(style="subtitle", prefix="📋 ")

    # Content messages
    CODE = MessageStyle(style="code")
    PATH = MessageStyle(style="path")
    COMMAND = MessageStyle(style="command")
    MUTED = MessageStyle(style="muted")
    HIGHLIGHT = MessageStyle(style="highlight")


def print_message(
    message: str,
    msg_type: MessageType,
    prefix: str | None = None,
    suffix: str | None = None,
    style_override: str | None = None,
) -> None:
    """Generic function to print messages with consistent styling.

    Args:
        message: The message to print
        msg_type: The type of message (determines style and icon)
        prefix: Optional custom prefix to override the default
        suffix: str | None = None,
        style_override: str | None = None,
    """
    msg_style = msg_type.value
    display_prefix = prefix if prefix is not None else msg_style.prefix + msg_style.icon
    display_suffix = suffix if suffix is not None else msg_style.suffix
    style = style_override if style_override is not None else msg_style.style

    console.print(f"{display_prefix}{message}{display_suffix}", style=style)


def print_success(message: str) -> None:
    """Print a success message."""
    print_message(message, MessageType.SUCCESS)


def print_error(message: str) -> None:
    """Print an error message."""
    print_message(message, MessageType.ERROR)


def print_warning(message: str) -> None:
    """Print a warning message."""
    print_message(message, MessageType.WARNING)


def print_info(message: str) -> None:
    """Print an info message."""
    print_message(message, MessageType.INFO)


def print_step(message: str) -> None:
    """Print a step message."""
    print_message(message, MessageType.STEP)


def print_clone(message: str) -> None:
    """Print a clone message."""
    print_message(message, MessageType.CLONE)


def print_skip(message: str) -> None:
    """Print a skip message."""
    print_message(message, MessageType.SKIP)


def print_title(message: str) -> None:
    """Print a title message."""
    print_message(message, MessageType.TITLE)


def print_subtitle(message: str) -> None:
    """Print a subtitle message."""
    print_message(message, MessageType.SUBTITLE)


def print_path(path: str) -> None:
    """Print a path with special styling."""
    print_message(path, MessageType.PATH)


def print_command(command: str) -> None:
    """Print a command with special styling."""
    print_message(command, MessageType.COMMAND)


def print_code(code: str) -> None:
    """Print code with special styling."""
    print_message(code, MessageType.CODE)


def print_separator(char: str = "=", length: int = 50) -> None:
    """Print a separator line."""
    print_message(char * length, MessageType.MUTED)


def print_newline() -> None:
    """Print a newline."""
    console.print()


def print_list(
    items: list[str], prefix: str = "  ", msg_type: MessageType = MessageType.MUTED
) -> None:
    """Print a list of items with consistent formatting.

    Args:
        items: List of items to print
        prefix: Prefix for each item
        msg_type: Message type for styling
    """
    for item in items:
        print_message(f"{prefix}{item}", msg_type)


def print_section(
    title: str, content: str | list[str], msg_type: MessageType = MessageType.MUTED
) -> None:
    """Print a section with title and content.

    Args:
        title: Section title
        content: Section content (string or list of strings)
        msg_type: Message type for content styling
    """
    print_subtitle(title)
    if isinstance(content, list):
        print_list(content, msg_type=msg_type)
    else:
        print_message(content, msg_type)
    print_newline()


def print_formatted(content: Any, style: str | None = None) -> None:
    """Print any content with optional custom styling.

    Args:
        content: Content to print
        style: Optional custom style to apply
    """
    if style:
        console.print(content, style=style)
    else:
        console.print(content)


def print_setup_success_message(target_path: Path) -> None:
    """Print success message and next steps."""
    print_newline()
    print_success("Setup completed successfully!")
    print_newline()
    print_info(f"Projects created in: {target_path}")
    print_newline()
    print_subtitle("Next steps:")
    print_command(
        "  API: cd foodtruck-api && uv run python -m foodtruck_api.cli.app database init"
    )
    print_command("  Website: cd foodtruck-website && open index.html")


def print_setup_failure_message(
    api_result: Any, website_result: Any
) -> None:
    """Print failure message with details."""
    print_newline()
    print_error("Setup failed. Please check the errors above.")

    if not api_result.success and api_result.message:
        print_error(f"API: {api_result.message}")
    if not website_result.success and website_result.message:
        print_error(f"Website: {website_result.message}")

    sys.exit(1)
