"""Enumerates every feasible assignment of the five-talk instance (Week 1
Unit 4's enumerate-all-solutions technique, reused), records each one's
(total violations, afternoon count) pair, and filters the Pareto-optimal
subset under the two objectives Unit 3 introduces.
"""

from ortools.sat.python import cp_model

from overconstrained_timetable import PAIRS, TALKS, build_variables


class _CandidateCollector(cp_model.CpSolverSolutionCallback):
    # BEGIN pareto_enumerate_candidates
    def __init__(self, slots: dict[str, cp_model.IntVar]) -> None:
        super().__init__()
        self._slots = slots
        self.candidates: list[tuple[int, int]] = []

    def OnSolutionCallback(self) -> None:
        assignment = {talk: self.Value(self._slots[talk]) for talk in TALKS}
        violations = sum(1 for a, b in PAIRS if assignment[a] == assignment[b])
        afternoon = sum(assignment.values())
        self.candidates.append((violations, afternoon))
    # END pareto_enumerate_candidates


def enumerate_candidates() -> list[tuple[int, int]]:
    model = cp_model.CpModel()
    slots = build_variables(model)
    collector = _CandidateCollector(slots)
    solver = cp_model.CpSolver()
    solver.parameters.enumerate_all_solutions = True
    solver.parameters.num_workers = 1
    solver.Solve(model, collector)
    return collector.candidates


def dominates(candidate_a: tuple[int, int], candidate_b: tuple[int, int]) -> bool:
    # BEGIN pareto_dominance_check
    at_least_as_good = candidate_a[0] <= candidate_b[0] and candidate_a[1] <= candidate_b[1]
    strictly_better = candidate_a[0] < candidate_b[0] or candidate_a[1] < candidate_b[1]
    return at_least_as_good and strictly_better
    # END pareto_dominance_check


def pareto_filter_front(candidates: list[tuple[int, int]]) -> list[tuple[int, int]]:
    # BEGIN pareto_filter_front
    unique_candidates = sorted(set(candidates))
    front = [
        candidate
        for candidate in unique_candidates
        if not any(
            dominates(other, candidate) for other in unique_candidates if other != candidate
        )
    ]
    return front
    # END pareto_filter_front


def pareto_print() -> None:
    candidates = enumerate_candidates()
    front = pareto_filter_front(candidates)

    # BEGIN pareto_print
    print("All candidates (violations, afternoon_count):")
    for candidate in sorted(set(candidates)):
        marker = " <- Pareto front" if candidate in front else ""
        print(f"  {candidate}{marker}")
    print("Pareto front:")
    for candidate in front:
        print(f"  {candidate}")
    # END pareto_print


if __name__ == "__main__":
    pareto_print()
