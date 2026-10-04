"""Pure-Python (no CP-SAT) implementation of AC-3, run on Unit 2's worked
chain CSP X<Y<Z, all three domains {1, 2, 3}, so the by-hand trace is
independently checkable against real code output.
"""

from collections import deque


def revise(domains: dict[str, set[int]], xi: str, xj: str, constraint) -> bool:
    # BEGIN ac3_revise
    changed = False
    for value_i in set(domains[xi]):
        if not any(constraint(value_i, value_j) for value_j in domains[xj]):
            domains[xi].remove(value_i)
            changed = True
    return changed
    # END ac3_revise


def ac3(
    domains: dict[str, set[int]],
    arcs: list[tuple[str, str]],
    constraints: dict[tuple[str, str], object],
    neighbours: dict[str, list[str]],
) -> bool:
    # BEGIN ac3_algorithm
    worklist = deque(arcs)
    while worklist:
        xi, xj = worklist.popleft()
        if revise(domains, xi, xj, constraints[(xi, xj)]):
            if not domains[xi]:
                return False
            for xk in neighbours[xi]:
                if xk != xj:
                    worklist.append((xk, xi))
    return True
    # END ac3_algorithm


def build_chain_csp() -> tuple[
    dict[str, set[int]],
    list[tuple[str, str]],
    dict[tuple[str, str], object],
    dict[str, list[str]],
]:
    # BEGIN ac3_toy_csp
    domains = {"X": {1, 2, 3}, "Y": {1, 2, 3}, "Z": {1, 2, 3}}
    arcs = [("X", "Y"), ("Y", "X"), ("Y", "Z"), ("Z", "Y")]
    constraints = {
        ("X", "Y"): lambda x, y: x < y,
        ("Y", "X"): lambda y, x: x < y,
        ("Y", "Z"): lambda y, z: y < z,
        ("Z", "Y"): lambda z, y: y < z,
    }
    neighbours = {"X": ["Y"], "Y": ["X", "Z"], "Z": ["Y"]}
    return domains, arcs, constraints, neighbours
    # END ac3_toy_csp


def format_domains(domains: dict[str, set[int]]) -> str:
    return ", ".join(f"{name}={sorted(values)}" for name, values in domains.items())


def run() -> dict[str, set[int]]:
    domains, arcs, constraints, neighbours = build_chain_csp()

    # BEGIN ac3_run
    print(f"Domains before AC-3: {format_domains(domains)}")
    consistent = ac3(domains, arcs, constraints, neighbours)
    print(f"Arc-consistent: {consistent}")
    print(f"Domains after AC-3 (fixpoint): {format_domains(domains)}")
    # END ac3_run
    return domains


if __name__ == "__main__":
    run()
