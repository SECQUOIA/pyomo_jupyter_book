# Pyomo Workshop

Welcome to the Pyomo Workshop - your comprehensive guide to optimization modeling in Python!

## What is Pyomo?

Pyomo (Python Optimization Modeling Objects) is a powerful, open-source software package for formulating and solving large-scale optimization problems. Developed at Sandia National Laboratories, Pyomo provides a collection of Python software packages that support a diverse set of optimization capabilities for formulating optimization models {cite}`hart2017pyomo`.

Pyomo enables users to:
- Model optimization problems using algebraic expressions in Python
- Define optimization problems with linear, nonlinear, mixed-integer, and stochastic programming formulations
- Solve problems using commercial and open-source optimization solvers
- Analyze and visualize optimization results

## Installation Instructions

Before diving into Pyomo fundamentals, ensure you have the necessary software installed:

### Python and Pyomo Installation

1. **Install Python** (version 3.8 or higher recommended)
   - Download from [python.org](https://python.org) or use a package manager like conda

2. **Install Pyomo**
   ```bash
   pip install pyomo
   ```

3. **Install additional packages for this workshop**
   ```bash
   pip install matplotlib numpy pandas openpyxl jupyter
   ```

### Solver Installation

Pyomo requires optimization solvers to solve mathematical models. For this workshop:

1. **GLPK (GNU Linear Programming Kit)** - Open-source linear programming solver
   - Windows: Download from [GLPK website](https://www.gnu.org/software/glpk/)
   - macOS: `brew install glpk`
   - Linux: `sudo apt-get install glpk-utils` (Ubuntu/Debian)

2. **CBC (Coin-or Branch and Cut)** - Open-source mixed-integer programming solver
   - Windows: Download from [COIN-OR website](https://www.coin-or.org/download/binary/Cbc/)
   - macOS: `brew install coin-or-tools/coinor/cbc`
   - Linux: `sudo apt-get install coinor-cbc`

3. **IPOPT** - Open-source nonlinear programming solver
   - Can be installed via conda: `conda install -c conda-forge ipopt`

### Verification
Test your installation by running:
```python
import pyomo.environ as pyo
model = pyo.ConcreteModel()
print("Pyomo successfully installed!")
```

## Mathematical Programming Fundamentals

Mathematical programming (optimization) involves finding the best solution to a problem from a set of feasible alternatives. Every optimization problem consists of three essential components:

### 1. Decision Variables

**Variables** represent the unknowns in your optimization problem - the values you want the solver to determine. In Pyomo, variables are defined with domains, bounds, and initial values.

**Example:**
- In a production planning problem: How many units of each product to manufacture?
- In a portfolio optimization: What fraction of budget to invest in each asset?

**Mathematical notation:** Typically denoted as $x_1, x_2, \ldots, x_n$ or vectors $\mathbf{x}$

### 2. Objective Function

The **objective function** quantifies what you want to optimize - either maximize (profit, efficiency) or minimize (cost, time, risk). It expresses the goal of your optimization problem as a mathematical function of the decision variables.

**Mathematical form:** 
- Minimize: $\min f(\mathbf{x})$  
- Maximize: $\max f(\mathbf{x})$

**Examples:**
- Minimize total production cost: $\min \sum_{i} c_i x_i$
- Maximize portfolio return: $\max \sum_{i} r_i x_i$

### 3. Constraints

**Constraints** define the limitations and requirements that any feasible solution must satisfy. They restrict the values that decision variables can take.

**Types of constraints:**
- **Equality constraints:** $g(\mathbf{x}) = 0$ (must be satisfied exactly)
- **Inequality constraints:** $h(\mathbf{x}) \leq 0$ or $h(\mathbf{x}) \geq 0$
- **Bound constraints:** $x_{\text{min}} \leq x \leq x_{\text{max}}$

**Examples:**
- Resource limitations: Total material usage ≤ Available material
- Demand requirements: Production ≥ Minimum demand
- Logical constraints: Binary variables for yes/no decisions

## Types of Optimization Problems

Understanding different problem types helps you choose appropriate solution methods:

1. **Linear Programming (LP):** Linear objective and constraints
2. **Mixed-Integer Programming (MIP):** Includes integer variables
3. **Nonlinear Programming (NLP):** Nonlinear objective or constraints
4. **Mixed-Integer Nonlinear Programming (MINLP):** Combines integer and nonlinear elements

## Why Use Pyomo?

- **Flexibility:** Model complex optimization problems with intuitive Python syntax
- **Solver Integration:** Interface with 20+ commercial and open-source solvers
- **Extensibility:** Build custom solution algorithms and extensions
- **Open Source:** Free to use with active community support
- **Scalability:** Handle problems from small examples to large-scale industrial applications

## Workshop Structure

This workshop is organized into progressive sections that build your Pyomo expertise:

```{tableofcontents}
```

## References

For deeper understanding of optimization modeling and Pyomo:

- {cite}`hart2017pyomo` - Comprehensive Pyomo reference
- {cite}`williams2013model` - Mathematical programming fundamentals  
- {cite}`boyd2004convex` - Convex optimization theory
- {cite}`glpk2012gnu` - GLPK solver documentation
- {cite}`cbc2021coin` - CBC solver documentation
