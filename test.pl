/*
bob_list(0, []) :- !.
bob_list(N, [_Hey|T]) :- R is N-1, bob_list(R, T).

bob_matrix(N, X) :- bob_aux(N, N, X).

bob_aux(_, 0, []) :- !.
bob_aux(S, N, [X|T]) :- R is N-1, bob_list(S, X), bob_aux(S, R, T).

find_bob([[_,bob,_]|_]).
find_bob([_|T]) :- find_bob(T).

run_bob(N, X) :- bob_matrix(N, X), find_bob(X).
*/

list(0, []) :- !.
list(N, [o|T]) :- R is N-1, list(R, T).

matrix(N, X) :- aux(N, N, X).

aux(_, 0, []) :- !.
aux(S, N, [X|T]) :- R is N-1, list(S, X), aux(S, R, T).

putqueen(_, _, []) :- !.
putqueen(S, N, [H|_]) :- free(S, N, H).
putqueen(S, N, [_|T]) :- R is N-1, putqueen(S, R, T).
