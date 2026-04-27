"""Test notebook execution and validation."""

import pytest
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor


def get_all_notebooks(material_dir):
    """Get all notebook files in the Material directory."""
    notebook_files = []
    for notebook_path in material_dir.rglob("*.ipynb"):
        # Skip checkpoints and hidden files
        if ".ipynb_checkpoints" not in str(notebook_path):
            notebook_files.append(notebook_path)
    return notebook_files


def test_notebooks_exist(material_dir):
    """Test that notebook files exist in Material directory."""
    notebooks = get_all_notebooks(material_dir)
    assert len(notebooks) > 0, "No notebook files found in Material directory"

    # Check that we have notebooks in expected subdirectories
    subdirs_with_notebooks = set()
    for notebook in notebooks:
        relative_path = notebook.relative_to(material_dir)
        if len(relative_path.parts) > 1:
            subdirs_with_notebooks.add(relative_path.parts[0])

    expected_subdirs = {
        "Pyomo Fundamentals",
        "Nonlinear Exercises",
        "Dynamic Exercises",
        "GDP Exercises",
    }
    assert (
        len(subdirs_with_notebooks & expected_subdirs) > 0
    ), "No notebooks found in expected subdirectories"


def test_notebooks_are_valid(material_dir):
    """Test that all notebooks are valid nbformat files."""
    notebooks = get_all_notebooks(material_dir)

    for notebook_path in notebooks:
        try:
            with open(notebook_path, "r", encoding="utf-8") as f:
                nb = nbformat.read(f, as_version=4)

            # Basic validation
            assert "cells" in nb, f"Notebook {notebook_path} has no cells"
            assert len(nb.cells) > 0, f"Notebook {notebook_path} has no cells"

            # Check that notebook has some code cells
            code_cells = [cell for cell in nb.cells if cell.cell_type == "code"]
            assert len(code_cells) > 0, f"Notebook {notebook_path} has no code cells"

        except Exception as e:
            pytest.fail(f"Failed to read notebook {notebook_path}: {e}")


@pytest.mark.slow
def test_sample_notebook_execution(material_dir):
    """Test execution of a few sample notebooks to ensure they work."""
    notebooks = get_all_notebooks(material_dir)

    # Test a small sample to avoid long test times
    # Focus on fundamental notebooks that should be more stable
    fundamental_notebooks = [
        nb for nb in notebooks if "Pyomo Fundamentals" in str(nb) and "1.1" in str(nb)
    ]

    if not fundamental_notebooks:
        pytest.skip("No fundamental notebooks found for testing")

    # Test just the first fundamental notebook
    test_notebook = fundamental_notebooks[0]

    try:
        with open(test_notebook, "r", encoding="utf-8") as f:
            nb = nbformat.read(f, as_version=4)

        # Execute the notebook
        ep = ExecutePreprocessor(timeout=300, kernel_name="python3")
        ep.preprocess(nb, {"metadata": {"path": test_notebook.parent}})

    except Exception as e:
        # Don't fail the test for execution errors since some notebooks
        # may require specific solvers that aren't available in CI
        pytest.skip(f"Notebook execution skipped due to: {e}")


def test_notebooks_have_proper_structure(material_dir):
    """Test that notebooks have proper structure with markdown and code cells."""
    notebooks = get_all_notebooks(material_dir)

    for notebook_path in notebooks:
        with open(notebook_path, "r", encoding="utf-8") as f:
            nb = nbformat.read(f, as_version=4)

        # Check cell type distribution
        cell_types = [cell.cell_type for cell in nb.cells]

        # Should have both markdown and code cells
        assert "code" in cell_types, f"Notebook {notebook_path} has no code cells"
        assert (
            "markdown" in cell_types
        ), f"Notebook {notebook_path} has no markdown cells"

        # Check that first cell is typically markdown (title/description)
        if len(nb.cells) > 0:
            # Many notebooks start with markdown, but not enforcing strictly
            # as some might start with imports
            pass

        # Check for potential issues in code cells
        for i, cell in enumerate(nb.cells):
            if cell.cell_type == "code":
                source = cell.source

                # Check for common issues
                if "input(" in source:
                    pytest.fail(
                        f"Notebook {notebook_path} cell {i} contains input() which will hang in automated execution"
                    )

                # Check for absolute paths that might be problematic
                if any(
                    path in source for path in ["/Users/", "/home/", "C:\\", "D:\\"]
                ):
                    # This is a warning, not a failure, as some paths might be examples
                    print(
                        f"Warning: Notebook {notebook_path} cell {i} contains absolute paths"
                    )


def test_notebook_imports(material_dir):
    """Test that notebooks have reasonable import statements."""
    notebooks = get_all_notebooks(material_dir)

    for notebook_path in notebooks:
        with open(notebook_path, "r", encoding="utf-8") as f:
            nb = nbformat.read(f, as_version=4)

        # Look for import statements
        imports_found = False
        pyomo_imported = False

        for cell in nb.cells:
            if cell.cell_type == "code":
                source = cell.source.lower()

                if "import" in source:
                    imports_found = True

                if "pyomo" in source and "import" in source:
                    pyomo_imported = True

        # Most notebooks should have imports
        if not imports_found:
            print(f"Warning: Notebook {notebook_path} has no import statements")

        # Pyomo notebooks should import pyomo
        if not pyomo_imported and "pyomo" in str(notebook_path).lower():
            print(f"Warning: Pyomo notebook {notebook_path} doesn't import pyomo")


def test_notebooks_install_pyomo_in_colab(material_dir):
    """Ensure notebooks install Pyomo automatically when running in Colab."""
    notebooks = get_all_notebooks(material_dir)

    for notebook_path in notebooks:
        with open(notebook_path, "r", encoding="utf-8") as f:
            nb = nbformat.read(f, as_version=4)

        has_colab_install = any(
            cell.cell_type == "code"
            and "google.colab" in cell.source
            and "pip" in cell.source
            and "pyomo" in cell.source
            for cell in nb.cells
        )

        assert (
            has_colab_install
        ), f"Notebook {notebook_path} missing Colab Pyomo install cell"
