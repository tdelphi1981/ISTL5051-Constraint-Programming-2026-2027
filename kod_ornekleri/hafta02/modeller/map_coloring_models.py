"""Australia map-coloring CSP (Russell & Norvig, AIMA), carried over
unchanged from hafta01/modeller/map_coloring.py: one variable per region,
domain = 3 colours, one pairwise "!=" constraint per adjacency edge. Used
this week only as Unit 4's Check Yourself Q4 scenario (why AllDifferent
over *all* regions would be wrong here) — not re-solved with a new model.
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

    solver = cp_model.CpSolver()
    solver.parameters.num_workers = 1
    solver.parameters.random_seed = 42
    status = solver.Solve(model)
    assignment = {region: solver.Value(colours[region]) for region in REGIONS}
    print(f"Status: {solver.StatusName(status)}")
    for region in REGIONS:
        print(f"{region}: {COLOUR_NAMES[assignment[region]]}")
    return assignment


if __name__ == "__main__":
    solve()
