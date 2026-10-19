"""Social golfer problem, a small instance: 3 groups of 3 golfers (9
golfers total) over 4 weeks, so that no two golfers ever share a group
more than once (CSPLib prob010; 4 weeks is this instance's maximum,
since it uses up all C(9, 2) = 36 pairs exactly once). Modeled twice from
the same base variables: once with no symmetry-breaking constraints, once
with lexicographic-ordering symmetry breaking added.
"""

from ortools.sat.python import cp_model

NUM_WEEKS = 4
NUM_GROUPS = 3
GROUP_SIZE = 3
NUM_GOLFERS = NUM_GROUPS * GROUP_SIZE


# BEGIN golfer_variables
def build_variables(model: cp_model.CpModel) -> dict[tuple[int, int, int], cp_model.IntVar]:
    """play[week, golfer, group] is true iff `golfer` is in `group` in
    `week`; every golfer plays exactly one group each week.
    """
    play = {
        (week, golfer, group): model.NewBoolVar(f"play_w{week}_g{golfer}_grp{group}")
        for week in range(NUM_WEEKS)
        for golfer in range(NUM_GOLFERS)
        for group in range(NUM_GROUPS)
    }
    for week in range(NUM_WEEKS):
        for golfer in range(NUM_GOLFERS):
            model.AddExactlyOne(play[week, golfer, group] for group in range(NUM_GROUPS))
    return play
# END golfer_variables


# BEGIN golfer_group_size_constraints
def add_group_size_constraints(model: cp_model.CpModel, play) -> None:
    """Every group has exactly GROUP_SIZE golfers, every week."""
    for week in range(NUM_WEEKS):
        for group in range(NUM_GROUPS):
            model.Add(
                sum(play[week, golfer, group] for golfer in range(NUM_GOLFERS)) == GROUP_SIZE
            )
# END golfer_group_size_constraints


# BEGIN golfer_pairing_constraints
def add_pairing_constraints(model: cp_model.CpModel, play) -> None:
    """Each pair of golfers shares a group in at most one week."""
    for golfer_a in range(NUM_GOLFERS):
        for golfer_b in range(golfer_a + 1, NUM_GOLFERS):
            meets_this_week = []
            for week in range(NUM_WEEKS):
                meet = model.NewBoolVar(f"meet_w{week}_g{golfer_a}_g{golfer_b}")
                for group in range(NUM_GROUPS):
                    model.AddBoolOr(
                        [play[week, golfer_a, group].Not(), play[week, golfer_b, group].Not(), meet]
                    )
                meets_this_week.append(meet)
            model.Add(sum(meets_this_week) <= 1)
# END golfer_pairing_constraints


def _group_of(play, week: int, golfer: int):
    """Linear expression for the group index `golfer` plays in `week`."""
    return sum(group * play[week, golfer, group] for group in range(NUM_GROUPS))


def _add_lex_le(model: cp_model.CpModel, left: list, right: list) -> None:
    """Hand-rolled sequential lex-<=: ortools==9.14.6206's cp_model.CpModel
    has no built-in lexicographic constraint (checked: no `*Lex*` method on
    the class). For every position, `left[i] <= right[i]` is required only
    while every earlier position is already equal, exactly the definition
    of lexicographic order.
    """
    equal_so_far: list[cp_model.IntVar] = []
    for a, b in zip(left, right):
        model.Add(a <= b).OnlyEnforceIf(equal_so_far)
        is_equal = model.NewBoolVar("")
        model.Add(a == b).OnlyEnforceIf(is_equal)
        model.Add(a != b).OnlyEnforceIf(is_equal.Not())
        equal_so_far = equal_so_far + [is_equal]


# BEGIN golfer_symmetry_breaking
def add_symmetry_breaking(model: cp_model.CpModel, play) -> None:
    """Week 1 fixed to a canonical grouping; groups within every other
    week ordered by smallest golfer id; weeks after week 1 lexicographically
    ordered against each other.
    """
    for golfer in range(NUM_GOLFERS):
        model.Add(play[0, golfer, golfer // GROUP_SIZE] == 1)
    for week in range(1, NUM_WEEKS):
        model.Add(play[week, 0, 0] == 1)
    for week in range(1, NUM_WEEKS - 1):
        left = [_group_of(play, week, golfer) for golfer in range(NUM_GOLFERS)]
        right = [_group_of(play, week + 1, golfer) for golfer in range(NUM_GOLFERS)]
        _add_lex_le(model, left, right)
# END golfer_symmetry_breaking


def solve_and_report(with_symmetry_breaking: bool):
    model = cp_model.CpModel()
    play = build_variables(model)
    add_group_size_constraints(model, play)
    add_pairing_constraints(model, play)
    if with_symmetry_breaking:
        add_symmetry_breaking(model, play)

    # BEGIN golfer_solve_and_report
    solver = cp_model.CpSolver()
    solver.parameters.num_workers = 1
    solver.parameters.random_seed = 42
    status = solver.Solve(model)
    print(f"Status: {solver.StatusName(status)}")
    print(f"NumBranches: {solver.NumBranches()}")
    print(f"NumConflicts: {solver.NumConflicts()}")
    print(f"WallTime: {solver.WallTime():.6f}")
    # END golfer_solve_and_report
    schedule = None
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        schedule = [
            [
                next(group for group in range(NUM_GROUPS) if solver.Value(play[week, golfer, group]))
                for golfer in range(NUM_GOLFERS)
            ]
            for week in range(NUM_WEEKS)
        ]
    return status, schedule


if __name__ == "__main__":
    print("Without symmetry breaking:")
    solve_and_report(False)
    print()
    print("With symmetry breaking:")
    solve_and_report(True)
