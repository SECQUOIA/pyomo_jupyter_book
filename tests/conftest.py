"""Test configuration file for the Pyomo Jupyter Book project."""

import pytest
from pathlib import Path

# Get the root directory of the project
PROJECT_ROOT = Path(__file__).parent.parent


@pytest.fixture
def project_root():
    """Return the project root directory."""
    return PROJECT_ROOT


@pytest.fixture
def material_dir():
    """Return the Material directory containing notebooks."""
    return PROJECT_ROOT / "Material"


@pytest.fixture
def config_file():
    """Return the _config.yml file path."""
    return PROJECT_ROOT / "_config.yml"


@pytest.fixture
def toc_file():
    """Return the _toc.yml file path."""
    return PROJECT_ROOT / "_toc.yml"


@pytest.fixture
def requirements_file():
    """Return the requirements.txt file path."""
    return PROJECT_ROOT / "requirements.txt"
