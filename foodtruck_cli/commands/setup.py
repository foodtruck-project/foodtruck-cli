"""
Setup command for Food Truck CLI
"""

import os
import subprocess
import sys
from pathlib import Path

from cyclopts import App
from pydantic import BaseModel, Field

from ..console import (
    print_clone,
    print_command,
    print_error,
    print_info,
    print_newline,
    print_separator,
    print_skip,
    print_step,
    print_subtitle,
    print_success,
    print_title,
    print_warning,
)


class SetupOptions(BaseModel):
    """Options for the setup command."""

    api_repo: str = Field(
        default="https://github.com/foodtruck-project/foodtruck-api.git",
        description="API repository URL",
    )
    website_repo: str = Field(
        default="https://github.com/foodtruck-project/foodtruck-website.git",
        description="Website repository URL",
    )
    target_dir: str = Field(
        default=".", description="Target directory to clone repositories"
    )
    skip_api: bool = Field(default=False, description="Skip API repository setup")
    skip_website: bool = Field(
        default=False, description="Skip website repository setup"
    )


def run_command(cmd: list[str], cwd: Path | None = None) -> bool:
    """Run a command and return success status."""
    try:
        result = subprocess.run(
            cmd, cwd=cwd, capture_output=True, text=True, check=True
        )
        print_success(result.stdout.strip())
    except subprocess.CalledProcessError as e:
        print_error(f"Error running {' '.join(cmd)}: {e.stderr.strip()}")
        return False
    else:
        return True


def clone_repository(repo_url: str, target_path: Path, repo_name: str) -> bool:
    """Clone a repository."""
    print_clone(f"Cloning {repo_name}...")

    if target_path.exists():
        print_warning(f"Directory {target_path} already exists. Skipping clone.")
        return True

    return run_command(["git", "clone", repo_url, str(target_path)])


def setup_api_project(api_path: Path) -> bool:
    """Setup the API project."""
    print_step("Setting up API project...")

    # Check if UV is available
    if not run_command(["uv", "--version"], cwd=api_path):
        print_error("UV is not available. Please install UV first.")
        return False

    # Install dependencies
    if not run_command(["uv", "sync"], cwd=api_path):
        print_error("Failed to install API dependencies.")
        return False

    print_success("API project setup completed!")
    return True


def setup_website_project(website_path: Path) -> bool:
    """Setup the website project."""
    print_step("Setting up Website project...")

    # Check if it's a Node.js project
    package_json = website_path / "package.json"
    if package_json.exists():
        # Install npm dependencies
        if not run_command(["npm", "install"], cwd=website_path):
            print_error("Failed to install website dependencies.")
            return False
    else:
        print_info("No package.json found. Website might not need npm dependencies.")

    print_success("Website project setup completed!")
    return True


def _setup_environment(
    api_repo: str = "https://github.com/foodtruck-project/foodtruck-api.git",
    website_repo: str = "https://github.com/foodtruck-project/foodtruck-website.git",
    target_dir: str = ".",
    skip_api: bool = False,
    skip_website: bool = False,
) -> None:
    """Setup the complete Food Truck development environment."""
    print_title("Food Truck Development Environment Setup")
    print_separator()

    # Parse options
    options = SetupOptions(
        api_repo=api_repo,
        website_repo=website_repo,
        target_dir=target_dir,
        skip_api=skip_api,
        skip_website=skip_website,
    )

    # Create target directory
    target_path = Path(options.target_dir).resolve()
    target_path.mkdir(parents=True, exist_ok=True)

    # Create foodtruck directory inside target directory
    foodtruck_path = target_path / "foodtruck"

    # Check if foodtruck_path exists and is a file (wrapper script)
    if foodtruck_path.exists() and foodtruck_path.is_file():
        print_warning(
            f"{foodtruck_path} is a file (wrapper script). Using different directory name."
        )
        foodtruck_path = target_path / "foodtruck-projects"

    foodtruck_path.mkdir(parents=True, exist_ok=True)

    # Check if foodtruck directory already has content
    if any(foodtruck_path.iterdir()):
        print_warning(
            f"Directory {foodtruck_path} already has content. Please clean it first or use a different target directory."
        )
        sys.exit(1)

    print_info(f"Creating foodtruck directory: {foodtruck_path}")

    # Change to foodtruck directory for operations
    original_cwd = Path.cwd()
    os.chdir(foodtruck_path)

    success = True

    # Setup API
    if not options.skip_api:
        api_path = Path("foodtruck-api")
        if not clone_repository(
            options.api_repo, api_path, "API"
        ) or not setup_api_project(api_path):
            success = False
    else:
        print_skip("Skipping API setup")

    # Setup Website
    if not options.skip_website:
        website_path = Path("foodtruck-website")
        if not clone_repository(
            options.website_repo, website_path, "Website"
        ) or not setup_website_project(website_path):
            success = False
    else:
        print_skip("Skipping Website setup")

    # Restore original directory
    os.chdir(original_cwd)

    if success:
        print_newline()
        print_success("Setup completed successfully!")
        print_newline()
        print_info(f"Projects created in: {foodtruck_path}")
        print_newline()
        print_subtitle("Next steps:")
        print_command("  API: cd foodtruck/foodtruck-api && uv run python -m foodtruck_api.cli.app database init")
        print_command("  Website: cd foodtruck/foodtruck-website && open index.html")
    else:
        print_newline()
        print_error("Setup failed. Please check the errors above.")
        sys.exit(1)


def setup_api_command(
    api_repo: str = "https://github.com/foodtruck-project/foodtruck-api.git",
    target_dir: str = ".",
) -> None:
    """Setup only the API project"""
    _setup_environment(api_repo=api_repo, target_dir=target_dir, skip_website=True)


def setup_website_command(
    website_repo: str = "https://github.com/foodtruck-project/foodtruck-website.git",
    target_dir: str = ".",
) -> None:
    """Setup only the website project"""
    _setup_environment(website_repo=website_repo, target_dir=target_dir, skip_api=True)


def setup_all_command(
    api_repo: str = "https://github.com/foodtruck-project/foodtruck-api.git",
    website_repo: str = "https://github.com/foodtruck-project/foodtruck-website.git",
    target_dir: str = ".",
) -> None:
    """Setup both API and website projects"""
    _setup_environment(api_repo=api_repo, website_repo=website_repo, target_dir=target_dir)


# Create setup sub-app
setup_app = App(name="setup", help="Setup the complete Food Truck development environment")

@setup_app.command
def api(
    api_repo: str = "https://github.com/foodtruck-project/foodtruck-api.git",
    target_dir: str = ".",
):
    """Setup only the API project"""
    setup_api_command(api_repo, target_dir)

@setup_app.command
def website(
    website_repo: str = "https://github.com/foodtruck-project/foodtruck-website.git",
    target_dir: str = ".",
):
    """Setup only the website project"""
    setup_website_command(website_repo, target_dir)

@setup_app.command
def all(
    api_repo: str = "https://github.com/foodtruck-project/foodtruck-api.git",
    website_repo: str = "https://github.com/foodtruck-project/foodtruck-website.git",
    target_dir: str = ".",
):
    """Setup both API and website projects"""
    setup_all_command(api_repo, website_repo, target_dir)


def setup_command() -> None:
    """Setup the complete Food Truck development environment"""
    setup_app()
