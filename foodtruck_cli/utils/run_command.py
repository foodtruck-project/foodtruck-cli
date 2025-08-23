import subprocess
from pathlib import Path
from typing import NamedTuple

from .console import print_error, print_success


class CommandResult(NamedTuple):
    """Result of a command execution."""

    success: bool
    stdout: str
    stderr: str
    returncode: int


def run_command(
    cmd: list[str],
    cwd: Path | None = None,
    timeout: int = 300,
    capture_output: bool = True,
    print_output: bool = False,
) -> CommandResult:
    """Execute a shell command and return comprehensive result."""
    if not cmd:
        error_msg = "No command provided"
        if print_output:
            print_error(error_msg)
        return CommandResult(False, "", error_msg, -1)

    error_msg = ""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=capture_output,
            text=True,
            check=True,
            timeout=timeout,
        )
        if print_output and result.stdout and result.stdout.strip():
            print_success(result.stdout.strip())
        return CommandResult(
            True,
            result.stdout.strip() if result.stdout else "",
            result.stderr.strip() if result.stderr else "",
            result.returncode,
        )
    except subprocess.CalledProcessError as e:
        error_msg = (
            e.stderr.strip()
            if e.stderr
            else f"Command failed with exit code {e.returncode}"
        )
    except (FileNotFoundError, PermissionError) as e:
        if isinstance(e, FileNotFoundError):
            error_msg = f"Command '{cmd[0]}' not found. Please ensure it's installed and in your PATH"
        else:
            error_msg = f"Permission denied when running '{' '.join(cmd)}'"
    except subprocess.TimeoutExpired:
        error_msg = f"Command '{' '.join(cmd)}' timed out after {timeout} seconds"
    except Exception as e:
        error_msg = f"Unexpected error: {e!s}"

    if print_output and error_msg:
        print_error(error_msg)
    return CommandResult(False, "", error_msg, -1)
