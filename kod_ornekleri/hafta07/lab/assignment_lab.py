"""Week 7 lab: a small three-worker/three-task assignment problem with a
deliberately incomplete model -- only the "every worker does exactly one
task" constraint family is present. Complete the missing "every task
gets exactly one worker" family where the TODO below says to, then
re-run this script.
"""

import gurobipy as gp
from gurobipy import GRB

WORKERS = ["S1", "S2", "S3"]
TASKS = ["J1", "J2", "J3"]

COST = {
    ("S1", "J1"): 9, ("S1", "J2"): 2, ("S1", "J3"): 7,
    ("S2", "J1"): 6, ("S2", "J2"): 4, ("S2", "J3"): 3,
    ("S3", "J1"): 5, ("S3", "J2"): 8, ("S3", "J3"): 1,
}


def build_model() -> tuple[gp.Model, gp.tupledict]:
    # BEGIN assignment_lab_variables
    model = gp.Model("assignment_lab")
    x = model.addVars(WORKERS, TASKS, vtype=GRB.BINARY, name="x")
    # END assignment_lab_variables

    # BEGIN assignment_lab_constraints
    for worker in WORKERS:
        model.addConstr(gp.quicksum(x[worker, task] for task in TASKS) == 1)
    # TODO: add the missing "every task gets exactly one worker" family
    # here -- one constraint per task in TASKS.
    # END assignment_lab_constraints

    model.setObjective(
        gp.quicksum(
            COST[worker, task] * x[worker, task]
            for worker in WORKERS
            for task in TASKS
        ),
        GRB.MINIMIZE,
    )
    return model, x


def solve() -> float:
    model, x = build_model()
    # BEGIN assignment_lab_solve
    model.optimize()
    for worker in WORKERS:
        for task in TASKS:
            if x[worker, task].X > 0.5:
                print(f"{worker} -> {task}")
    print(f"Total cost: {model.ObjVal}")
    # END assignment_lab_solve
    return model.ObjVal


if __name__ == "__main__":
    solve()
