"""
Food Truck CLI Check Commands Package
"""

from .app import check_app
from .command import check_dependencies_command

# Legacy compatibility
check_command = check_dependencies_command

__all__ = [
    "check_app",
    "check_command",
    "check_dependencies_command"
]
