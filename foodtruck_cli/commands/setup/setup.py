"""
Setup command for Food Truck CLI
"""

from pathlib import Path

from foodtruck_cli.commands.setup.models import ProjectSetupResult, SetupOptions

from ...utils.console import (
    print_info,
    print_separator,
    print_setup_failure_message,
    print_setup_success_message,
    print_skip,
    print_step,
    print_success,
    print_title,
)
from ...utils.fs import get_project_path, project_exists
from ...utils.git import clone_repository
from ...utils.run_command import run_command


def _install_api_dependencies(
    project_path: Path, project_name: str
) -> ProjectSetupResult:
    """Install project dependencies using UV."""
    print_step(f"Setting up {project_name} dependencies...")

    if not run_command(["uv", "--version"], cwd=project_path):
        return ProjectSetupResult(
            success=False, message="UV is not available. Please install UV first."
        )

    if not run_command(["uv", "sync"], cwd=project_path):
        return ProjectSetupResult(
            success=False, message=f"Failed to install {project_name} dependencies."
        )

    print_success(f"{project_name} dependencies setup completed!")
    return ProjectSetupResult(
        success=True, message=f"{project_name} dependencies setup completed!"
    )


def _setup_project(
    target_path: Path,
    project_name: str,
    repo_url: str,
    skip_flag: bool,
) -> ProjectSetupResult:
    """Setup a single project (clone and optionally setup dependencies)."""

    if skip_flag:
        print_skip(f"Skipping {project_name} setup")
        return ProjectSetupResult(
            success=True, message=f"Skipping {project_name} setup"
        )

    project_path = get_project_path(target_path, project_name)

    if project_exists(target_path, project_name):
        print_info(f"{project_name} directory already exists, skipping clone")
        return ProjectSetupResult(success=True, project_path=project_path)

    cloned = clone_repository(repo_url, project_path)

    if not cloned:
        return ProjectSetupResult(
            success=False, message=f"Failed to clone {project_name}"
        )

    if "api" in project_name.lower():
        result = _install_api_dependencies(project_path, project_name)
        if not result.success:
            return result

    return ProjectSetupResult(success=True, project_path=project_path)


def setup_environment(setup_options: SetupOptions) -> None:
    """Setup the complete Food Truck development environment."""
    print_title("Food Truck Development Environment Setup")
    print_separator()

    target_path = setup_options.get_target_path()
    print_info(f"Target directory: {target_path}")

    api_result = _setup_project(
        target_path=target_path,
        project_name="foodtruck-api",
        repo_url=setup_options.api_repo,
        skip_flag=not setup_options.should_setup_api(),
    )

    website_result = _setup_project(
        target_path=target_path,
        project_name="foodtruck-website",
        repo_url=setup_options.website_repo,
        skip_flag=not setup_options.should_setup_website(),
    )

    if api_result.success and website_result.success:
        print_setup_success_message(target_path)
    else:
        print_setup_failure_message(api_result, website_result)
