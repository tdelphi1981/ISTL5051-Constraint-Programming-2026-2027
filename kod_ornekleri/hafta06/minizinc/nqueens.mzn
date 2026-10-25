% N-queens: one queen per row, all_different on columns and both diagonals
% (the same Week 1 CSP formulation, rewritten in MiniZinc).

include "all_different.mzn";

% BEGIN nqueens_decl
int: n;
array[1..n] of var 1..n: q;
% END nqueens_decl

% BEGIN nqueens_constraints
constraint all_different(q);
constraint all_different([q[i] + i | i in 1..n]);
constraint all_different([q[i] - i | i in 1..n]);
% END nqueens_constraints

% BEGIN nqueens_solve
solve satisfy;

output ["queen columns per row: \(q)\n"];
% END nqueens_solve
