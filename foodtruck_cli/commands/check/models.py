"""Data models for check command."""

from enum import Enum
from typing import NamedTuple


class DependencyStatus(NamedTuple):
    """Status of a dependency check."""

    is_ok: bool
    message: str


class DependencyType(Enum):
    """Types of dependencies to check."""

    PYTHON = "Python 3.13"
    UV = "UV"
    GIT = "Git"
    DOCKER = "Docker"
    DOCKER_DAEMON = "Docker Daemon"


class CheckResult(NamedTuple):
    """Result of all dependency checks."""

    results: dict[str, DependencyStatus]
    all_ok: bool

    @classmethod
    def from_results(cls, results: dict[str, DependencyStatus]) -> "CheckResult":
        """Create CheckResult from dependency results."""
        all_ok = all(status.is_ok for status in results.values())
        return cls(results=results, all_ok=all_ok)
