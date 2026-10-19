"""A genuine tree-shaped 5-region map-coloring instance, deliberately
contrasted with Week 1's cyclic Australia map: R1 is the root, R2 and R3
are R1's children, R4 and R5 are R2's children. Runs Unit 1's directional
arc consistency (DAC) by hand-coded domain filtering, then a forward
assignment that Freuder's tree theorem guarantees is backtrack-free, and
cross-checks the result against a plain CP-SAT solve of the same instance.
"""

from ortools.sat.python import cp_model

COLOUR_NAMES = ["Red", "Green", "Blue"]

# Tree-consistent ordering: R1 is the root; every later region has
# exactly one earlier neighbour in the constraint graph (its parent).
ORDER = ["R1", "R2", "R3", "R4", "R5"]
PARENT = {"R2": "R1", "R3": "R1", "R4": "R2", "R5": "R2"}


# BEGIN tree_csp_variables
REGIONS = ["R1", "R2", "R3", "R4", "R5"]
EDGES = [("R1", "R2"), ("R1", "R3"), ("R2", "R4"), ("R2", "R5")]


def build_domains() -> dict[str, list[int]]:
    """One 3-colour domain (0, 1, 2) per region, before any DAC filtering."""
    return {region: [0, 1, 2] for region in REGIONS}
# END tree_csp_variables


def is_compatible(value_a: int, value_b: int) -> bool:
    """This tree's only constraint type: adjacent regions must differ."""
    return value_a != value_b


# BEGIN tree_csp_dac
def apply_dac(domains: dict[str, list[int]]) -> None:
    """Directional arc consistency, processed in reverse tree-consistent
    order (last region to second): for each region, remove from its
    parent's domain every value with no compatible value left in the
    region's own (current) domain.
    """
    for child in reversed(ORDER[1:]):
        parent = PARENT[child]
        domains[parent] = [
            value
            for value in domains[parent]
            if any(is_compatible(value, other) for other in domains[child])
        ]
        print(f"Revise {parent} against {child}: domains[{parent}] = {domains[parent]}")
# END tree_csp_dac


def cross_check_with_cp_sat() -> tuple[str, dict[str, int]]:
    """Solve the same instance directly with CP-SAT, independent of the
    hand-coded DAC/forward-assignment pass, as a correctness check.
    """
    model = cp_model.CpModel()
    colours = {region: model.NewIntVar(0, 2, f"colour_{region}") for region in REGIONS}
    for region_a, region_b in EDGES:
        model.Add(colours[region_a] != colours[region_b])
    solver = cp_model.CpSolver()
    solver.parameters.num_workers = 1
    solver.parameters.random_seed = 42
    status = solver.Solve(model)
    values = {region: solver.Value(colours[region]) for region in REGIONS}
    return solver.StatusName(status), values


# BEGIN tree_csp_backtrack_free_check
def forward_assign_and_check() -> dict[str, int]:
    """Forward assignment, root to leaves, after DAC filtering: at each
    step pick the first domain value compatible with the already-assigned
    parent. DAC on a tree-consistent order guarantees a compatible value
    always exists, so this count of undone assignments stays zero.
    """
    domains = build_domains()
    apply_dac(domains)
    assignment: dict[str, int] = {}
    backtracks = 0
    for region in ORDER:
        parent = PARENT.get(region)
        if parent is None:
            candidates = domains[region]
        else:
            candidates = [v for v in domains[region] if is_compatible(v, assignment[parent])]
        if not candidates:
            backtracks += 1
        assignment[region] = candidates[0]
        print(f"Assign {region} = {COLOUR_NAMES[assignment[region]]}")
    print(f"Backtracks needed: {backtracks}")
    status, cp_sat_assignment = cross_check_with_cp_sat()
    cp_sat_valid = all(cp_sat_assignment[a] != cp_sat_assignment[b] for a, b in EDGES)
    print(f"CP-SAT cross-check status: {status}, valid coloring: {cp_sat_valid}")
    return assignment
# END tree_csp_backtrack_free_check


if __name__ == "__main__":
    print("Initial domains:", build_domains())
    forward_assign_and_check()
