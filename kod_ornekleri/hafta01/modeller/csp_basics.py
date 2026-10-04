"""A tiny 3-region "triangle" toy CSP: three mutually adjacent regions,
three available colours. Built and solved step by step to make the
variables/domains/constraints/solution vocabulary concrete before any
classic combinatorial problem appears.
"""

from ortools.sat.python import cp_model


def build_variables(model: cp_model.CpModel) -> list[cp_model.IntVar]:
    # BEGIN toy_csp_variables
    region_a = model.NewIntVar(0, 2, "region_a")
    region_b = model.NewIntVar(0, 2, "region_b")
    region_c = model.NewIntVar(0, 2, "region_c")
    return [region_a, region_b, region_c]
    # END toy_csp_variables


def add_constraints(model: cp_model.CpModel, regions: list[cp_model.IntVar]) -> None:
    region_a, region_b, region_c = regions
    # BEGIN toy_csp_constraints
    model.Add(region_a != region_b)
    model.Add(region_b != region_c)
    model.Add(region_a != region_c)
    # END toy_csp_constraints


def solve() -> tuple[int, list[int]]:
    model = cp_model.CpModel()
    regions = build_variables(model)
    add_constraints(model, regions)

    # BEGIN toy_csp_solve
    solver = cp_model.CpSolver()
    solver.parameters.num_workers = 1
    solver.parameters.random_seed = 42
    status = solver.Solve(model)
    values = [solver.Value(region) for region in regions]
    print(f"Status: {solver.StatusName(status)}")
    print(f"Assignment: region_a={values[0]}, region_b={values[1]}, region_c={values[2]}")
    # END toy_csp_solve
    return status, values


if __name__ == "__main__":
    solve()
