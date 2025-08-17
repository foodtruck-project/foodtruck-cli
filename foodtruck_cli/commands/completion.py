"""
Food Truck CLI - Completion Command
Uses carapace-bin to provide shell completions
"""

import os
import platform
import sys
from pathlib import Path

from ..console import print_error, print_success, print_warning


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


def completion_command(
    shell: str = "",
    output: Path | None = None,
    install: bool = False
) -> None:
    """Generate shell completion scripts using carapace-bin"""

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
        print_error("Carapace-bin not found. Please run the installation script first: python install.py")
        sys.exit(1)

    try:
        if install:
            print_success(f"Installing carapace completion for {shell}...")

            # Create spec in user's carapace config directory
            config_dir = get_carapace_config_dir()
            spec_path = save_carapace_spec(config_dir)
            print_success(f"Carapace spec saved to: {spec_path}")

        # Get the proper setup commands for the shell
        setup_commands = get_shell_setup_commands(shell, carapace_path)

        print_success(f"To enable completion for {shell}, add this to your shell configuration:")
        print_warning(setup_commands)

        if install:
            print_success("Completion installation completed!")
            if platform.system() == "Windows":
                print_warning("You may need to restart your terminal or reload your shell configuration.")
                if shell == "cmd":
                    print_warning("Note: CMD completion is limited. Consider using PowerShell for better completion support.")
            else:
                print_warning("You may need to restart your terminal or reload your shell configuration.")

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
