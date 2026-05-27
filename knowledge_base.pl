% ============================================================
% Animals Knowledge Base
% 17 facts, 8 rules
% ============================================================

% --- Facts ---
mammal(dog).
mammal(cat).
mammal(whale).
mammal(bat).
mammal(human).

bird(eagle).
bird(penguin).
bird(parrot).

reptile(snake).
reptile(crocodile).

has_wings(eagle).
has_wings(bat).
has_wings(parrot).
has_wings(penguin).

lives_in_water(whale).
lives_in_water(crocodile).
lives_in_water(penguin).

% --- Rules ---
animal(X) :- mammal(X).
animal(X) :- bird(X).
animal(X) :- reptile(X).

can_fly(X) :- bird(X), has_wings(X), \+(X = penguin).
can_fly(X) :- mammal(X), has_wings(X).

warm_blooded(X) :- mammal(X).
warm_blooded(X) :- bird(X).
cold_blooded(X) :- reptile(X).

aquatic(X) :- lives_in_water(X).

vertebrate(X) :- animal(X).
