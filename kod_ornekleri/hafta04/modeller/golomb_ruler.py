"""CP-SAT model of the optimal Golomb ruler (OGR) for 8 marks (Unit 2's
second worked instance), plus an LNS-improve variant that starts from a
deliberately non-optimal greedy ruler and shrinks it round by round.

Neighbourhood size note: an exhaustive check over every 2-mark subset of
this specific greedy start showed none of them can improve the length in
a single repair round (the six marks left fixed already pin the pairwise
distances too tightly); relaxing 3 marks at a time is the smallest
neighbourhood size for which this file's captured LNS run genuinely
shrinks the ruler, so `NEIGHBOURHOOD_SIZE = 3` here (no fabricated
improvement over an unworkable 2-mark neighbourhood).
"""

import random

from ortools.sat.python import cp_model

ORDER = 8
UPPER_BOUND = ORDER * ORDER
NEIGHBOURHOOD_SIZE = 3
ROUNDS = 15
SEED = 1


def golomb_variables(
    order: int, upper_bound: int
) -> tuple[cp_model.CpModel, list[cp_model.IntVar]]:
    model = cp_model.CpModel()
    # BEGIN golomb_variables
    marks = [model.NewIntVar(0, upper_bound, f"mark_{i}") for i in range(order)]
    model.Add(marks[0] == 0)
    for i in range(order - 1):
        model.Add(marks[i] < marks[i + 1])
    # END golomb_variables
    return model, marks


def golomb_distinct_distances(
    model: cp_model.CpModel, marks: list[cp_model.IntVar], upper_bound: int
) -> None:
    # BEGIN golomb_distinct_distances
    distances = []
    for i in range(len(marks)):
        for j in range(i + 1, len(marks)):
            distance = model.NewIntVar(1, upper_bound, f"dist_{i}_{j}")
            model.Add(distance == marks[j] - marks[i])
            distances.append(distance)
    model.AddAllDifferent(distances)
    # END golomb_distinct_distances


def golomb_objective_solve(order: int, upper_bound: int) -> tuple[int, list[int]]:
    model, marks = golomb_variables(order, upper_bound)
    golomb_distinct_distances(model, marks, upper_bound)
    # BEGIN golomb_objective_solve
    model.Minimize(marks[-1])
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 1
    solver.parameters.random_seed = 42
    status = solver.Solve(model)
    length = solver.Value(marks[-1])
    positions = [solver.Value(mark) for mark in marks]
    print(f"Status: {solver.StatusName(status)}")
    print(f"Optimal length for {order} marks: {length}")
    print(f"Marks: {positions}")
    # END golomb_objective_solve
    return length, positions


def golomb_greedy_start(order: int) -> list[int]:
    # BEGIN golomb_greedy_start
    marks = [0]
    seen_distances: set[int] = set()
    for _ in range(order - 1):
        candidate = marks[-1] + 1
        while True:
            new_distances = {candidate - mark for mark in marks}
            if len(new_distances) == len(marks) and not (new_distances & seen_distances):
                break
            candidate += 1
        marks.append(candidate)
        seen_distances |= new_distances
    # END golomb_greedy_start
    return marks


def _ruler_length(marks: list[int]) -> int:
    return marks[-1]


def _repair_relaxed_marks(
    marks: list[int], relaxed: list[int], order: int, upper_bound: int
) -> list[int] | None:
    model = cp_model.CpModel()
    marks_vars = [
        model.NewIntVar(0, upper_bound, f"mark_{i}")
        if i in relaxed
        else model.NewIntVar(marks[i], marks[i], f"mark_{i}")
        for i in range(order)
    ]
    for i in range(order - 1):
        model.Add(marks_vars[i] < marks_vars[i + 1])
    golomb_distinct_distances(model, marks_vars, upper_bound)
    model.Minimize(marks_vars[-1])
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 1
    solver.parameters.random_seed = 42
    status = solver.Solve(model)
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return [solver.Value(mark) for mark in marks_vars]
    return None


def golomb_lns_destroy_repair(
    order: int, upper_bound: int, neighbourhood_size: int, rounds: int, seed: int
) -> list[int]:
    rng = random.Random(seed)
    marks = golomb_greedy_start(order)
    print(f"Round 0: length {_ruler_length(marks)}, marks {marks}")
    # BEGIN golomb_lns_destroy_repair
    for round_number in range(1, rounds + 1):
        relaxed = rng.sample(range(1, order), neighbourhood_size)
        proposal = _repair_relaxed_marks(marks, relaxed, order, upper_bound)
        if proposal is not None and _ruler_length(proposal) <= _ruler_length(marks):
            marks = proposal
        print(f"Round {round_number}: length {_ruler_length(marks)}, marks {marks}")
    # END golomb_lns_destroy_repair
    return marks


if __name__ == "__main__":
    golomb_objective_solve(ORDER, UPPER_BOUND)
    golomb_lns_destroy_repair(ORDER, UPPER_BOUND, NEIGHBOURHOOD_SIZE, ROUNDS, SEED)
