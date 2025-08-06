# Generalized Disjunctive Programming (GDP) Exercises

## Overview of Generalized Disjunctive Programming

**Generalized Disjunctive Programming (GDP)** is a modeling framework that extends traditional mixed-integer programming to handle logical relationships and discrete choices more naturally. GDP provides an intuitive way to model complex decision-making problems involving both continuous and discrete variables.

### What is GDP?

GDP stands for **Generalized Disjunctive Programming**, a mathematical programming paradigm that:

- **Combines continuous and discrete decisions** in a unified framework
- **Uses logical propositions** to represent discrete choices
- **Employs disjunctions** to model alternative scenarios or operating modes
- **Provides natural problem formulation** for complex systems with operational choices

### Key Components of GDP

**1. Disjunctions**: Logical OR relationships representing mutually exclusive alternatives
$$\begin{bmatrix}
Y_1 \\
g_1(x) \leq 0 \\
\Omega_1(x) = 0
\end{bmatrix} \vee \begin{bmatrix}
Y_2 \\
g_2(x) \leq 0 \\
\Omega_2(x) = 0
\end{bmatrix} \vee \ldots \vee \begin{bmatrix}
Y_K \\
g_K(x) \leq 0 \\
\Omega_K(x) = 0
\end{bmatrix}$$

**2. Boolean Variables**: $Y_k \in \{True, False\}$ indicate which disjunctive term is active

**3. Logic Constraints**: Additional logical relationships between Boolean variables

### GDP vs. Traditional MIP

| Aspect | GDP | Traditional MIP |
|--------|-----|----------------|
| **Modeling** | Intuitive logical structure | Requires manual big-M formulations |
| **Readability** | Clear representation of choices | Obscured by binary variable tricks |
| **Flexibility** | Easy to modify logical structure | Difficult to change formulations |
| **Solution** | Automatic reformulation to MIP | Direct MIP solving |

### Solution Methods

GDP problems are typically solved by:

1. **Big-M Reformulation**: Convert disjunctions to inequalities with large constants
2. **Hull Reformulation**: Use convex hull representation for tighter relaxations
3. **Hybrid Methods**: Combine different reformulation techniques

### Applications

- **Process Design**: Equipment selection and sizing
- **Scheduling**: Resource allocation with setup decisions  
- **Supply Chain**: Facility location and capacity decisions
- **Engineering Design**: Configuration and topology optimization
- **Logic-based Planning**: Manufacturing and operations research

### Why Use GDP?

- **Natural Modeling**: Express decisions as they occur in real problems
- **Automatic Reformulation**: Pyomo.GDP handles conversion to solvable forms
- **Enhanced Readability**: Models are easier to understand and maintain
- **Flexible Solving**: Multiple solution strategies available
