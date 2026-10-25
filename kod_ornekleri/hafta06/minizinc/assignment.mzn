% Assignment problem: pair each of n workers with exactly one of n tasks,
% one-to-one, minimizing total assignment cost.

include "all_different.mzn";

% BEGIN assignment_params
int: n;
array[1..n, 1..n] of int: cost;
% END assignment_params

% BEGIN assignment_vars
array[1..n] of var 1..n: assign;
% END assignment_vars

% BEGIN assignment_constraint
constraint all_different(assign);
% END assignment_constraint

% BEGIN assignment_solve
var int: total_cost = sum(i in 1..n)(cost[i, assign[i]]);
solve minimize total_cost;

output ["assignment: \(assign)\n",
        "total cost: \(total_cost)\n"];
% END assignment_solve
