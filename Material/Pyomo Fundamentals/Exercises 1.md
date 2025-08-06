# Knapsack Problem: Exercises 1

## Overview of the Knapsack Problem

The **knapsack problem** is a classic optimization problem that serves as an excellent introduction to mathematical programming and Pyomo. This problem demonstrates fundamental concepts including decision variables, constraints, and objective functions in a practical context.

### Problem Description

Imagine you are a hiker preparing for a trip and need to pack your knapsack (backpack). You have a collection of items you'd like to bring, but your knapsack has limited capacity. Each item has:
- A **weight** (or volume)
- A **value** (utility or importance to you)

**Goal**: Select which items to pack to maximize the total value while staying within the weight capacity of your knapsack.

### Mathematical Formulation

The knapsack problem can be formulated as follows:

**Decision Variables:**
- $x_i \in \{0, 1\}$ for each item $i$, where:
  - $x_i = 1$ if item $i$ is selected (packed)
  - $x_i = 0$ if item $i$ is not selected

**Objective Function:**
$$\max \sum_{i} v_i x_i$$
where $v_i$ is the value of item $i$.

**Constraints:**
$$\sum_{i} w_i x_i \leq W$$
where $w_i$ is the weight of item $i$ and $W$ is the knapsack capacity.

### Problem Characteristics

- **Type**: Integer Programming (specifically, Binary Integer Programming)
- **Complexity**: NP-hard (no known polynomial-time algorithm for large instances)
- **Applications**: Resource allocation, capital budgeting, cargo loading, portfolio selection

### Why Start with the Knapsack Problem?

1. **Intuitive**: Easy to understand conceptually
2. **Fundamental**: Demonstrates core optimization concepts
3. **Practical**: Has many real-world applications
4. **Scalable**: Can be simple or complex depending on the variant

The following exercises will guide you through implementing and solving knapsack problems using Pyomo, starting with basic formulations and progressing to more advanced techniques.