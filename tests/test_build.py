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

    # Try to build the book (without --quiet as it may not be supported in all versions)
    result = subprocess.run(
        ["jupyter-book", "build", str(project_root)],
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
    import yaml
    
    # Validate _config.yml by loading it
    with open("_config.yml", "r") as f:
        config = yaml.safe_load(f)
    
    # Check for essential config fields
    assert "title" in config, "Config must have a title"
    # Config is valid if we can load it without errors
    assert config is not None, "Config file is empty or invalid"


def test_toc_validation(project_root):
    """Test that table of contents is properly structured."""
    import yaml
    
    # Validate _toc.yml by loading it
    toc_file = project_root / "_toc.yml"
    with open(toc_file, "r") as f:
        toc = yaml.safe_load(f)
    
    # Check for essential TOC structure
    assert toc is not None, "TOC file is empty or invalid"
    # Most TOCs have either 'chapters' or 'parts' or 'format'
    assert any(key in toc for key in ["chapters", "parts", "format", "root"]), \
        "TOC must have expected structure (chapters, parts, format, or root)"


def test_clean_build(project_root):
    """Test that cleaning and rebuilding works."""
    # First build
    result1 = subprocess.run(
        ["jupyter-book", "build", str(project_root)],
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
        ["jupyter-book", "build", str(project_root)],
        capture_output=True,
        text=True,
        cwd=project_root,
    )
    assert result3.returncode == 0, "Rebuild after clean failed"
