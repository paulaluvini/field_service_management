# Optimization Problem

Final assignment for the Optimization subject of the MSc in Data Science from Universidad de San Andrés.

## Problem
In this project, we focus on the weekly planning of work crews for different assigned tasks. We have a list of workers and a list of jobs to complete. The objective is to maximize total profit by considering the benefit of completing a job while accounting for worker compensation.

Formally, the problem is defined as follows. We have **T** workers available for the tasks. Additionally, we have a list of **O** work orders to complete. Each order requires a predefined number of workers, **To**. The planning period consists of **6 days** (Monday to Saturday), with each day divided into **5 shifts of 2 hours**. Each work order can be completed within a single shift, and multiple orders cannot be scheduled in the same shift if they share workers. The solution must assign workers to work orders and schedule them in shifts while meeting the following constraints:

- Not all work orders need to be completed.
- No worker can be scheduled for all **6 days** of the planning period.
- No worker can be assigned to all **5 shifts** in a single day.
- Some work orders are geographically distant, meaning they cannot be assigned to consecutive shifts for the same worker.
- A work order must have all **To** required workers assigned to the same shift to be completed.
- Some orders are correlated: If order **A** is completed, then order **B** must also be completed in the consecutive shift of the same day.
- Workers are compensated based on the number of orders assigned. The difference between the worker with the highest number of assigned orders and the worker with the least (including those with no assignments) cannot exceed **10**.

If these constraints are met, the assignment is feasible. Additionally, there are two desirable (but not mandatory) constraints:

- Some workers prefer not to be assigned to the same work order due to conflicts.
- Some work orders are repetitive, so it is preferable that the same worker is not assigned to both.

Once the necessary constraints are met, the objective is to maximize the **profit of the assignment**, defined as the sum of the benefits of completed work orders minus worker compensation. Worker compensation follows this scheme:

- **0 to 5 orders**: $1000 per order
- **6 to 10 orders**: $1200 per order
- **11 to 15 orders**: $1400 per order
- **More than 15 orders**: $1500 per order

## Context

A preliminary implementation of the problem is available, including data input from an instance. The data includes the number of workers, work orders with their respective benefits and required workforce, correlated work orders, conflicting orders, repetitive orders, and worker conflicts. After reading the data, it is stored in an instance of the `FieldWorkAssignment` class, which contains:

- **Number of workers**: Integer representing available workers.
- **Work orders**: List of all weekly work orders.
- **Worker conflicts**: List of worker pairs with conflicts.
- **Correlated work orders**: List of ordered pairs of correlated work orders.
- **Conflicting work orders**: List of conflicting work orders.
- **Repetitive work orders**: List of repetitive work orders.

Each work order contains the following fields:

- **ID**: Unique integer identifier.
- **Benefit**: Integer representing the value of completing the order.
- **Required workers**: Number of workers needed for completion.

## Task Description

The task involves modeling and solving the optimization problem, implementing provided code to handle different instances, and delivering a report covering the following aspects:

1. **Modeling**: Formulating a model that meets all constraints and incorporates the objective function.
2. **Desirable Constraints**: Reformulating the model to include these constraints as additional constraints or objective function terms.
3. **Implementation**: Developing and implementing proposed alternatives using CPLEX.
4. **Experimentation**: Conducting experiments with different alternatives to analyze results both quantitatively and qualitatively.

## Solution Approach

Initially, we have information about workers, work orders, required workforce, order benefits, worker conflicts, correlated orders, conflicting orders, and repetitive orders.

- To complete an order, it must have the required number of assigned workers:

```math
assigned\_workers(order) \geq required\_workers(order)
```

Since workers generate a cost, we enforce equality:

```math
assigned\_workers(order) - required\_workers(order) = 0
```
