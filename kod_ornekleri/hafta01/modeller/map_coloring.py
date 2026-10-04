"""Australia map-coloring CSP (Russell & Norvig, AIMA): one variable per
region, domain = 3 colours, one pairwise "!=" constraint per adjacency
edge. Tasmania (T) borders no other region and still needs a domain
value, a deliberate edge case for a variable with zero constraints.
"""

from ortools.sat.python import cp_model

REGIONS = ["WA", "NT", "SA", "Q", "NSW", "V", "T"]
EDGES = [
    ("WA", "NT"),
    ("WA", "SA"),
    ("NT", "SA"),
    ("NT", "Q"),
    ("SA", "Q"),
    ("SA", "NSW"),
    ("SA", "V"),
    ("Q", "NSW"),
    ("NSW", "V"),
]
COLOUR_NAMES = ["Red", "Green", "Blue"]


def build_variables(model: cp_model.CpModel) -> dict[str, cp_model.IntVar]:
    # BEGIN mapcolor_variables
    colours = {
        region: model.NewIntVar(0, 2, f"colour_{region}") for region in REGIONS
    }
    return colours
    # END mapcolor_variables


def add_constraints(model: cp_model.CpModel, colours: dict[str, cp_model.IntVar]) -> None:
    # BEGIN mapcolor_constraints
    for region_a, region_b in EDGES:
        model.Add(colours[region_a] != colours[region_b])
    # END mapcolor_constraints


def solve() -> dict[str, int]:
    model = cp_model.CpModel()
    colours = build_variables(model)
    add_constraints(model, colours)

    # BEGIN mapcolor_solve
    solver = cp_model.CpSolver()
    solver.parameters.num_workers = 1
    solver.parameters.random_seed = 42
    status = solver.Solve(model)
    assignment = {region: solver.Value(colours[region]) for region in REGIONS}
    print(f"Status: {solver.StatusName(status)}")
    for region in REGIONS:
        print(f"{region}: {COLOUR_NAMES[assignment[region]]}")
    # END mapcolor_solve
    return assignment


if __name__ == "__main__":
    solve()
