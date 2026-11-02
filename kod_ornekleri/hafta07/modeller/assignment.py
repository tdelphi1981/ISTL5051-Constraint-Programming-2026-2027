"""Unit 3's four-worker / four-task assignment problem: minimize total
cost, with every worker doing exactly one task and every task getting
exactly one worker.
"""

import gurobipy as gp
from gurobipy import GRB

WORKERS = ["W1", "W2", "W3", "W4"]
TASKS = ["Ta", "Tb", "Tc", "Td"]

COST = {
    ("W1", "Ta"): 4, ("W1", "Tb"): 9, ("W1", "Tc"): 9, ("W1", "Td"): 9,
    ("W2", "Ta"): 9, ("W2", "Tb"): 3, ("W2", "Tc"): 9, ("W2", "Td"): 9,
    ("W3", "Ta"): 9, ("W3", "Tb"): 9, ("W3", "Tc"): 2, ("W3", "Td"): 9,
    ("W4", "Ta"): 9, ("W4", "Tb"): 9, ("W4", "Tc"): 9, ("W4", "Td"): 5,
}


def build_model() -> tuple[gp.Model, gp.tupledict]:
    # BEGIN assignment_variables
    model = gp.Model("assignment")
    x = model.addVars(WORKERS, TASKS, vtype=GRB.BINARY, name="x")
    # END assignment_variables

    # BEGIN assignment_constraints
    for worker in WORKERS:
        model.addConstr(gp.quicksum(x[worker, task] for task in TASKS) == 1)
    for task in TASKS:
        model.addConstr(gp.quicksum(x[worker, task] for worker in WORKERS) == 1)
    # END assignment_constraints

    model.setObjective(
        gp.quicksum(
            COST[worker, task] * x[worker, task]
            for worker in WORKERS
            for task in TASKS
        ),
        GRB.MINIMIZE,
    )
    return model, x


def solve() -> tuple[float, dict[str, str]]:
    model, x = build_model()
    # BEGIN assignment_solve
    model.optimize()
    assignment = {}
    for worker in WORKERS:
        for task in TASKS:
            if x[worker, task].X > 0.5:
                assignment[worker] = task
                print(f"{worker} -> {task}")
    print(f"Total cost: {model.ObjVal}")
    # END assignment_solve
    return model.ObjVal, assignment


if __name__ == "__main__":
    solve()
