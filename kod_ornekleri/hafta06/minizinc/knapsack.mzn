% 0/1 knapsack: choose a subset of n items maximizing total value
% without exceeding the knapsack's weight capacity.

% BEGIN knapsack_params
int: n;
int: capacity;
array[1..n] of int: weight;
array[1..n] of int: value;
% END knapsack_params

% BEGIN knapsack_vars
array[1..n] of var bool: x;
% END knapsack_vars

% BEGIN knapsack_constraint
constraint sum(i in 1..n)(weight[i] * x[i]) <= capacity;
% END knapsack_constraint

% BEGIN knapsack_solve
solve maximize sum(i in 1..n)(value[i] * x[i]);

output ["selected items: \(x)\n",
        "total value: \(sum(i in 1..n)(value[i] * x[i]))\n"];
% END knapsack_solve
