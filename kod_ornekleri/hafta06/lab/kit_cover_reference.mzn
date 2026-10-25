% Reference solution for the Week 6 lab sheet's capstone step (H5).
% NOT distributed to students as a starter file --- the lab sheet asks
% students to build this model entirely from scratch. Kept here only so
% every \beklenen{}/ciktikutusu box in the lab sheet quotes a real,
% captured run.
%
% Lab kit coverage (a small set-cover instance): four lab stations need
% at least one compatible measurement kit; five candidate kits each cover
% a subset of stations at a fixed cost. Choose the cheapest subset of
% kits that covers every station at least once.

int: n_stations;
int: n_kits;
array[1..n_kits, 1..n_stations] of bool: covers;
array[1..n_kits] of int: cost;

array[1..n_kits] of var bool: choose;

constraint forall(s in 1..n_stations)(
  sum(k in 1..n_kits)(bool2int(covers[k,s]) * bool2int(choose[k])) >= 1
);

solve minimize sum(k in 1..n_kits)(cost[k] * bool2int(choose[k]));

output ["chosen kits: \(choose)\n",
        "total cost: \(sum(k in 1..n_kits)(cost[k] * bool2int(choose[k])))\n"];
