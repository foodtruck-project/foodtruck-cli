"""Completion command implementation functions."""

import sys
from pathlib import Path

from ...utils.console import (
    print_error,
    print_info,
    print_success,
    print_warning,
)
from .completion import (
    create_completion_setup,
    get_carapace_config_dir,
    save_carapace_spec,
)
from .models import CompletionResult, SupportedShell


def check_existing_completion(setup):
    """Check if completion is already installed."""
    if not setup.config_file.exists() or not setup.spec_path.exists():
        return False

    try:
        with setup.config_file.open("r", encoding="utf-8") as f:
            content = f.read()
            return "carapace" in content and "foodtruck" in content
    except Exception:
        return False


def auto_configure_shell(setup):
    """Automatically configure the shell for carapace completion."""
    try:
        config_file = setup.config_file
        setup_commands = setup.setup_commands

        # Check if configuration already exists
        if config_file.exists():
            with config_file.open("r", encoding="utf-8") as f:
                content = f.read()
                if "carapace" in content and "foodtruck" in content:
                    return CompletionResult(
                        success=True,
                        message="Configuration already exists",
                        details=str(config_file),
                    )

        # Create parent directories if needed
        config_file.parent.mkdir(parents=True, exist_ok=True)

        # Add configuration to the file
        with config_file.open("a", encoding="utf-8") as f:
            f.write("\n# Food Truck CLI completion (auto-configured)\n")
            f.write(setup_commands)
            f.write("\n")

        # For CMD, also create a batch file that can be sourced
        if setup.shell == SupportedShell.CMD:
            batch_file = Path.home() / "foodtruck_completion.bat"
            with batch_file.open("w", encoding="utf-8") as f:
                f.write("@echo off\n")
                f.write("REM Food Truck CLI completion for CMD\n")
                f.write(f"set PATH={setup.carapace_path.parent};%PATH%\n")
                f.write(
                    "REM Note: CMD completion is limited. Consider using PowerShell.\n"
                )

        return CompletionResult(
            success=True,
            message=f"Auto-configured {setup.shell.value} completion",
            details=str(config_file),
        )

    except PermissionError as e:
        return CompletionResult(
            success=False,
            message=f"Permission denied while configuring {setup.shell.value}",
            details=str(e),
        )
    except OSError as e:
        return CompletionResult(
            success=False,
            message=f"IO error while configuring {setup.shell.value}",
            details=str(e),
        )
    except Exception as e:
        return CompletionResult(
            success=False,
            message=f"Unexpected error while configuring {setup.shell.value}",
            details=str(e),
        )


def remove_carapace_spec():
    """Remove the existing carapace spec file."""
    config_dir = get_carapace_config_dir()
    spec_path = config_dir / "foodtruck.yaml"

    if not spec_path.exists():
        return CompletionResult(
            success=True, message="No existing spec file found", details=""
        )

    try:
        spec_path.unlink()
        return CompletionResult(
            success=True, message="Removed existing spec file", details=str(spec_path)
        )
    except PermissionError as e:
        return CompletionResult(
            success=False,
            message="Permission denied while removing spec file",
            details=str(e),
        )
    except OSError as e:
        return CompletionResult(
            success=False, message="OS error while removing spec file", details=str(e)
        )
    except Exception as e:
        return CompletionResult(
            success=False,
            message="Unexpected error while removing spec file",
            details=str(e),
        )


def remove_shell_config(setup):
    """Remove carapace configuration from shell config file."""
    try:
        config_file = setup.config_file

        if not config_file.exists():
            return CompletionResult(
                success=True,
                message="Shell config file not found",
                details=str(config_file),
            )

        # Read the file and remove carapace-related lines
        with config_file.open("r", encoding="utf-8") as f:
            lines = f.readlines()

        # Filter out carapace and foodtruck completion lines
        filtered_lines = []
        in_carapace_block = False

        for line in lines:
            # Check if this line starts a carapace block
            if (
                "Food Truck CLI completion" in line
                or "carapace" in line.lower()
                or "Carapace-bin completion setup" in line
            ):
                in_carapace_block = True
                continue

            # Skip lines that are part of the carapace block
            if in_carapace_block:
                if line.strip() == "" or (
                    line.startswith("#") and "carapace" not in line.lower()
                ):
                    # End of carapace block
                    in_carapace_block = False
                else:
                    # Still in carapace block, skip this line
                    continue

            # Keep non-carapace lines
            filtered_lines.append(line)

        # Write back the filtered content
        with config_file.open("w", encoding="utf-8") as f:
            f.writelines(filtered_lines)

        return CompletionResult(
            success=True,
            message="Removed carapace configuration",
            details=str(config_file),
        )

    except PermissionError as e:
        return CompletionResult(
            success=False,
            message="Permission denied while removing shell configuration",
            details=str(e),
        )
    except OSError as e:
        return CompletionResult(
            success=False,
            message="IO error while removing shell configuration",
            details=str(e),
        )
    except Exception as e:
        return CompletionResult(
            success=False,
            message="Unexpected error while removing shell configuration",
            details=str(e),
        )


def _handle_spec_operations(config_dir):
    """Handle common spec operations for install and refresh commands."""
    spec_result = remove_carapace_spec()
    if not spec_result.success:
        return spec_result, CompletionResult(success=False, message="", details="")

    new_spec_result = save_carapace_spec(config_dir)
    if not new_spec_result.success:
        return spec_result, new_spec_result

    return spec_result, new_spec_result


def install_completion_command(shell: str = "") -> None:
    """Install shell completion."""
    try:
        setup = create_completion_setup(shell)

        # Check if completion is already installed
        if check_existing_completion(setup):
            print_info(f"Completion already installed for {setup.shell.value}")
            print_info("Use 'foodtruck completion refresh' to reinstall")
            return

        print_success(f"Installing carapace completion for {setup.shell.value}...")

        # Create spec in user's carapace config directory
        config_dir = get_carapace_config_dir()
        spec_result, new_spec_result = _handle_spec_operations(config_dir)

        if not new_spec_result.success:
            print_error(f"Failed to save spec: {new_spec_result.message}")
            if new_spec_result.details:
                print_error(f"Details: {new_spec_result.details}")
            sys.exit(1)

        print_success(f"Carapace spec saved to: {new_spec_result.details}")

        # Auto-configure shell
        print_info(f"Auto-configuring {setup.shell.value} completion...")
        config_result = auto_configure_shell(setup)

        if config_result.success:
            print_success(
                f"Shell configuration completed! To activate the completion, please restart your terminal session. Alternatively, you can run 'source {setup.config_file}' in your current terminal session to apply the changes immediately."
            )
        else:
            print_warning(f"Auto-configuration failed: {config_result.message}")
            print_warning(
                "Please configure manually using 'foodtruck completion manual'"
            )

        print_success("Completion installation completed!")

    except Exception as e:
        print_error(f"Installation failed: {e}")
        sys.exit(1)


def refresh_completion_command(shell: str = "") -> None:
    """Refresh shell completion."""
    try:
        setup = create_completion_setup(shell)

        print_info("Refreshing carapace completion...")

        # Remove existing spec
        config_dir = get_carapace_config_dir()
        spec_result, new_spec_result = _handle_spec_operations(config_dir)

        if spec_result.success:
            print_success(spec_result.message)
        else:
            print_error(f"Failed to remove spec: {spec_result.message}")
            sys.exit(1)

        # Remove existing shell configuration
        config_result = remove_shell_config(setup)
        if config_result.success:
            print_success(config_result.message)
        else:
            print_warning(f"Failed to remove shell config: {config_result.message}")

        if not new_spec_result.success:
            print_error(f"Failed to create new spec: {new_spec_result.message}")
            sys.exit(1)

        print_success(f"New carapace spec saved to: {new_spec_result.details}")

        # Auto-configure shell
        print_info(f"Auto-configuring {setup.shell.value} completion...")
        auto_config_result = auto_configure_shell(setup)

        if auto_config_result.success:
            print_success(
                f"Shell configuration completed! To activate the updated completion, please restart your terminal session. Alternatively, you can run 'source {setup.config_file}' in your current terminal session to apply the changes immediately."
            )
        else:
            print_warning(f"Auto-configuration failed: {auto_config_result.message}")

        print_success("Completion refresh completed!")

    except Exception as e:
        print_error(f"Refresh failed: {e}")
        sys.exit(1)


def manual_completion_command(shell: str = "", output: Path | None = None) -> None:
    """Show manual completion instructions."""
    try:
        setup = create_completion_setup(shell)

        # Get the proper setup commands for the shell
        print_success(
            f"To enable completion for {setup.shell.value}, add this to your shell configuration:"
        )
        print_warning(setup.setup_commands)

        if output:
            # Save the setup commands to a file
            output.parent.mkdir(parents=True, exist_ok=True)
            with output.open("w", encoding="utf-8") as f:
                f.write(f"# Food Truck CLI completion for {setup.shell.value}\n")
                f.write("# Generated by carapace-bin\n\n")
                f.write(setup.setup_commands)
                f.write("\n")
            print_success(f"Setup commands saved to: {output}")

    except Exception as e:
        print_error(f"Manual command failed: {e}")
        sys.exit(1)
