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
import tarfile
import urllib.request
import zipfile
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


def get_carapace_download_url() -> str:
    """Get the appropriate carapace-bin download URL for the current platform"""
    version = "1.4.1"

    if platform.system() == "Windows":
        return f"https://github.com/carapace-sh/carapace-bin/releases/download/v{version}/carapace-bin_{version}_windows_amd64.zip"
    if platform.system() == "Darwin":  # macOS
        return f"https://github.com/carapace-sh/carapace-bin/releases/download/v{version}/carapace-bin_{version}_darwin_amd64.tar.gz"
    # For Linux and other Unix-like systems
    return f"https://github.com/carapace-sh/carapace-bin/releases/download/v{version}/carapace-bin_{version}_linux_386.tar.gz"


def download_carapace(script_dir: Path) -> Path:
    """Download and extract carapace-bin"""
    url = get_carapace_download_url()
    filename = url.split("/")[-1]
    download_path = script_dir / filename

    # Check if the download file already exists
    if download_path.exists():
        print_warning(f"Arquivo já existe: {download_path}")
        print_step("Usando arquivo existente...")
    else:
        print_step(f"Baixando carapace-bin: {filename}")
        try:
            # Download the file
            urllib.request.urlretrieve(url, download_path)
            print_success(f"Download concluído: {download_path}")
        except Exception as e:
            print_error(f"Erro ao baixar carapace-bin: {e}")
            sys.exit(1)

    try:
        # Extract the file
        extract_dir = script_dir / "carapace-bin"
        extract_dir.mkdir(exist_ok=True)

        if filename.endswith(".zip"):
            # Windows zip file
            with zipfile.ZipFile(download_path, "r") as zip_ref:
                zip_ref.extractall(extract_dir)
        else:
            # Linux tar.gz file
            with tarfile.open(download_path, "r:gz") as tar_ref:
                tar_ref.extractall(extract_dir)

        print_success(f"Carapace-bin extraído para: {extract_dir}")

        # Clean up the downloaded file
        download_path.unlink()
        print_success("Arquivo de download removido")

        # Find the carapace executable
        carapace_exe = None
        for file in extract_dir.rglob("*"):
            if file.is_file() and file.name in {"carapace", "carapace.exe"}:
                carapace_exe = file
                break

        if carapace_exe:
            # Make executable on Unix systems
            if platform.system() != "Windows":
                carapace_exe.chmod(0o755)
            print_success(f"Carapace-bin instalado: {carapace_exe}")
            return carapace_exe
        print_error("Executável carapace não encontrado no arquivo extraído")
        sys.exit(1)

    except Exception as e:
        print_error(f"Erro ao extrair carapace-bin: {e}")
        if download_path.exists():
            download_path.unlink()
        sys.exit(1)


def install_carapace(script_dir: Path) -> None:
    """Install carapace-bin if not already present"""
    carapace_dir = script_dir / "carapace-bin"

    # Check if carapace is already installed
    if carapace_dir.exists():
        carapace_exe = None
        for file in carapace_dir.rglob("*"):
            if file.is_file() and file.name in {"carapace", "carapace.exe"}:
                carapace_exe = file
                break

        if carapace_exe:
            print_warning(f"Carapace-bin já instalado: {carapace_exe}")
            return

    # Download and install carapace-bin
    download_carapace(script_dir)





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

    # Install carapace-bin
    print_step("Instalando carapace-bin...")
    install_carapace(script_dir)

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
