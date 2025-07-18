"""Test the building of the Jupyter Book."""

import pytest
import subprocess
import shutil


def test_jupyter_book_build(project_root):
    """Test that the Jupyter Book can be built successfully."""
    # Clean previous build if it exists
    build_dir = project_root / "_build"
    if build_dir.exists():
        shutil.rmtree(build_dir)

    # Try to build the book
    result = subprocess.run(
        ["jupyter-book", "build", str(project_root), "--quiet"],
        capture_output=True,
        text=True,
        cwd=project_root,
    )

    # Check that build succeeded (allow warnings but not errors)
    assert result.returncode == 0, f"Jupyter Book build failed:\n{result.stderr}"

    # Check that essential output files were created
    html_dir = build_dir / "html"
    assert html_dir.exists(), "HTML output directory was not created"

    index_file = html_dir / "index.html"
    assert index_file.exists(), "index.html was not created"

    # Check for intro.html which is the actual content page
    intro_file = html_dir / "intro.html"
    assert intro_file.exists(), "intro.html was not created"

    # Check that intro.html has reasonable content
    with open(intro_file, "r", encoding="utf-8") as f:
        content = f.read()

    assert len(content) > 1000, "intro.html appears to be too small"
    assert "<html" in content.lower(), "intro.html doesn't appear to be valid HTML"


def test_config_validation():
    """Test that Jupyter Book configuration is valid."""
    result = subprocess.run(
        ["jupyter-book", "config", "sphinx", "."], capture_output=True, text=True
    )

    # This command should succeed if config is valid
    assert result.returncode == 0, f"Config validation failed:\n{result.stderr}"


def test_toc_validation(project_root):
    """Test that table of contents is properly structured."""
    # Try to parse the TOC by building just the structure
    result = subprocess.run(
        ["jupyter-book", "toc", "from-project", str(project_root)],
        capture_output=True,
        text=True,
        cwd=project_root,
    )

    # This should succeed if TOC is valid
    # Note: This command might not exist in all versions, so we allow it to fail gracefully
    if result.returncode != 0 and "command not found" not in result.stderr:
        pytest.fail(f"TOC validation failed:\n{result.stderr}")


def test_clean_build(project_root):
    """Test that cleaning and rebuilding works."""
    # First build
    result1 = subprocess.run(
        ["jupyter-book", "build", str(project_root), "--quiet"],
        capture_output=True,
        text=True,
        cwd=project_root,
    )
    assert result1.returncode == 0, "Initial build failed"

    # Clean
    result2 = subprocess.run(
        ["jupyter-book", "clean", str(project_root)],
        capture_output=True,
        text=True,
        cwd=project_root,
    )
    assert result2.returncode == 0, "Clean command failed"

    # Check that build directory was cleaned
    build_dir = project_root / "_build"
    if build_dir.exists():
        # Some files might remain, but HTML should be gone
        html_dir = build_dir / "html"
        assert (
            not html_dir.exists() or len(list(html_dir.iterdir())) == 0
        ), "HTML directory was not properly cleaned"

    # Rebuild
    result3 = subprocess.run(
        ["jupyter-book", "build", str(project_root), "--quiet"],
        capture_output=True,
        text=True,
        cwd=project_root,
    )
    assert result3.returncode == 0, "Rebuild after clean failed"
