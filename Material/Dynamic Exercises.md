# Dynamic Optimization Exercises

## Overview of Dynamic Optimization

**Dynamic optimization** deals with optimization problems that evolve over time or space. Unlike static optimization problems where all decisions are made at once, dynamic optimization involves finding optimal strategies or trajectories over a time horizon or spatial domain.

### Key Characteristics

Dynamic optimization problems typically involve:

1. **Time-dependent variables**: Variables that change over time $x(t)$
2. **Differential equations**: Mathematical relationships describing how variables evolve
3. **Boundary conditions**: Initial and/or final conditions that must be satisfied
4. **Integral objectives**: Objectives that accumulate value over time

### Types of Dynamic Optimization

**Optimal Control Problems:**
- Find optimal control inputs $u(t)$ to steer a dynamic system
- Objective: $\min \int_0^T L(x(t), u(t), t) dt + \phi(x(T))$
- Subject to: $\frac{dx}{dt} = f(x(t), u(t), t)$

**Parameter Estimation Problems:**
- Estimate unknown parameters in dynamic models from experimental data
- Match model predictions to observed data
- Critical for model validation and system identification

**Dynamic Programming:**
- Break complex problems into simpler subproblems
- Solve recursively using Bellman's principle of optimality

### Solution Methods

1. **Direct Methods**: Discretize the problem and solve as a large NLP
2. **Indirect Methods**: Derive optimality conditions and solve boundary value problems
3. **Collocation Methods**: Use polynomial approximations on finite elements

### Applications

- Chemical process control and design
- Robotics and trajectory planning  
- Economics and finance (dynamic programming)
- Biomedical engineering (pharmacokinetics)
- Energy systems optimization