# Coding Agent Instructions for Pyomo Jupyter Book

## Project Overview
This is a Jupyter Book project that converts Pyomo workshop materials into an interactive web book. The project includes optimization examples, exercises, and tutorials using Pyomo for mathematical optimization.

## Code Style and Standards
- Follow PEP 8 Python style guidelines.
- Use meaningful variable names, especially for optimization models, such as `model`, `solver`, and `constraints`.
- Comment complex optimization formulations and mathematical expressions.
- Prefer Pyomo's concrete model approach for examples.
- Use proper docstrings for functions and classes.

## Project Structure
- `Material/` contains the Jupyter notebooks organized by topic.
- `_config.yml` is the Jupyter Book configuration.
- `_toc.yml` is the table of contents structure.
- `requirements.in` contains direct Python dependency inputs.
- `requirements.txt` is the generated pinned Python dependency lock.
- `venv_requirements.txt` is a compatibility alias that delegates to `requirements.txt`.
- `tests/` contains validation tests.
- `.github/workflows/` contains CI/CD workflows.

## Optimization-Specific Guidelines
- Always import Pyomo as `import pyomo.environ as pyo`.
- Use descriptive names for optimization components:
  - Models: `model = pyo.ConcreteModel()`
  - Variables: `model.x = pyo.Var(...)`
  - Constraints: `model.constraint_name = pyo.Constraint(...)`
  - Objectives: `model.objective = pyo.Objective(...)`
- Include solver status checks after optimization.
- Add meaningful print statements for solution interpretation.

## Jupyter Notebook Guidelines
- Start each notebook with a clear title and learning objectives.
- Include markdown cells explaining the mathematical formulation.
- Use LaTeX notation for mathematical expressions.
- Add visualizations where appropriate.
- End notebooks with exercises or questions for students.

## Testing Preferences
- Use pytest for the test framework.
- Create tests that validate notebook execution without errors.
- Test that optimization models solve successfully.
- Verify expected solution ranges for deterministic problems.
- Keep `pytest`, `nbconvert`, and `nbformat` in `requirements.in` because the CI workflow uses them directly.

## Documentation Standards
- Use clear, educational language suitable for optimization learners.
- Explain mathematical concepts before implementation.
- Include references to relevant optimization literature.
- Add cross-references between related notebooks.

## Common Patterns
```python
import pyomo.environ as pyo

model = pyo.ConcreteModel()
model.x = pyo.Var(domain=pyo.NonNegativeReals)
model.constraint = pyo.Constraint(expr=model.x <= 10)
model.objective = pyo.Objective(expr=model.x, sense=pyo.maximize)

solver = pyo.SolverFactory("glpk")
result = solver.solve(model)

if result.solver.termination_condition == pyo.TerminationCondition.optimal:
    print(f"Optimal solution: x = {pyo.value(model.x)}")
else:
    print("No optimal solution found")
```

## Avoid These Patterns
- Do not use deprecated Pyomo syntax.
- Avoid hardcoded solver paths.
- Do not include personal file paths in examples.
- Avoid overly complex examples without explanation.
- Do not forget to handle solver failures gracefully.

## File Naming Conventions
- Notebooks: use descriptive names with numbers for ordering, such as `1.1 Basic Model.ipynb`.
- Test files: prefix with `test_`, such as `test_notebook_execution.py`.
- Data files: use lowercase with underscores, such as `transportation_data.xlsx`.

## Dependencies and Environment
- Edit `requirements.in` for direct dependency changes.
- Regenerate `requirements.txt` with:
  ```bash
  uv pip compile requirements.in --universal --python-version 3.11 -o requirements.txt
  ```
- Prefer open-source solvers such as GLPK and CBC for examples.
- Include installation instructions for specialized solvers when needed.
- Test with the Python version specified in the workflows.
