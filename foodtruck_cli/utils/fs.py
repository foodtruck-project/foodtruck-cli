from pathlib import Path


def create_dir(target: str) -> Path:
    """Create directory and return resolved path."""
    target_path = Path(target).resolve()
    target_path.mkdir(parents=True, exist_ok=True)
    return target_path


def ensure_project_dir(base_path: Path, project_name: str) -> Path:
    """Ensure project directory exists and return its path."""
    project_path = base_path / project_name
    project_path.mkdir(parents=True, exist_ok=True)
    return project_path


def project_exists(base_path: Path, project_name: str) -> bool:
    """Check if project directory already exists."""
    return (base_path / project_name).exists()


def get_project_path(base_path: Path, project_name: str) -> Path:
    """Get the full path for a project directory."""
    return base_path / project_name
