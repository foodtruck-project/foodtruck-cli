"""Data models for completion command."""

from enum import Enum
from pathlib import Path

from pydantic import BaseModel, Field


class SupportedShell(Enum):
    """Supported shell types for completion."""

    BASH = "bash"
    ZSH = "zsh"
    FISH = "fish"
    POWERSHELL = "powershell"
    CMD = "cmd"

    class UnsupportedShellError(ValueError):
        """Exception raised when an unsupported shell type is provided."""

        def __init__(self, shell: str):
            super().__init__(f"Unsupported shell: {shell}")

    @classmethod
    def from_string(cls, shell: str) -> "SupportedShell":
        """Create SupportedShell from string value."""
        for shell_type in cls:
            if shell_type.value == shell.lower():
                return shell_type
        raise cls.UnsupportedShellError(shell)

    @classmethod
    def all_shells(cls) -> list[str]:
        """Get list of all supported shell names."""
        return [shell.value for shell in cls]


class CompletionSetup(BaseModel):
    """Configuration for shell completion setup."""

    shell: SupportedShell = Field(description="Shell type for completion")
    carapace_path: Path = Field(description="Path to carapace executable")
    config_file: Path = Field(description="Shell configuration file path")
    spec_path: Path = Field(description="Carapace spec file path")
    setup_commands: str = Field(description="Shell-specific setup commands")


class CompletionResult(BaseModel):
    """Result of a completion operation."""

    success: bool = Field(description="Whether the operation succeeded")
    message: str = Field(description="Result message")
    details: str = Field(
        default="", description="Additional details or error information"
    )
