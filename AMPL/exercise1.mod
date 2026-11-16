# Sets and parameters
param n integer > 0;
set V := 1..n;
param raw_file symbolic default "../data/" & n & "_raw.txt";
param c {V, V} binary;
set E := setof {i in V, j in V: i <> j and c[i,j] = 1 and c[j,i] = 1} (i,j);

# X[i,j] = 1 when donor i gives to patient j.
var X {E} binary;

maximize Matched: sum {(i,j) in E} X[i,j];

subject to DonorLimit {i in V}:
    sum {(i,j) in E} X[i,j] <= 1;

subject to PatientLimit {j in V}:
    sum {(i,j) in E} X[i,j] <= 1;

# One equality per unordered pair enforces both directions of the swap.
subject to Swap {(i,j) in E: i < j}:
    X[i,j] = X[j,i];
