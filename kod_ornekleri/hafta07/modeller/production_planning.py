"""A small factory with three products, each with a per-unit profit and
per-unit consumption of two shared resources (labour hours, machine
hours), each resource with a fixed budget; maximize total profit with
integer production quantities.
"""

import gurobipy as gp
from gurobipy import GRB

PRODUCTS = ["P1", "P2", "P3"]
PROFIT = {"P1": 40, "P2": 30, "P3": 20}
LABOUR_USE = {"P1": 2, "P2": 4, "P3": 3}
MACHINE_USE = {"P1": 3, "P2": 2, "P3": 1}
LABOUR_BUDGET = 60
MACHINE_BUDGET = 40


def build_model() -> tuple[gp.Model, dict[str, gp.Var]]:
    # BEGIN production_variables
    model = gp.Model("production_planning")
    x = {
        product: model.addVar(vtype=GRB.INTEGER, lb=0, name=product)
        for product in PRODUCTS
    }
    # END production_variables

    # BEGIN production_constraints
    model.addConstr(
        gp.quicksum(LABOUR_USE[p] * x[p] for p in PRODUCTS) <= LABOUR_BUDGET,
        name="labour",
    )
    model.addConstr(
        gp.quicksum(MACHINE_USE[p] * x[p] for p in PRODUCTS) <= MACHINE_BUDGET,
        name="machine",
    )
    # END production_constraints

    model.setObjective(
        gp.quicksum(PROFIT[p] * x[p] for p in PRODUCTS), GRB.MAXIMIZE
    )
    return model, x


def solve() -> tuple[float, dict[str, float]]:
    model, x = build_model()
    # BEGIN production_solve
    model.optimize()
    plan = {product: x[product].X for product in PRODUCTS}
    for product in PRODUCTS:
        print(f"{product}: {plan[product]}")
    print(f"Total profit: {model.ObjVal}")
    # END production_solve
    return model.ObjVal, plan


if __name__ == "__main__":
    solve()
