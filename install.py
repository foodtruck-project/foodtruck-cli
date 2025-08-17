#!/usr/bin/env python3
"""
Cross-platform installation script for Food Truck CLI
Replaces the functionality of install.sh
"""

import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path


def print_success(text: str) -> None:
    """Print success message"""
    print(f"\033[0;32m✅ {text}\033[0m")


def print_error(text: str) -> None:
    """Print error message"""
    print(f"\033[0;31m❌ {text}\033[0m")


def print_warning(text: str) -> None:
    """Print warning message"""
    print(f"\033[1;33m⚠️  {text}\033[0m")


def print_info(text: str) -> None:
    """Print info message"""
    print(f"\033[0;34mi  {text}\033[0m")


def print_step(text: str) -> None:
    """Print step message"""
    print(f"\033[0;34m🔧 {text}\033[0m")


def print_title(text: str) -> None:
    """Print title message"""
    print(f"\033[0;34m🚚 {text}\033[0m")


def get_script_dir() -> Path:
    """Get the directory where this script is located"""
    return Path(__file__).parent.absolute()


def check_uv_installed() -> bool:
    """Check if UV is installed and available in PATH"""
    return shutil.which("uv") is not None


def create_wrapper_script(script_dir: Path) -> None:
    """Create a wrapper script for the CLI"""
    wrapper_script = script_dir / "foodtruck"

    if platform.system() == "Windows":
        # Windows batch file
        wrapper_content = f"""@echo off
cd /d "{script_dir}"
uv run foodtruck %*
"""
        wrapper_script = wrapper_script.with_suffix(".bat")
    else:
        # Unix shell script
        wrapper_content = """#!/bin/bash
# Wrapper script for foodtruck CLI
cd "$(dirname "$0")"
uv run foodtruck "$@"
"""

    # Check if wrapper script already exists
    if wrapper_script.exists():
        print_warning(f"Script wrapper já existe: {wrapper_script}")
        return

    try:
        with wrapper_script.open("w", encoding="utf-8") as f:
            f.write(wrapper_content)

        # Make executable on Unix systems
        if platform.system() != "Windows":
            wrapper_script.chmod(0o755)

        print_success("Script wrapper criado")
    except PermissionError:
        print_error(f"Erro de permissão ao criar script: {wrapper_script}")
        sys.exit(1)
    except Exception as e:
        print_error(f"Erro ao criar script wrapper: {e}")
        sys.exit(1)


def detect_shell() -> tuple[str | None, Path | None]:
    """Detect the current shell and its configuration file"""
    shell = os.environ.get("SHELL", "")
    home = Path.home()

    if "zsh" in shell:
        return "zsh", home / ".zshrc"
    if "bash" in shell:
        return "bash", home / ".bashrc"
    if platform.system() == "Windows":
        # On Windows, we'll use PowerShell profile
        powershell_profile = (
            home
            / "Documents"
            / "WindowsPowerShell"
            / "Microsoft.PowerShell_profile.ps1"
        )
        return "powershell", powershell_profile
    return None, None


def add_to_path(script_dir: Path, shell_config: Path, shell_name: str) -> None:
    """Add the script directory to PATH in shell configuration"""
    if not shell_config.exists():
        # Create the directory if it doesn't exist (for PowerShell on Windows)
        shell_config.parent.mkdir(parents=True, exist_ok=True)
        shell_config.touch()

    # Read existing content
    try:
        with shell_config.open(encoding="utf-8") as f:
            content = f.read()
    except UnicodeDecodeError:
        # Try with different encoding
        with shell_config.open(encoding="latin-1") as f:
            content = f.read()

    # Check if already configured
    path_entry = str(script_dir)
    if path_entry in content:
        print_warning(f"PATH já configurado em {shell_config}")
        return

    # Add to configuration
    with shell_config.open("a", encoding="utf-8") as f:
        f.write("\n# Food Truck CLI\n")
        if platform.system() == "Windows" and shell_name == "powershell":
            f.write(f'$env:PATH = "{script_dir};" + $env:PATH\n')
        else:
            f.write(f'export PATH="{script_dir}:$PATH"\n')

    print_success(f"Adicionado ao {shell_config}")


def install_package() -> None:
    """Install the package using UV"""
    try:
        subprocess.run(
            ["uv", "pip", "install", "-e", "."],
            capture_output=True,
            text=True,
            check=True,
        )
        print_success("Pacote instalado com sucesso")
    except subprocess.CalledProcessError as e:
        print_error(f"Erro ao instalar pacote: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print_error("UV não encontrado no PATH")
        sys.exit(1)


def install_completion_scripts(shell_name: str, shell_config: Path) -> None:
    """Install completion scripts for the detected shell"""
    try:
        # Import the completion command after package installation
        from foodtruck_cli.commands.completion import (
            get_completion_file_path,
            install_completion,
        )

        print_step("Instalando scripts de completion...")

        if shell_name in ["bash", "zsh"]:
            # Install completion script
            completion_path = get_completion_file_path(shell_name)
            if install_completion(shell_name, completion_path):
                print_success(
                    f"Completion {shell_name} instalado em: {completion_path}"
                )

                # Add completion source to shell config if not already present
                with shell_config.open("r", encoding="utf-8") as f:
                    content = f.read()

                completion_source = ""
                if shell_name == "bash":
                    completion_source = f"source {completion_path}"
                elif shell_name == "zsh":
                    completion_source = "autoload -U compinit && compinit"

                if completion_source and completion_source not in content:
                    with shell_config.open("a", encoding="utf-8") as f:
                        f.write(f"\n# Food Truck CLI Completion\n{completion_source}\n")
                    print_success(f"Completion configurado em {shell_config}")
                else:
                    print_warning(f"Completion já configurado em {shell_config}")
            else:
                print_warning(f"Falha ao instalar completion {shell_name}")

        elif shell_name == "powershell":
            # For PowerShell, we'll add the completion script to the profile
            completion_script = Path(__file__).parent / "completions" / "foodtruck.ps1"
            if completion_script.exists():
                with shell_config.open("a", encoding="utf-8") as f:
                    f.write(f"\n# Food Truck CLI Completion\n. '{completion_script}'\n")
                print_success(f"Completion PowerShell configurado em {shell_config}")
            else:
                print_warning("Script de completion PowerShell não encontrado")

    except ImportError:
        print_warning(
            "Não foi possível instalar completion scripts (pacote não instalado)"
        )
    except Exception as e:
        print_warning(f"Erro ao instalar completion: {e}")


def main():
    """Main installation function"""
    print_title("Configurando Food Truck CLI...")

    # Get script directory
    script_dir = get_script_dir()

    # Check if UV is installed
    if not check_uv_installed():
        print_error(
            "UV não está instalado. Instale em: https://docs.astral.sh/uv/getting-started/installation/"
        )
        sys.exit(1)

    # Create wrapper script
    create_wrapper_script(script_dir)

    # Detect shell and configure PATH
    shell_name, shell_config = detect_shell()

    if shell_name and shell_config:
        print_step(f"Configurando {shell_name}...")
        add_to_path(script_dir, shell_config, shell_name)
    else:
        print_warning(
            "Shell não detectado. Adicione manualmente ao seu arquivo de configuração:"
        )
        if platform.system() == "Windows":
            print(f'$env:PATH = "{script_dir};" + $env:PATH')
        else:
            print(f'export PATH="{script_dir}:$PATH"')

    # Install the package
    print_step("Instalando pacote...")
    install_package()

    # Install completion scripts
    if shell_name and shell_config:
        install_completion_scripts(shell_name, shell_config)

    # Success message
    print_success("Instalação concluída!")

    if shell_config:
        print_warning("💡 Recarregue seu terminal ou execute:")
        if platform.system() == "Windows" and shell_name == "powershell":
            print(f". {shell_config}")
        else:
            print(f"source {shell_config}")

    print()
    print_success("🚀 Use o CLI com:")
    if platform.system() == "Windows":
        print("foodtruck.bat")
    else:
        print("foodtruck")

    print()
    print_step("🔧 Para desenvolvimento:")
    print("uv run task cli")


if __name__ == "__main__":
    main()
