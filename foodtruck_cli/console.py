"""
Unified console utility for Food Truck CLI
Provides consistent styling and output across all commands
"""

from rich.console import Console
from rich.theme import Theme

# Create a custom theme for consistent styling
custom_theme = Theme({
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
})

# Global console instance
console = Console(theme=custom_theme)


def print_success(message: str) -> None:
    """Print a success message."""
    console.print(f"✅ {message}", style="success")


def print_error(message: str) -> None:
    """Print an error message."""
    console.print(f"❌ {message}", style="error")


def print_warning(message: str) -> None:
    """Print a warning message."""
    console.print(f"⚠️  {message}", style="warning")


def print_info(message: str) -> None:
    """Print an info message."""
    console.print(f"i  {message}", style="info")


def print_step(message: str) -> None:
    """Print a step message."""
    console.print(f"🔧 {message}", style="info")


def print_clone(message: str) -> None:
    """Print a clone message."""
    console.print(f"🚀 {message}", style="info")


def print_skip(message: str) -> None:
    """Print a skip message."""
    console.print(f"⏭️  {message}", style="muted")


def print_title(message: str) -> None:
    """Print a title message."""
    console.print(message, style="title")


def print_subtitle(message: str) -> None:
    """Print a subtitle message."""
    console.print(message, style="subtitle")


def print_path(path: str) -> None:
    """Print a path with special styling."""
    console.print(path, style="path")


def print_command(command: str) -> None:
    """Print a command with special styling."""
    console.print(command, style="command")


def print_code(code: str) -> None:
    """Print code with special styling."""
    console.print(code, style="code")


def print_separator(char: str = "=", length: int = 50) -> None:
    """Print a separator line."""
    console.print(char * length, style="muted")


def print_newline() -> None:
    """Print a newline."""
    console.print()


def print_list(items: list[str], prefix: str = "  ") -> None:
    """Print a list of items with consistent formatting."""
    for item in items:
        console.print(f"{prefix}{item}")


def print_section(title: str, content: str | list[str]) -> None:
    """Print a section with title and content."""
    print_subtitle(title)
    if isinstance(content, list):
        print_list(content)
    else:
        console.print(content)
    print_newline()
