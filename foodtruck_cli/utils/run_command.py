import subprocess
from pathlib import Path

from .console import print_error, print_success


def run_command(cmd: list[str], cwd: Path | None = None) -> bool:
    """Execute a shell command and return success status.

    Runs a command using subprocess with comprehensive error handling including
    timeouts, missing commands, permission errors, and execution failures.

    Args:
        cmd: List of command arguments (e.g., ['git', 'clone', 'repo'])
        cwd: Working directory for command execution (default: current directory)

    Returns:
        bool: True if command executed successfully, False otherwise

    Raises:
        No exceptions are raised - all errors are handled internally and logged
    """
    success = False

    if not cmd:
        print_error("No command provided")
    else:
        try:
            result = subprocess.run(
                cmd,
                cwd=cwd,
                capture_output=True,
                text=True,
                check=True,
                timeout=300,  # 5 minute timeout
            )
            # Only print output if there's something meaningful
            if result.stdout and result.stdout.strip():
                print_success(result.stdout.strip())
            success = True

        except subprocess.CalledProcessError as e:
            error_msg = (
                e.stderr.strip()
                if e.stderr
                else f"Command failed with exit code {e.returncode}"
            )
            print_error(f"Error running '{' '.join(cmd)}': {error_msg}")

        except subprocess.TimeoutExpired:
            print_error(f"Command '{' '.join(cmd)}' timed out after 5 minutes")

        except FileNotFoundError:
            print_error(
                f"Command '{cmd[0]}' not found. Please ensure it's installed and in your PATH"
            )

        except PermissionError:
            print_error(f"Permission denied when running '{' '.join(cmd)}'")

        except Exception as e:
            print_error(f"Unexpected error running '{' '.join(cmd)}': {e!s}")

    return success
