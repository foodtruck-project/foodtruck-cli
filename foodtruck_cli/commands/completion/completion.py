"""Core completion logic for Food Truck CLI."""

import os
import platform
import shutil
from pathlib import Path

from .models import CompletionResult, CompletionSetup, SupportedShell


def get_carapace_path() -> Path | None:
    """Get the path to the carapace executable."""
    # Try to find carapace in the project directory first
    project_dir = Path(__file__).parent.parent.parent

    # Use correct executable name for platform
    carapace_name = "carapace.exe" if platform.system() == "Windows" else "carapace"
    carapace_path = project_dir / "carapace-bin" / carapace_name

    if carapace_path.exists() and carapace_path.is_file():
        return carapace_path

    # Try to find carapace in PATH
    carapace_in_path = shutil.which(carapace_name)
    if carapace_in_path:
        return Path(carapace_in_path)

    return None


def get_spec_file_path() -> Path:
    """Get the path to the carapace spec file."""
    return Path(__file__).parent / "complete.yaml"


def get_carapace_config_dir() -> Path:
    """Get the appropriate carapace config directory for the platform."""
    if platform.system() == "Windows":
        # Windows: Use APPDATA directory
        appdata = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
        return appdata / "carapace" / "specs"
    # Unix-like: Use .config directory
    return Path.home() / ".config" / "carapace" / "specs"


def get_shell_config_file(shell: SupportedShell) -> Path:
    """Get the path to the shell configuration file."""
    home = Path.home()
    shell_config_map = {
        SupportedShell.BASH: home / ".bashrc",
        SupportedShell.ZSH: home / ".zshrc",
        SupportedShell.FISH: home / ".config" / "fish" / "config.fish",
        SupportedShell.CMD: home / "foodtruck_completion.bat"
    }

    if shell == SupportedShell.POWERSHELL:
        profile_path = os.environ.get("POWERSHELL_PROFILE")
        if profile_path:
            return Path(profile_path)
        return home / "Documents" / "PowerShell" / "Microsoft.PowerShell_profile.ps1"

    return shell_config_map.get(shell, UnsupportedShellConfigError())


def get_shell_setup_commands(shell: SupportedShell, carapace_path: Path) -> str:
    """Get the proper setup commands for each shell based on official documentation."""
    carapace_dir = carapace_path.parent

    # Convert path to appropriate format for the shell
    if platform.system() == "Windows":
        carapace_dir_str = str(carapace_dir).replace("/", "\\")
        carapace_path_str = str(carapace_path).replace("/", "\\")
    else:
        carapace_dir_str = str(carapace_dir)
        carapace_path_str = str(carapace_path)

    shell_setup_map = {
        SupportedShell.BASH: f"""# Add carapace to PATH
export PATH="{carapace_dir_str}:$PATH"

# Load all carapace completions
source <({carapace_path_str} _carapace)""",
        SupportedShell.ZSH: f"""# Add carapace to PATH
export PATH="{carapace_dir_str}:$PATH"

# Optional: Configure bridges
export CARAPACE_BRIDGES='zsh,fish,bash,inshellisense'

# Optional: Configure completion style
zstyle ':completion:*' format $'\\e[2;37mCompleting %d\\e[m'

# Load all carapace completions
source <({carapace_path_str} _carapace)""",
        SupportedShell.FISH: f"""# Add carapace to PATH
set -Ux PATH "{carapace_dir_str}" $PATH

# Optional: Configure bridges
set -Ux CARAPACE_BRIDGES 'zsh,fish,bash,inshellisense'

# Load all carapace completions
{carapace_path_str} _carapace | source""",
        SupportedShell.POWERSHELL: f"""# Add carapace to PATH
$env:PATH = "{carapace_dir_str};" + $env:PATH

# Optional: Configure bridges
$env:CARAPACE_BRIDGES = 'zsh,fish,bash,inshellisense'

# Configure PowerShell completion
Set-PSReadLineOption -Colors @{{ "Selection" = "`e[7m" }}
Set-PSReadlineKeyHandler -Key Tab -Function MenuComplete

# Load all carapace completions
{carapace_path_str} _carapace | Out-String | Invoke-Expression""",
        SupportedShell.CMD: f"""# Add carapace to PATH
set PATH={carapace_dir_str};%PATH%

# Note: CMD completion is limited. Consider using PowerShell for better completion support."""
    }

    setup_command = shell_setup_map.get(shell)
    if setup_command is None:
        raise UnsupportedShellSetupError
    return setup_command


def detect_shell() -> SupportedShell:
    """Auto-detect the current shell."""
    if platform.system() == "Windows":
        # Check for PowerShell first, then CMD
        if "powershell" in os.environ.get("SHELL", "").lower():
            return SupportedShell.POWERSHELL
        return SupportedShell.CMD
    # Unix-like systems
    shell = os.environ.get("SHELL", "bash")
    if "zsh" in shell:
        return SupportedShell.ZSH
    if "fish" in shell:
        return SupportedShell.FISH
    return SupportedShell.BASH


def save_carapace_spec(spec_dir: Path) -> CompletionResult:
    """Save the carapace spec to the appropriate directory."""
    try:
        spec_dir.mkdir(parents=True, exist_ok=True)
        spec_path = spec_dir / "foodtruck.yaml"

        # Read the spec from the local YAML file
        source_spec = get_spec_file_path()
        if not source_spec.exists():
            return CompletionResult(
                success=False, message="Spec file not found", details=str(source_spec)
            )

        # Copy the spec file to the carapace config directory
        shutil.copy2(source_spec, spec_path)

        return CompletionResult(
            success=True, message="Spec file saved successfully", details=str(spec_path)
        )

    except Exception as e:
        return CompletionResult(
            success=False, message="Failed to save spec file", details=str(e)
        )


def create_completion_setup(shell: str = "") -> CompletionSetup:
    """Create a CompletionSetup configuration."""
    # Parse shell type
    shell_type = detect_shell() if not shell else SupportedShell.from_string(shell)

    # Get carapace path
    carapace_path = get_carapace_path()
    if not carapace_path:
        raise CarapaceNotFoundError

    # Get paths and commands
    config_file = get_shell_config_file(shell_type)
    spec_path = get_carapace_config_dir() / "foodtruck.yaml"
    setup_commands = get_shell_setup_commands(shell_type, carapace_path)

    return CompletionSetup(
        shell=shell_type,
        carapace_path=carapace_path,
        config_file=config_file,
        spec_path=spec_path,
        setup_commands=setup_commands,
    )


class UnsupportedShellConfigError(ValueError):
    """Exception raised when an unsupported shell type is provided for configuration."""

    def __init__(self):
        super().__init__("Unsupported shell for config file")


class UnsupportedShellSetupError(ValueError):
    """Exception raised when an unsupported shell type is provided for setup commands."""

    def __init__(self):
        super().__init__("Unsupported shell")


class CarapaceNotFoundError(FileNotFoundError):
    """Exception raised when carapace binary is not found."""

    def __init__(self):
        super().__init__("Carapace-bin not found. Please ensure it's installed in the project directory or in your PATH. You can install it by running: python install.py")
