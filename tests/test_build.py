"""Test the building of the Jupyter Book."""

import json
import subprocess
import shutil
import yaml

JUPYTER_BOOK_BUILD = ["jupyter", "book", "build", "--html", "--ci"]
JUPYTER_BOOK_CLEAN = ["jupyter", "book", "clean", "--html", "--yes"]


def clean_html_build_outputs(build_dir):
    """Remove generated book outputs before a Jupyter Book 2 build test."""
    if not build_dir.exists():
        return

    for child_name in ("html", "site", "exports", "temp"):
        child = build_dir / child_name
        if child.is_dir():
            shutil.rmtree(child)
        elif child.exists():
            child.unlink()


def toc_entries(entries):
    """Yield all entries from a MyST table of contents."""
    for entry in entries:
        yield entry
        yield from toc_entries(entry.get("children", []))


def assert_colab_redirect_matches_built_notebook_slugs(project_root, html_dir):
    """Assert the static Colab redirect covers generated notebook URLs."""
    with open(html_dir / "config.json", "r", encoding="utf-8") as f:
        site_config = json.load(f)

    project = site_config["projects"][0]
    page_entries = list(toc_entries(project["toc"]))[1:]

    with open(project_root / "colab.html", "r", encoding="utf-8") as f:
        colab_redirect = f.read()

    assert len(page_entries) == len(project["pages"])
    for entry, page in zip(page_entries, project["pages"]):
        if not entry.get("file", "").endswith(".ipynb"):
            continue

        slash_slug = page["slug"].replace(".", "/")
        assert page["slug"] in colab_redirect
        assert slash_slug in colab_redirect


def test_jupyter_book_build(project_root):
    """Test that the Jupyter Book can be built successfully."""
    build_dir = project_root / "_build"
    clean_html_build_outputs(build_dir)

    result = subprocess.run(
        JUPYTER_BOOK_BUILD,
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

    # Jupyter Book 2 renders the first TOC entry as the site index.
    intro_file = html_dir / "index.html"

    with open(intro_file, "r", encoding="utf-8") as f:
        content = f.read()

    assert len(content) > 1000, "index.html appears to be too small"
    assert "<html" in content.lower(), "index.html doesn't appear to be valid HTML"
    assert "Pyomo Workshop" in content

    assert_colab_redirect_matches_built_notebook_slugs(project_root, html_dir)


def test_config_validation(project_root):
    """Test that Jupyter Book configuration is valid."""
    config_file = project_root / "myst.yml"
    with open(config_file, "r") as f:
        config = yaml.safe_load(f)

    assert config["version"] == 1
    assert "project" in config, "Config must have project metadata"
    assert "toc" in config["project"], "Config must have a table of contents"
    assert config is not None, "Config file is empty or invalid"


def test_toc_validation(project_root):
    """Test that table of contents is properly structured."""
    config_file = project_root / "myst.yml"
    with open(config_file, "r") as f:
        config = yaml.safe_load(f)

    toc = config["project"]["toc"]
    assert toc is not None, "TOC file is empty or invalid"
    assert toc[0]["file"] == "intro.md"
    assert any(entry.get("children") for entry in toc), "TOC must have nested entries"


def test_clean_build(project_root):
    """Test that cleaning and rebuilding works."""
    # First build
    result1 = subprocess.run(
        JUPYTER_BOOK_BUILD,
        capture_output=True,
        text=True,
        cwd=project_root,
    )
    assert result1.returncode == 0, "Initial build failed"

    # Clean
    result2 = subprocess.run(
        JUPYTER_BOOK_CLEAN,
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
        JUPYTER_BOOK_BUILD,
        capture_output=True,
        text=True,
        cwd=project_root,
    )
    assert result3.returncode == 0, "Rebuild after clean failed"
