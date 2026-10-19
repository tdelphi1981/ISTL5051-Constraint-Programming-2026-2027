"""Balanced incomplete block design (BIBD), the Fano plane: the smallest
classic instance from CSPLib prob028, (v, b, r, k, lambda) = (7, 7, 3, 3,
1). A 7x7 Boolean incidence matrix x[point, block]; every row (point)
sums to r, every column (block) sums to k, and every pair of rows shares
exactly lambda columns. Modeled twice: once with no symmetry-breaking
constraints, once with a lexicographic-ordering constraint between
adjacent block-columns.
"""

from ortools.sat.python import cp_model

NUM_POINTS = 7
NUM_BLOCKS = 7
BLOCKS_PER_POINT = 3   # r
POINTS_PER_BLOCK = 3   # k
PAIR_COUNT = 1         # lambda


# BEGIN bibd_variables
def build_variables(model: cp_model.CpModel) -> dict[tuple[int, int], cp_model.IntVar]:
    """x[point, block] is true iff `point` belongs to `block`; every row
    sums to BLOCKS_PER_POINT, every column sums to POINTS_PER_BLOCK.
    """
    x = {
        (point, block): model.NewBoolVar(f"x_{point}_{block}")
        for point in range(NUM_POINTS)
        for block in range(NUM_BLOCKS)
    }
    for point in range(NUM_POINTS):
        model.Add(sum(x[point, block] for block in range(NUM_BLOCKS)) == BLOCKS_PER_POINT)
    for block in range(NUM_BLOCKS):
        model.Add(sum(x[point, block] for point in range(NUM_POINTS)) == POINTS_PER_BLOCK)
    return x
# END bibd_variables


# BEGIN bibd_pairwise_lambda_constraints
def add_pairwise_lambda_constraints(model: cp_model.CpModel, x) -> None:
    """Every pair of points shares exactly PAIR_COUNT blocks; each shared
    block is linearized as the Boolean product of the pair's two entries.
    """
    for point_a in range(NUM_POINTS):
        for point_b in range(point_a + 1, NUM_POINTS):
            shared_blocks = []
            for block in range(NUM_BLOCKS):
                both = model.NewBoolVar(f"both_{point_a}_{point_b}_{block}")
                model.AddMultiplicationEquality(both, [x[point_a, block], x[point_b, block]])
                shared_blocks.append(both)
            model.Add(sum(shared_blocks) == PAIR_COUNT)
# END bibd_pairwise_lambda_constraints


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


# BEGIN bibd_symmetry_breaking
def add_symmetry_breaking(model: cp_model.CpModel, x) -> None:
    """Adjacent block-columns forced into non-decreasing lexicographic
    order, one column-relabeling symmetry-breaking constraint per pair.
    """
    for block in range(NUM_BLOCKS - 1):
        left = [x[point, block] for point in range(NUM_POINTS)]
        right = [x[point, block + 1] for point in range(NUM_POINTS)]
        _add_lex_le(model, left, right)
# END bibd_symmetry_breaking


def solve_and_report(with_symmetry_breaking: bool):
    model = cp_model.CpModel()
    x = build_variables(model)
    add_pairwise_lambda_constraints(model, x)
    if with_symmetry_breaking:
        add_symmetry_breaking(model, x)

    # BEGIN bibd_solve_and_report
    solver = cp_model.CpSolver()
    solver.parameters.num_workers = 1
    solver.parameters.random_seed = 42
    status = solver.Solve(model)
    print(f"Status: {solver.StatusName(status)}")
    print(f"NumBranches: {solver.NumBranches()}")
    print(f"NumConflicts: {solver.NumConflicts()}")
    print(f"WallTime: {solver.WallTime():.6f}")
    # END bibd_solve_and_report
    design = None
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        design = [[solver.Value(x[point, block]) for block in range(NUM_BLOCKS)] for point in range(NUM_POINTS)]
    return status, design


if __name__ == "__main__":
    print("Without symmetry breaking:")
    solve_and_report(False)
    print()
    print("With symmetry breaking:")
    solve_and_report(True)
