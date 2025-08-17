"""
Completion command for generating shell completion scripts.
"""

import sys
from pathlib import Path

from ..console import print_error, print_info, print_success, print_title


def generate_bash_completion() -> str:
    """Generate bash completion script."""
    return """# bash completion for foodtruck

_foodtruck_completion() {
    local cur prev opts cmds
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    
    # Main commands
    cmds="check setup completion --help --version"
    
    # Command-specific completions
    case "${prev}" in
        setup)
            # Setup command options
            opts="--api-repo --website-repo --target-dir --skip-api --skip-website --help"
            COMPREPLY=( $(compgen -W "${opts}" -- "${cur}") )
            return 0
            ;;
        check)
            # Check command has no additional options
            COMPREPLY=( $(compgen -W "--help" -- "${cur}") )
            return 0
            ;;
        completion)
            # Completion command options
            opts="bash zsh powershell --help"
            COMPREPLY=( $(compgen -W "${opts}" -- "${cur}") )
            return 0
            ;;
        --api-repo|--website-repo|--target-dir)
            # These options expect file/directory completion
            return 0
            ;;
        --skip-api|--skip-website)
            # Boolean flags
            COMPREPLY=( $(compgen -W "true false" -- "${cur}") )
            return 0
            ;;
        *)
            # Default completion for main commands
            COMPREPLY=( $(compgen -W "${cmds}" -- "${cur}") )
            return 0
            ;;
    esac
}

complete -F _foodtruck_completion foodtruck
"""


def generate_zsh_completion() -> str:
    """Generate zsh completion script."""
    return """# zsh completion for foodtruck

_foodtruck() {
    local curcontext="$curcontext" state line
    typeset -A opt_args

    _arguments -C \\
        '1: :->cmds' \\
        '*:: :->args'

    case $state in
        cmds)
            local commands
            commands=(
                'check:Check dependencies'
                'setup:Setup development environment'
                'completion:Generate shell completion'
                '--help:Show help'
                '--version:Show version'
            )
            _describe -t commands 'foodtruck commands' commands
            ;;
        args)
            case $line[1] in
                setup)
                    _arguments \\
                        '--api-repo[API repository URL]:url:_urls' \\
                        '--website-repo[Website repository URL]:url:_urls' \\
                        '--target-dir[Target directory]:directory:_files -/' \\
                        '--skip-api[Skip API setup]' \\
                        '--skip-website[Skip website setup]' \\
                        '--help[Show help]'
                    ;;
                check)
                    _arguments \\
                        '--help[Show help]'
                    ;;
                completion)
                    _arguments \\
                        'bash[Generate bash completion]' \\
                        'zsh[Generate zsh completion]' \\
                        'powershell[Generate PowerShell completion]' \\
                        '--help[Show help]'
                    ;;
            esac
            ;;
    esac
}

compdef _foodtruck foodtruck
"""


def generate_powershell_completion() -> str:
    """Generate PowerShell completion script."""
    return """# PowerShell completion for foodtruck

Register-ArgumentCompleter -Native -CommandName foodtruck -ScriptBlock {
    param($wordToComplete, $commandAst, $cursorPosition)
    
    $completions = @(
        @{Command = "check"; Description = "Check dependencies"}
        @{Command = "setup"; Description = "Setup development environment"}
        @{Command = "completion"; Description = "Generate shell completion"}
        @{Command = "--help"; Description = "Show help"}
        @{Command = "--version"; Description = "Show version"}
    )
    
    $setupOptions = @(
        @{Option = "--api-repo"; Description = "API repository URL"}
        @{Option = "--website-repo"; Description = "Website repository URL"}
        @{Option = "--target-dir"; Description = "Target directory"}
        @{Option = "--skip-api"; Description = "Skip API setup"}
        @{Option = "--skip-website"; Description = "Skip website setup"}
        @{Option = "--help"; Description = "Show help"}
    )
    
    $completionOptions = @(
        @{Option = "bash"; Description = "Generate bash completion"}
        @{Option = "zsh"; Description = "Generate zsh completion"}
        @{Option = "powershell"; Description = "Generate PowerShell completion"}
        @{Option = "--help"; Description = "Show help"}
    )
    
    # Get the command being completed
    $command = $commandAst.CommandElements | Where-Object { $_.ToString() -ne "foodtruck" } | Select-Object -First 1
    
    if ($command) {
        switch ($command.ToString()) {
            "setup" {
                $setupOptions | Where-Object { $_.Option -like "$wordToComplete*" } | ForEach-Object {
                    [System.Management.Automation.CompletionResult]::new($_.Option, $_.Option, 'ParameterName', $_.Description)
                }
            }
            "check" {
                if ("--help" -like "$wordToComplete*") {
                    [System.Management.Automation.CompletionResult]::new("--help", "--help", 'ParameterName', "Show help")
                }
            }
            "completion" {
                $completionOptions | Where-Object { $_.Option -like "$wordToComplete*" } | ForEach-Object {
                    [System.Management.Automation.CompletionResult]::new($_.Option, $_.Option, 'ParameterName', $_.Description)
                }
            }
        }
    } else {
        # Main command completion
        $completions | Where-Object { $_.Command -like "$wordToComplete*" } | ForEach-Object {
            [System.Management.Automation.CompletionResult]::new($_.Command, $_.Command, 'ParameterName', $_.Description)
        }
    }
}
"""


def get_completion_script(shell: str) -> str:
    """Get completion script for the specified shell."""
    if shell == "bash":
        return generate_bash_completion()
    if shell == "zsh":
        return generate_zsh_completion()
    if shell == "powershell":
        return generate_powershell_completion()
    raise ValueError(f"Unsupported shell: {shell}")


def get_completion_file_path(shell: str) -> Path:
    """Get the default completion file path for the shell."""
    home = Path.home()

    if shell == "bash":
        return home / ".local/share/bash-completion/completions/foodtruck"
    if shell == "zsh":
        return home / ".zsh/completions/_foodtruck"
    if shell == "powershell":
        # PowerShell profile location
        return home / "Documents/WindowsPowerShell/Microsoft.PowerShell_profile.ps1"
    raise ValueError(f"Unsupported shell: {shell}")


def install_completion(shell: str, output_path: Path | None = None) -> bool:
    """Install completion script for the specified shell."""
    try:
        script = get_completion_script(shell)

        if output_path is None:
            output_path = get_completion_file_path(shell)

        # Create parent directories if they don't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Write the completion script
        with output_path.open("w", encoding="utf-8") as f:
            f.write(script)

        # Make executable on Unix systems
        if shell in ["bash", "zsh"]:
            output_path.chmod(0o644)

        return True
    except Exception as e:
        print_error(f"Failed to install {shell} completion: {e}")
        return False


def completion_command(
    shell: str | None = None,
    install: bool = False,
    output: str | None = None,
) -> None:
    """
    Generate shell completion scripts for foodtruck CLI.

    Args:
        shell: Target shell (bash, zsh, powershell). If not specified, shows all.
        install: Install the completion script automatically.
        output: Output file path (optional).
    """
    print_title("🐚 Shell Completion Generator")

    supported_shells = ["bash", "zsh", "powershell"]

    if shell and shell not in supported_shells:
        print_error(f"Unsupported shell: {shell}")
        print_info(f"Supported shells: {', '.join(supported_shells)}")
        sys.exit(1)

    shells_to_process = [shell] if shell else supported_shells

    for current_shell in shells_to_process:
        print_info(f"\n📝 Generating {current_shell} completion...")

        try:
            script = get_completion_script(current_shell)

            if install:
                output_path = (
                    Path(output) if output else get_completion_file_path(current_shell)
                )
                if install_completion(current_shell, output_path):
                    print_success(
                        f"✅ {current_shell} completion installed to: {output_path}"
                    )

                    if current_shell in ["bash", "zsh"]:
                        print_info(
                            "💡 To enable completion, restart your shell or run:"
                        )
                        if current_shell == "bash":
                            print_info(f"   source {output_path}")
                        else:  # zsh
                            print_info("   autoload -U compinit && compinit")
                else:
                    print_error(f"❌ Failed to install {current_shell} completion")
            else:
                # Just print the script
                print_info(f"📄 {current_shell} completion script:")
                print("─" * 50)
                print(script)
                print("─" * 50)

                if not output:
                    default_path = get_completion_file_path(current_shell)
                    print_info(f"💡 To install, save to: {default_path}")

        except Exception as e:
            print_error(f"❌ Failed to generate {current_shell} completion: {e}")

    if install:
        print_info("\n🎉 Completion installation complete!")
        print_info("💡 Restart your shell or reload your profile to enable completion.")
    else:
        print_info(
            "\n💡 To install completion scripts, use: foodtruck completion --install"
        )
