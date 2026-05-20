
import sys
sys.path.insert(0, '.')
from logic_lm import LogicProgram, solve

FACTS = [
    "parent(homer, bart)", "parent(homer, lisa)", "parent(homer, maggie)",
    "parent(marge, bart)", "parent(marge, lisa)", "parent(marge, maggie)",
    "parent(abraham, homer)", "parent(mona, homer)",
    "parent(clancy, marge)", "parent(jacqueline, marge)",
]
RULE = "parent(X, Y) & parent(Y, Z) -> grandparent(X, Z)"

def test_homer_is_barts_parent():
    r = solve(LogicProgram(facts=FACTS, rules=[], query="parent(homer, bart)"))
    assert r.answer == True

def test_abraham_is_grandparent_of_bart():
    r = solve(LogicProgram(facts=FACTS, rules=[RULE], query="grandparent(abraham, bart)"))
    assert r.answer == True

def test_jacqueline_is_grandparent_of_lisa():
    r = solve(LogicProgram(facts=FACTS, rules=[RULE], query="grandparent(jacqueline, lisa)"))
    assert r.answer == True

def test_clancy_is_not_homers_parent():
    r = solve(LogicProgram(facts=FACTS, rules=[], query="parent(clancy, homer)"))
    assert r.answer == False

def test_mona_is_grandparent_of_maggie():
    r = solve(LogicProgram(facts=FACTS, rules=[RULE], query="grandparent(mona, maggie)"))
    assert r.answer == True
