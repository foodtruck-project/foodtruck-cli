"""
Setup command for Food Truck CLI
"""

import os
import subprocess
import sys
from pathlib import Path

from pydantic import BaseModel, Field


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
        print(f"✅ {result.stdout.strip()}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running {' '.join(cmd)}: {e.stderr.strip()}")
        return False
    else:
        return True


def clone_repository(repo_url: str, target_path: Path, repo_name: str) -> bool:
    """Clone a repository."""
    print(f"🚀 Cloning {repo_name}...")

    if target_path.exists():
        print(f"⚠️  Directory {target_path} already exists. Skipping clone.")
        return True

    return run_command(["git", "clone", repo_url, str(target_path)])


def setup_api_project(api_path: Path) -> bool:
    """Setup the API project."""
    print("🔧 Setting up API project...")

    # Check if UV is available
    if not run_command(["uv", "--version"], cwd=api_path):
        print("❌ UV is not available. Please install UV first.")
        return False

    # Install dependencies
    if not run_command(["uv", "sync"], cwd=api_path):
        print("❌ Failed to install API dependencies.")
        return False

    print("✅ API project setup completed!")
    return True


def setup_website_project(website_path: Path) -> bool:
    """Setup the website project."""
    print("🔧 Setting up Website project...")

    # Check if it's a Node.js project
    package_json = website_path / "package.json"
    if package_json.exists():
        # Install npm dependencies
        if not run_command(["npm", "install"], cwd=website_path):
            print("❌ Failed to install website dependencies.")
            return False
    else:
        print("i  No package.json found. Website might not need npm dependencies.")

    print("✅ Website project setup completed!")
    return True


def setup_command(
    api_repo: str = "https://github.com/foodtruck-project/foodtruck-api.git",
    website_repo: str = "https://github.com/foodtruck-project/foodtruck-website.git",
    target_dir: str = ".",
    skip_api: bool = False,
    skip_website: bool = False,
) -> None:
    """
    Setup the complete Food Truck development environment.

    This command will clone both the API and website repositories
    and install their dependencies.
    """
    print("🚚 Food Truck Development Environment Setup")
    print("=" * 50)

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
    foodtruck_path.mkdir(parents=True, exist_ok=True)

    # Check if foodtruck directory already has content
    if any(foodtruck_path.iterdir()):
        print(
            f"⚠️  Directory {foodtruck_path} already has content. Please clean it first or use a different target directory."
        )
        sys.exit(1)

    print(f"📁 Creating foodtruck directory: {foodtruck_path}")

    # Change to foodtruck directory for operations
    original_cwd = Path.cwd()
    os.chdir(foodtruck_path)

    success = True

    # Setup API
    if not options.skip_api:
        api_path = Path("foodtruck-api")
        if not clone_repository(options.api_repo, api_path, "API") or not setup_api_project(api_path):
            success = False
    else:
        print("⏭️  Skipping API setup")

    # Setup Website
    if not options.skip_website:
        website_path = Path("foodtruck-website")
        if not clone_repository(options.website_repo, website_path, "Website") or not setup_website_project(website_path):
            success = False
    else:
        print("⏭️  Skipping Website setup")

    # Restore original directory
    os.chdir(original_cwd)

    if success:
        print("\n🎉 Setup completed successfully!")
        print(f"\n📁 Projects created in: {foodtruck_path}")
        print("\n📋 Next steps:")
        print(
            "  API: cd foodtruck/foodtruck-api && uv run python -m foodtruck_api.cli.app database init"
        )
        print("  Website: cd foodtruck/foodtruck-website && open index.html")
    else:
        print("\n💥 Setup failed. Please check the errors above.")
        sys.exit(1)
