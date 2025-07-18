# GitHub Copilot Instructions for Pyomo Jupyter Book

## Project Overview
This is a Jupyter Book project that converts Pyomo (Python Optimization Modeling Objects) workshop materials into an interactive web book. The project includes optimization examples, exercises, and tutorials using Pyomo for mathematical optimization.

## Code Style and Standards
- Follow PEP 8 Python style guidelines
- Use meaningful variable names, especially for optimization models (e.g., `model`, `solver`, `constraints`)
- Comment complex optimization formulations and mathematical expressions
- Prefer Pyomo's concrete model approach for examples
- Use proper docstrings for functions and classes

## Project Structure
- `Material/` - Contains all the Jupyter notebooks organized by topic
- `_config.yml` - Jupyter Book configuration
- `_toc.yml` - Table of contents structure  
- `requirements.txt` - Python dependencies
- `tests/` - Test files for validation
- `.github/workflows/` - CI/CD workflows

## Optimization-Specific Guidelines
- Always import Pyomo as `import pyomo.environ as pyo`
- Use descriptive names for optimization components:
  - Models: `model = pyo.ConcreteModel()`
  - Variables: `model.x = pyo.Var(...)`
  - Constraints: `model.constraint_name = pyo.Constraint(...)`
  - Objectives: `model.objective = pyo.Objective(...)`
- Include solver status checks after optimization
- Add meaningful print statements for solution interpretation

## Jupyter Notebook Guidelines
- Start each notebook with a clear title and learning objectives
- Include markdown cells explaining the mathematical formulation
- Use LaTeX notation for mathematical expressions
- Add visualizations where appropriate (matplotlib, plots)
- End notebooks with exercises or questions for students

## Testing Preferences
- Create tests that validate notebook execution without errors
- Test that optimization models solve successfully
- Verify expected solution ranges for deterministic problems
- Use pytest for test framework

## Documentation Standards
- Use clear, educational language suitable for optimization learners
- Explain mathematical concepts before implementation
- Include references to relevant optimization literature
- Add cross-references between related notebooks

## Common Patterns to Suggest
```python
# Standard Pyomo model setup
import pyomo.environ as pyo

model = pyo.ConcreteModel()
model.x = pyo.Var(domain=pyo.NonNegativeReals)
model.constraint = pyo.Constraint(expr=model.x <= 10)
model.objective = pyo.Objective(expr=model.x, sense=pyo.maximize)

# Solve and check status
solver = pyo.SolverFactory('glpk')
result = solver.solve(model)

if result.solver.termination_condition == pyo.TerminationCondition.optimal:
    print(f"Optimal solution: x = {pyo.value(model.x)}")
else:
    print("No optimal solution found")
```

## Avoid These Patterns
- Don't use deprecated Pyomo syntax
- Avoid hardcoded solver paths
- Don't include personal file paths in examples
- Avoid overly complex examples without explanation
- Don't forget to handle solver failures gracefully

## File Naming Conventions
- Notebooks: Use descriptive names with numbers for ordering (e.g., "1.1 Basic Model.ipynb")
- Test files: Prefix with "test_" (e.g., "test_notebook_execution.py")
- Data files: Use lowercase with underscores (e.g., "transportation_data.xlsx")

## Dependencies and Environment
- Stick to the packages in requirements.txt unless absolutely necessary
- Prefer open-source solvers (GLPK, CBC) for examples
- Include installation instructions for specialized solvers when needed
- Test with the specified Python version in the workflows