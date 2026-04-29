% Facts
parent(homer, bart).
parent(homer, lisa).
parent(homer, maggie).
parent(marge, bart).
parent(marge, lisa).
parent(marge, maggie).

parent(abraham, homer).
parent(mona, homer).

parent(clancy, marge).
parent(jacqueline, marge).

sibling(X, Y) :-
    parent(Z, X), 
    parent(Z, Y), 
    X \= Y.

male(homer).
male(bart).
male(abraham).
male(clancy).

female(marge).
female(lisa).
female(maggie).
female(mona).
female(jacqueline).

% Rule
grandparent(X, Z) :- parent(X, Y), parent(Y, Z).
