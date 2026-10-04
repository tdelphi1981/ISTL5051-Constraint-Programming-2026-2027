"""Four small, self-contained propagation demonstrations, one per Unit 3
global constraint besides AllDifferent (already covered by
nqueens_models.py): Element, Table, Circuit, Cumulative. Every instance is
deliberately tiny -- these are propagation demos, not full routing or
scheduling models (those are Weeks 14 and 11).
"""

from ortools.sat.python import cp_model


def _enumerate_values(model: cp_model.CpModel, var: cp_model.IntVar) -> list[int]:
    solver = cp_model.CpSolver()
    solver.parameters.num_workers = 1
    solver.parameters.enumerate_all_solutions = True
    seen: set[int] = set()

    class _Collector(cp_model.CpSolverSolutionCallback):
        def OnSolutionCallback(self) -> None:
            seen.add(self.Value(var))

    solver.Solve(model, _Collector())
    return sorted(seen)


def element_demo() -> None:
    prices = [10, 25, 40, 15]
    # BEGIN element_demo
    model = cp_model.CpModel()
    index = model.NewIntVar(0, len(prices) - 1, "index")
    target = model.NewIntVar(min(prices), max(prices), "target")
    model.AddElement(index, prices, target)
    before = _enumerate_values(model, index)

    model.Add(target >= 20)
    after = _enumerate_values(model, index)

    print(f"Element demo, menu prices={prices}")
    print(f"index domain before target >= 20: {before}")
    print(f"index domain after target >= 20: {after}")
    # END element_demo


def table_demo() -> None:
    colours = ["R", "G", "B"]
    allowed = [(i, j) for i in range(3) for j in range(3) if i != j]
    # BEGIN table_demo
    model = cp_model.CpModel()
    color1 = model.NewIntVar(0, 2, "color1")
    color2 = model.NewIntVar(0, 2, "color2")
    model.AddAllowedAssignments([color1, color2], allowed)
    model.Add(color1 == 0)
    remaining = _enumerate_values(model, color2)

    print(f"Table demo, allowed (color1, color2) pairs: {allowed}")
    print(f"color1 fixed to {colours[0]}; color2 narrows to "
          f"{[colours[v] for v in remaining]}")
    # END table_demo


def _extract_cycle(chosen: set[tuple[int, int]], n: int) -> list[int]:
    node, cycle = 0, [0]
    for _ in range(n - 1):
        node = next(j for (i, j) in chosen if i == node)
        cycle.append(node)
    return cycle


def circuit_demo() -> None:
    n = 4
    # BEGIN circuit_demo
    model = cp_model.CpModel()
    arcs = [
        (i, j, model.NewBoolVar(f"arc_{i}_{j}"))
        for i in range(n)
        for j in range(n)
        if i != j
    ]
    model.AddCircuit(arcs)

    solver = cp_model.CpSolver()
    solver.parameters.num_workers = 1
    solver.parameters.random_seed = 42
    solver.Solve(model)
    chosen = {(i, j) for i, j, lit in arcs if solver.Value(lit)}
    cycle = _extract_cycle(chosen, n)
    print(f"Circuit demo ({n} nodes): visiting order {cycle} -> back to {cycle[0]}")
    # END circuit_demo


def cumulative_demo() -> None:
    durations = [3, 2, 2]
    demands = [2, 3, 2]
    capacity = 4
    horizon = sum(durations)
    # BEGIN cumulative_demo
    model = cp_model.CpModel()
    starts = [model.NewIntVar(0, horizon, f"start_{t}") for t in range(3)]
    intervals = [
        model.NewFixedSizeIntervalVar(starts[t], durations[t], f"task_{t}")
        for t in range(3)
    ]
    model.AddCumulative(intervals, demands, capacity)

    solver = cp_model.CpSolver()
    solver.parameters.num_workers = 1
    solver.parameters.random_seed = 42
    solver.Solve(model)
    result = [solver.Value(s) for s in starts]
    print(f"Cumulative demo, durations={durations}, demands={demands}, "
          f"capacity={capacity}: start times = {result}")
    # END cumulative_demo


if __name__ == "__main__":
    element_demo()
    table_demo()
    circuit_demo()
    cumulative_demo()
