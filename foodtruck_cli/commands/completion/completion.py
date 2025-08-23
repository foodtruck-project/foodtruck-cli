"""
Food Truck CLI - Completion Command
Uses carapace-bin to provide shell completions
"""

import os
import platform
import sys
from pathlib import Path

from cyclopts import App, Parameter

from ...utils.console import print_error, print_info, print_success, print_warning


def get_carapace_path() -> Path | None:
    """Get the path to the carapace executable"""
    # Try to find carapace in the project directory first
    project_dir = Path(__file__).parent.parent.parent

    # Use correct executable name for platform
    carapace_name = "carapace.exe" if platform.system() == "Windows" else "carapace"
    carapace_path = project_dir / "carapace-bin" / carapace_name

    if carapace_path.exists() and carapace_path.is_file():
        return carapace_path

    # Try to find carapace in PATH
    import shutil

    carapace_in_path = shutil.which(carapace_name)
    if carapace_in_path:
        return Path(carapace_in_path)

    return None


def get_spec_file_path() -> Path:
    """Get the path to the carapace spec file"""
    return Path(__file__).parent / "complete.yaml"


def save_carapace_spec(spec_dir: Path) -> Path:
    """Save the carapace spec to the appropriate directory"""
    spec_dir.mkdir(parents=True, exist_ok=True)
    spec_path = spec_dir / "foodtruck.yaml"

    # Read the spec from the local YAML file
    source_spec = get_spec_file_path()
    if not source_spec.exists():
        msg = f"Spec file not found: {source_spec}"
        raise FileNotFoundError(msg)

    # Copy the spec file to the carapace config directory
    import shutil

    shutil.copy2(source_spec, spec_path)

    return spec_path


def get_shell_setup_commands(shell: str, carapace_path: Path) -> str:
    """Get the proper setup commands for each shell based on official documentation"""
    carapace_dir = carapace_path.parent

    # Convert path to appropriate format for the shell
    if platform.system() == "Windows":
        carapace_dir_str = str(carapace_dir).replace("/", "\\")
        carapace_path_str = str(carapace_path).replace("/", "\\")
    else:
        carapace_dir_str = str(carapace_dir)
        carapace_path_str = str(carapace_path)

    if shell == "bash":
        return f"""# Add carapace to PATH
export PATH="{carapace_dir_str}:$PATH"

# Load all carapace completions
source <({carapace_path_str} _carapace)"""

    if shell == "zsh":
        return f"""# Add carapace to PATH
export PATH="{carapace_dir_str}:$PATH"

# Optional: Configure bridges
export CARAPACE_BRIDGES='zsh,fish,bash,inshellisense'

# Optional: Configure completion style
zstyle ':completion:*' format $'\\e[2;37mCompleting %d\\e[m'

# Load all carapace completions
source <({carapace_path_str} _carapace)"""

    if shell == "fish":
        return f"""# Add carapace to PATH
set -Ux PATH "{carapace_dir_str}" $PATH

# Optional: Configure bridges
set -Ux CARAPACE_BRIDGES 'zsh,fish,bash,inshellisense'

# Load all carapace completions
{carapace_path_str} _carapace | source"""

    if shell == "powershell":
        return f"""# Add carapace to PATH
$env:PATH = "{carapace_dir_str};" + $env:PATH

# Optional: Configure bridges
$env:CARAPACE_BRIDGES = 'zsh,fish,bash,inshellisense'

# Configure PowerShell completion
Set-PSReadLineOption -Colors @{{ "Selection" = "`e[7m" }}
Set-PSReadlineKeyHandler -Key Tab -Function MenuComplete

# Load all carapace completions
{carapace_path_str} _carapace | Out-String | Invoke-Expression"""

    if shell == "cmd":
        return f"""# Add carapace to PATH
set PATH={carapace_dir_str};%PATH%

# Note: CMD completion is limited. Consider using PowerShell for better completion support."""

    msg = f"Unsupported shell: {shell}"
    raise ValueError(msg)


def get_carapace_config_dir() -> Path:
    """Get the appropriate carapace config directory for the platform"""
    if platform.system() == "Windows":
        # Windows: Use APPDATA directory
        appdata = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
        return appdata / "carapace" / "specs"
    # Unix-like: Use .config directory
    return Path.home() / ".config" / "carapace" / "specs"


def get_shell_config_file(shell: str) -> Path:
    """Get the path to the shell configuration file"""
    home = Path.home()

    if shell == "bash":
        return home / ".bashrc"
    elif shell == "zsh":
        return home / ".zshrc"
    elif shell == "fish":
        return home / ".config" / "fish" / "config.fish"
    elif shell == "powershell":
        # PowerShell profile location
        profile_path = os.environ.get("POWERSHELL_PROFILE")
        if profile_path:
            return Path(profile_path)
        # Fallback to default location
        return home / "Documents" / "PowerShell" / "Microsoft.PowerShell_profile.ps1"
    elif shell == "cmd":
        # CMD doesn't have a config file, but we can create a batch file
        return home / "foodtruck_completion.bat"
    else:
        msg = f"Unsupported shell for config file: {shell}"
        raise ValueError(msg)


def auto_configure_shell(shell: str, carapace_path: Path) -> bool:
    """Automatically configure the shell for carapace completion"""
    try:
        config_file = get_shell_config_file(shell)
        setup_commands = get_shell_setup_commands(shell, carapace_path)

        # Check if configuration already exists
        if config_file.exists():
            with config_file.open("r", encoding="utf-8") as f:
                content = f.read()
                if "carapace" in content and "foodtruck" in content:
                    print_info(
                        f"Carapace configuration already exists in {config_file}"
                    )
                    return True

        # Create parent directories if needed
        config_file.parent.mkdir(parents=True, exist_ok=True)

        # Add configuration to the file
        with config_file.open("a", encoding="utf-8") as f:
            f.write(f"\n# Food Truck CLI completion (auto-configured)\n")
            f.write(setup_commands)
            f.write("\n")

        print_success(f"Auto-configured {shell} completion in {config_file}")

        # For CMD, also create a batch file that can be sourced
        if shell == "cmd":
            batch_file = Path.home() / "foodtruck_completion.bat"
            with batch_file.open("w", encoding="utf-8") as f:
                f.write("@echo off\n")
                f.write("REM Food Truck CLI completion for CMD\n")
                f.write(f"set PATH={carapace_path.parent};%PATH%\n")
                f.write(
                    "REM Note: CMD completion is limited. Consider using PowerShell.\n"
                )
            print_success(f"Created CMD batch file: {batch_file}")

        return True

    except Exception as e:
        print_error(f"Failed to auto-configure {shell}: {e}")
        return False


def remove_carapace_spec() -> bool:
    """Remove the existing carapace spec file"""
    config_dir = get_carapace_config_dir()
    spec_path = config_dir / "foodtruck.yaml"

    if spec_path.exists():
        try:
            spec_path.unlink()
            print_success(f"Removed existing spec file: {spec_path}")
            return True
        except Exception as e:
            print_error(f"Failed to remove spec file: {e}")
            return False
    else:
        print_warning("No existing spec file found to remove")
        return True


def remove_shell_config(shell: str) -> bool:
    """Remove carapace configuration from shell config file"""
    try:
        config_file = get_shell_config_file(shell)

        if not config_file.exists():
            print_warning(f"Shell config file not found: {config_file}")
            return True

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

        print_success(f"Removed carapace configuration from {config_file}")
        return True

    except Exception as e:
        print_error(f"Failed to remove shell configuration: {e}")
        return False


def refresh_carapace_completion(shell: str) -> None:
    """Remove existing completion and regenerate it"""
    print_info("Refreshing carapace completion...")

    # Remove existing spec
    if not remove_carapace_spec():
        sys.exit(1)

    # Remove existing shell configuration
    if not remove_shell_config(shell):
        print_warning("Failed to remove shell configuration, but continuing...")

    # Get carapace path
    carapace_path = get_carapace_path()
    if not carapace_path:
        print_error(
            "Carapace-bin not found. Please run the installation script first: python install.py"
        )
        sys.exit(1)

    try:
        # Create new spec in user's carapace config directory
        config_dir = get_carapace_config_dir()
        spec_path = save_carapace_spec(config_dir)
        print_success(f"New carapace spec saved to: {spec_path}")

        # Auto-configure shell by default
        print_info(f"Auto-configuring {shell} completion...")
        if auto_configure_shell(shell, carapace_path):
            print_success(
                f"Shell configuration completed! Restart your terminal or run 'source {get_shell_config_file(shell)}' to activate."
            )
        else:
            print_warning("Auto-configuration failed. Please configure manually.")

        print_success("Completion refresh completed!")

    except Exception as e:
        print_error(f"Error refreshing completion: {e}")
        sys.exit(1)


def _get_shell_and_validate(shell: str = "") -> tuple[str, Path]:
    """Get shell type and validate, return (shell, carapace_path)"""
    # Auto-detect shell if not specified
    if not shell:
        if platform.system() == "Windows":
            # Check for PowerShell first, then CMD
            if "powershell" in os.environ.get("SHELL", "").lower():
                shell = "powershell"
            else:
                shell = "cmd"
        else:
            # Unix-like systems
            shell = os.environ.get("SHELL", "bash")
            if "zsh" in shell:
                shell = "zsh"
            elif "fish" in shell:
                shell = "fish"
            else:
                shell = "bash"

    # Validate shell type
    supported_shells = ["bash", "zsh", "fish", "powershell", "cmd"]
    if shell not in supported_shells:
        print_error(f"Unsupported shell: {shell}")
        print_error(f"Supported shells: {', '.join(supported_shells)}")
        sys.exit(1)

    # Get carapace path
    carapace_path = get_carapace_path()
    if not carapace_path:
        print_error(
            "Carapace-bin not found. Please run the installation script first: python install.py"
        )
        sys.exit(1)

    return shell, carapace_path


def completion_install_command(shell: str = "", output: Path | None = None) -> None:
    """Install shell completion"""
    shell, carapace_path = _get_shell_and_validate()

    try:
        # Check if completion is already installed
        config_file = get_shell_config_file(shell)
        spec_path = get_carapace_config_dir() / "foodtruck.yaml"

        already_installed = False
        if config_file.exists() and spec_path.exists():
            with config_file.open("r", encoding="utf-8") as f:
                content = f.read()
                if "carapace" in content and "foodtruck" in content:
                    already_installed = True

        if already_installed:
            print_info(f"Completion already installed for {shell}")
            print_info("Use 'foodtruck completion refresh' to reinstall")
            return

        print_success(f"Installing carapace completion for {shell}...")

        # Create spec in user's carapace config directory
        config_dir = get_carapace_config_dir()
        spec_path = save_carapace_spec(config_dir)
        print_success(f"Carapace spec saved to: {spec_path}")

        # Auto-configure shell
        print_info(f"Auto-configuring {shell} completion...")
        if auto_configure_shell(shell, carapace_path):
            print_success(
                f"Shell configuration completed! Restart your terminal or run 'source {get_shell_config_file(shell)}' to activate."
            )
        else:
            print_warning("Auto-configuration failed. Please configure manually.")

        print_success("Completion installation completed!")

    except Exception as e:
        print_error(f"Error: {e}")
        sys.exit(1)


def completion_refresh_command(shell: str = "") -> None:
    """Refresh shell completion"""
    shell, carapace_path = _get_shell_and_validate()
    refresh_carapace_completion(shell)


def completion_manual_command(shell: str = "", output: Path | None = None) -> None:
    """Show manual completion instructions"""
    shell, carapace_path = _get_shell_and_validate(shell)

    try:
        # Get the proper setup commands for the shell
        setup_commands = get_shell_setup_commands(shell, carapace_path)
        print_success(
            f"To enable completion for {shell}, add this to your shell configuration:"
        )
        print_warning(setup_commands)

        if output:
            # Save the setup commands to a file
            output.parent.mkdir(parents=True, exist_ok=True)
            with output.open("w", encoding="utf-8") as f:
                f.write(f"# Food Truck CLI completion for {shell}\n")
                f.write("# Generated by carapace-bin\n\n")
                f.write(setup_commands)
                f.write("\n")
            print_success(f"Setup commands saved to: {output}")

    except Exception as e:
        print_error(f"Error: {e}")
        sys.exit(1)


# Create completion sub-app
completion_app = App(
    name="completion", help="Generate shell completion scripts using carapace-bin"
)


@completion_app.command
def install(shell: str = "", output: Path | None = None):
    """Install shell completion"""
    completion_install_command(shell, output)


@completion_app.command
def refresh(shell: str = ""):
    """Refresh shell completion"""
    completion_refresh_command(shell)


@completion_app.command
def manual(shell: str = "", output: Path | None = None):
    """Show manual completion instructions"""
    completion_manual_command(shell, output)


def completion_command(shell: str = "", output: Path | None = None) -> None:
    """Generate shell completion scripts using carapace-bin"""

    # Run the sub-app
    completion_app()
