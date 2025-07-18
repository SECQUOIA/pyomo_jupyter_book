"""Test the basic structure and configuration of the Jupyter Book."""

import pytest
import yaml
from pathlib import Path


def test_project_structure(project_root):
    """Test that essential project files and directories exist."""
    # Essential files
    essential_files = [
        "_config.yml",
        "_toc.yml", 
        "requirements.txt",
        "README.md",
        "intro.md"
    ]
    
    for file_name in essential_files:
        file_path = project_root / file_name
        assert file_path.exists(), f"Essential file {file_name} is missing"
        assert file_path.is_file(), f"{file_name} is not a file"
    
    # Essential directories
    essential_dirs = [
        "Material",
        ".github",
        ".github/workflows"
    ]
    
    for dir_name in essential_dirs:
        dir_path = project_root / dir_name
        assert dir_path.exists(), f"Essential directory {dir_name} is missing"
        assert dir_path.is_dir(), f"{dir_name} is not a directory"


def test_config_file_valid(config_file):
    """Test that _config.yml is valid YAML."""
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    
    # Check essential configuration keys
    assert 'title' in config, "_config.yml must have a title"
    assert 'author' in config, "_config.yml must have an author"
    assert 'repository' in config, "_config.yml must have repository info"
    
    # Check repository configuration
    repo_config = config['repository']
    assert 'url' in repo_config, "Repository must have a URL"
    assert 'branch' in repo_config, "Repository must specify a branch"


def test_toc_file_valid(toc_file):
    """Test that _toc.yml is valid YAML."""
    with open(toc_file, 'r') as f:
        toc = yaml.safe_load(f)
    
    # Check that TOC has required structure
    assert 'format' in toc, "_toc.yml must specify format"
    assert 'root' in toc, "_toc.yml must specify root document"
    
    # Check that root document exists
    root_doc = toc['root']
    if not root_doc.endswith('.md'):
        root_doc += '.md'
    root_path = toc_file.parent / root_doc
    assert root_path.exists(), f"Root document {root_doc} not found"


def test_requirements_file_exists(requirements_file):
    """Test that requirements.txt exists and has basic dependencies."""
    assert requirements_file.exists(), "requirements.txt is missing"
    
    with open(requirements_file, 'r') as f:
        requirements = f.read().lower()
    
    # Check for essential dependencies
    essential_deps = ['jupyter-book', 'pyomo', 'matplotlib', 'numpy']
    for dep in essential_deps:
        assert dep in requirements, f"Essential dependency {dep} missing from requirements.txt"


def test_material_directory_structure(material_dir):
    """Test that Material directory has expected structure."""
    assert material_dir.exists(), "Material directory is missing"
    assert material_dir.is_dir(), "Material is not a directory"
    
    # Check for expected subdirectories
    expected_subdirs = [
        "Pyomo Fundamentals",
        "Nonlinear Exercises", 
        "Dynamic Exercises",
        "GDP Exercises"
    ]
    
    for subdir in expected_subdirs:
        subdir_path = material_dir / subdir
        assert subdir_path.exists(), f"Expected subdirectory {subdir} is missing"
        assert subdir_path.is_dir(), f"{subdir} is not a directory"


def test_github_workflows_exist(project_root):
    """Test that GitHub workflows exist."""
    workflows_dir = project_root / ".github" / "workflows"
    assert workflows_dir.exists(), ".github/workflows directory is missing"
    
    # Check for main deployment workflow
    main_workflow = workflows_dir / "main.yml"
    assert main_workflow.exists(), "main.yml workflow is missing"
    
    with open(main_workflow, 'r') as f:
        workflow_content = yaml.safe_load(f)
    
    assert 'name' in workflow_content, "Workflow must have a name"
    assert True in workflow_content or 'on' in workflow_content, "Workflow must have triggers"
    assert 'jobs' in workflow_content, "Workflow must have jobs"