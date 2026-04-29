from pyswip import Prolog

prolog = Prolog()
prolog.consult("kb.pl")

print("Grandparents of Bart:")
for r in prolog.query("grandparent(X, bart)"):
    print(r["X"])

print("\nSiblings of Bart:")
for r in prolog.query("sibling(bart, X)"):
    print(r["X"])
