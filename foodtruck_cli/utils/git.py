from pathlib import Path

from .console import print_clone, print_warning
from .run_command import run_command


def clone_repository(repo_url: str, target_path: Path) -> bool:
    """Clone a repository."""
    print_clone(f"Cloning {repo_url}...")

    if target_path.exists():
        print_warning(f"Directory {target_path} already exists. Skipping clone.")
        return None

    return run_command(["git", "clone", repo_url, str(target_path)])