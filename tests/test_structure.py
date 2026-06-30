"""Test the basic structure and configuration of the Jupyter Book."""

import yaml


def _toc_entries(entries):
    """Yield all entries from a MyST table of contents."""
    for entry in entries:
        yield entry
        yield from _toc_entries(entry.get("children", []))


def _workflow_run_commands(workflow):
    """Yield run commands from all workflow jobs."""
    for job in workflow.get("jobs", {}).values():
        for step in job.get("steps", []):
            run = step.get("run")
            if run:
                yield run


def test_project_structure(project_root):
    """Test that essential project files and directories exist."""
    # Essential files
    essential_files = [
        "_config.yml",
        "myst.yml",
        "colab.html",
        "requirements.txt",
        "README.md",
        "intro.md",
    ]

    for file_name in essential_files:
        file_path = project_root / file_name
        assert file_path.exists(), f"Essential file {file_name} is missing"
        assert file_path.is_file(), f"{file_name} is not a file"

    assert not (project_root / "_toc.yml").exists(), "_toc.yml is replaced by myst.yml"

    # Essential directories
    essential_dirs = ["Material", ".github", ".github/workflows"]

    for dir_name in essential_dirs:
        dir_path = project_root / dir_name
        assert dir_path.exists(), f"Essential directory {dir_name} is missing"
        assert dir_path.is_dir(), f"{dir_name} is not a directory"


def test_legacy_config_file_valid(config_file):
    """Test that the legacy _config.yml is valid YAML."""
    with open(config_file, "r") as f:
        config = yaml.safe_load(f)

    assert "title" in config, "_config.yml must have a title"
    assert "author" in config, "_config.yml must have an author"
    assert "repository" in config, "_config.yml must have repository info"

    execute_config = config.get("execute", {})
    assert execute_config.get("execute_notebooks") == "off"

    repo_config = config["repository"]
    assert "url" in repo_config, "Repository must have a URL"
    assert "branch" in repo_config, "Repository must specify a branch"


def test_myst_file_valid(myst_file, material_dir):
    """Test that myst.yml is valid and includes the full book TOC."""
    with open(myst_file, "r") as f:
        config = yaml.safe_load(f)

    assert config["version"] == 1
    project = config["project"]
    assert project["title"] == "Pyomo Workshop"
    assert project["github"] == "SECQUOIA/pyomo_jupyter_book"
    assert project["bibliography"] == ["references.bib"]

    toc = project["toc"]
    assert toc[0]["file"] == "intro.md"

    toc_files = {entry["file"] for entry in _toc_entries(toc) if "file" in entry}
    toc_files_in_order = [
        entry["file"] for entry in _toc_entries(toc) if "file" in entry
    ]
    expected_notebooks = {
        str(path.relative_to(myst_file.parent))
        for path in material_dir.rglob("*.ipynb")
    }
    toc_notebooks = {
        file_name for file_name in toc_files if file_name.endswith(".ipynb")
    }

    assert toc_notebooks == expected_notebooks

    for file_name in toc_files:
        assert (myst_file.parent / file_name).exists(), f"{file_name} is missing"

    site = config["site"]
    assert site["template"] == "book-theme"
    assert site["options"]["folders"] is True
    assert site["options"]["logo"] == "logo.png"
    assert any(
        action.get("title") == "Open in Colab" and action.get("url") == "colab.html"
        for action in site["actions"]
    )

    tex_export = project["exports"][0]
    assert tex_export["format"] == "tex"
    assert tex_export["articles"] == toc_files_in_order
    assert tex_export["output"] == "_build/exports/book.tex"


def test_requirements_file_exists(project_root, requirements_file):
    """Test that requirements.txt exists and has basic dependencies."""
    assert requirements_file.exists(), "requirements.txt is missing"

    with open(requirements_file, "r") as f:
        requirements = f.read().lower()

    # Check for essential dependencies
    essential_deps = ["jupyter-book", "pyomo", "matplotlib", "numpy"]
    for dep in essential_deps:
        assert (
            dep in requirements
        ), f"Essential dependency {dep} missing from requirements.txt"

    requirements_in_path = project_root / "requirements.in"
    requirements_in = requirements_in_path.read_text().lower().splitlines()
    jupyter_book_pins = [
        line.strip()
        for line in requirements_in
        if line.strip().startswith("jupyter-book==")
    ]
    assert len(jupyter_book_pins) == 1
    assert jupyter_book_pins[0] in requirements


def test_material_directory_structure(material_dir):
    """Test that Material directory has expected structure."""
    assert material_dir.exists(), "Material directory is missing"
    assert material_dir.is_dir(), "Material is not a directory"

    # Check for expected subdirectories
    expected_subdirs = [
        "Pyomo Fundamentals",
        "Nonlinear Exercises",
        "Dynamic Exercises",
        "GDP Exercises",
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

    with open(main_workflow, "r") as f:
        workflow_content = yaml.safe_load(f)

    assert "name" in workflow_content, "Workflow must have a name"
    assert (
        True in workflow_content or "on" in workflow_content
    ), "Workflow must have triggers"
    assert "jobs" in workflow_content, "Workflow must have jobs"


def test_github_workflows_use_jupyter_book_v2(project_root):
    """Test that CI uses the Jupyter Book 2 build command."""
    workflows_dir = project_root / ".github" / "workflows"
    workflow_files = ["main.yml", "test.yml"]

    for workflow_file in workflow_files:
        with open(workflows_dir / workflow_file, "r") as f:
            workflow_content = yaml.safe_load(f)

        commands = "\n".join(_workflow_run_commands(workflow_content))
        assert "jupyter book build --html --ci" in commands
        assert "jupyter-book build" not in commands
        assert "_toc.yml" not in commands
        assert "myst.yml" in commands or workflow_file == "main.yml"


def test_colab_redirect_covers_toc_notebooks(project_root, myst_file):
    """Test that the static Colab redirect knows every notebook in the TOC."""
    with open(myst_file, "r") as f:
        config = yaml.safe_load(f)

    with open(project_root / "colab.html", "r", encoding="utf-8") as f:
        colab_redirect = f.read()

    toc_files = {
        entry["file"]
        for entry in _toc_entries(config["project"]["toc"])
        if entry.get("file", "").endswith(".ipynb")
    }

    for file_name in toc_files:
        assert file_name in colab_redirect, f"{file_name} is missing from colab.html"
