"""Unit 1's 0/1 knapsack instance (capacity 6; items A, B, C), solved
twice: once as a binary IP, once as its LP relaxation.
"""

import gurobipy as gp
from gurobipy import GRB

CAPACITY = 6
ITEMS = ["A", "B", "C"]
WEIGHT = {"A": 2, "B": 3, "C": 4}
VALUE = {"A": 3, "B": 4, "C": 5}


def add_capacity_constraint(model: gp.Model, x: dict[str, gp.Var]) -> None:
    # BEGIN knapsack_constraint
    model.addConstr(
        gp.quicksum(WEIGHT[item] * x[item] for item in ITEMS) <= CAPACITY,
        name="capacity",
    )
    # END knapsack_constraint


def build_ip_model() -> tuple[gp.Model, dict[str, gp.Var]]:
    # BEGIN knapsack_ip_variables
    model = gp.Model("knapsack_ip")
    x = {item: model.addVar(vtype=GRB.BINARY, name=item) for item in ITEMS}
    # END knapsack_ip_variables
    add_capacity_constraint(model, x)
    model.setObjective(
        gp.quicksum(VALUE[item] * x[item] for item in ITEMS), GRB.MAXIMIZE
    )
    return model, x


def solve_ip() -> float:
    model, x = build_ip_model()
    # BEGIN knapsack_ip_solve
    model.optimize()
    status = "OPTIMAL" if model.Status == GRB.OPTIMAL else str(model.Status)
    print(f"Status: {status}")
    print(f"Optimal value: {model.ObjVal}")
    for item in ITEMS:
        print(f"  {item}: {x[item].X}")
    # END knapsack_ip_solve
    return model.ObjVal


def solve_lp_relaxation() -> float:
    # BEGIN knapsack_lp_relaxation
    model = gp.Model("knapsack_lp_relaxation")
    x = {
        item: model.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=1, name=item)
        for item in ITEMS
    }
    add_capacity_constraint(model, x)
    model.setObjective(
        gp.quicksum(VALUE[item] * x[item] for item in ITEMS), GRB.MAXIMIZE
    )
    model.optimize()
    print(f"Relaxed optimal value: {model.ObjVal}")
    for item in ITEMS:
        print(f"  {item}: {x[item].X}")
    # END knapsack_lp_relaxation
    return model.ObjVal


if __name__ == "__main__":
    solve_ip()
    solve_lp_relaxation()
