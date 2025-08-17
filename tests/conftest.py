"""
Pytest configuration for Food Truck CLI tests
"""
from pathlib import Path

import pytest


@pytest.fixture
def project_root():
    """Return the project root directory"""
    return Path(__file__).parent.parent


@pytest.fixture
def cli_command():
    """Return the CLI command to run"""
    return ["uv", "run", "foodtruck"]
