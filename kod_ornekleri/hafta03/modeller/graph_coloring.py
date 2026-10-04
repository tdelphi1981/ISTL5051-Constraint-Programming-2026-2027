"""Petersen graph 3-colouring CSP: 10 nodes, 15 edges (outer 5-cycle,
inner pentagram, five spokes), one variable per node, domain = 3 colours,
one pairwise "!=" constraint per edge. Larger and structurally harder than
Week 1's 7-node Australia map-coloring toy, deliberately chosen so that
ordering and worker choices make a visible difference in search effort.
"""

from ortools.sat.python import cp_model

from search_stats import print_search_stats

NUM_NODES = 10
OUTER_CYCLE = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)]
INNER_PENTAGRAM = [(5, 7), (7, 9), (9, 6), (6, 8), (8, 5)]
SPOKES = [(i, i + 5) for i in range(5)]
EDGES = OUTER_CYCLE + INNER_PENTAGRAM + SPOKES


def build_variables(model: cp_model.CpModel) -> list[cp_model.IntVar]:
    # BEGIN petersen_variables
    colours = [model.NewIntVar(0, 2, f"colour_{node}") for node in range(NUM_NODES)]
    return colours
    # END petersen_variables


def add_constraints(model: cp_model.CpModel, colours: list[cp_model.IntVar]) -> None:
    # BEGIN petersen_constraints
    for node_a, node_b in EDGES:
        model.Add(colours[node_a] != colours[node_b])
    # END petersen_constraints


def petersen_solve_default() -> list[int]:
    model = cp_model.CpModel()
    colours = build_variables(model)
    add_constraints(model, colours)

    # BEGIN petersen_solve_default
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 1
    solver.parameters.random_seed = 42
    status = solver.Solve(model)
    print_search_stats(solver, status)
    # END petersen_solve_default
    return [solver.Value(colour) for colour in colours]


def petersen_solve_ordered() -> list[int]:
    model = cp_model.CpModel()
    colours = build_variables(model)
    add_constraints(model, colours)

    # BEGIN petersen_solve_ordered
    model.AddDecisionStrategy(
        colours, cp_model.CHOOSE_MIN_DOMAIN_SIZE, cp_model.SELECT_MIN_VALUE
    )
    solver = cp_model.CpSolver()
    solver.parameters.search_branching = cp_model.FIXED_SEARCH
    solver.parameters.num_search_workers = 1
    solver.parameters.random_seed = 42
    status = solver.Solve(model)
    print_search_stats(solver, status)
    # END petersen_solve_ordered
    return [solver.Value(colour) for colour in colours]


def petersen_solve_workers(num_workers: int) -> list[int]:
    model = cp_model.CpModel()
    colours = build_variables(model)
    add_constraints(model, colours)

    # BEGIN petersen_solve_workers
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = num_workers
    solver.parameters.random_seed = 42
    status = solver.Solve(model)
    print_search_stats(solver, status)
    # END petersen_solve_workers
    return [solver.Value(colour) for colour in colours]


if __name__ == "__main__":
    petersen_solve_default()
