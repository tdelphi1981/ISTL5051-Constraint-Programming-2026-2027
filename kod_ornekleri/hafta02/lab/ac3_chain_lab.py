"""Lab starter: reuses modeller/ac3.py's generic `revise`/`ac3` engine on a
new four-variable chain CSP, W<X<Y<Z, all domains {1, 2, 3, 4}. The `arcs`
list below is deliberately incomplete -- only the forward direction of
each constraint is queued, an easy bug to make and to miss (see Unit 2's
note on why neighbours must be re-queued in both directions). Run this
file once exactly as given, then add the three missing reverse arcs where
the TODO says to, and re-run.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "modeller"))

from ac3 import ac3, format_domains  # reused unchanged from Unit 2's engine


def build_chain_csp():
    domains = {
        "W": {1, 2, 3, 4},
        "X": {1, 2, 3, 4},
        "Y": {1, 2, 3, 4},
        "Z": {1, 2, 3, 4},
    }
    constraints = {
        ("W", "X"): lambda w, x: w < x,
        ("X", "W"): lambda x, w: w < x,
        ("X", "Y"): lambda x, y: x < y,
        ("Y", "X"): lambda y, x: x < y,
        ("Y", "Z"): lambda y, z: y < z,
        ("Z", "Y"): lambda z, y: y < z,
    }
    neighbours = {"W": ["X"], "X": ["W", "Y"], "Y": ["X", "Z"], "Z": ["Y"]}

    # BEGIN ac3_lab_arcs
    arcs = [("W", "X"), ("X", "Y"), ("Y", "Z")]
    # TODO: this list only queues the forward direction of each
    # constraint. Add the three missing reverse arcs -- ("X", "W"),
    # ("Y", "X"), ("Z", "Y") -- the same way modeller/ac3.py's
    # build_chain_csp() queues both directions of every constraint.
    # END ac3_lab_arcs

    return domains, arcs, constraints, neighbours


def run() -> dict[str, set[int]]:
    domains, arcs, constraints, neighbours = build_chain_csp()
    print(f"Domains before AC-3: {format_domains(domains)}")
    consistent = ac3(domains, arcs, constraints, neighbours)
    print(f"Arc-consistent: {consistent}")
    print(f"Domains after AC-3: {format_domains(domains)}")
    return domains


if __name__ == "__main__":
    run()
