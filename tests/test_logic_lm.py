
import sys
sys.path.insert(0, '.')
from logic_lm import LogicProgram, solve, backward_chain

FACTS = [
    "parent(homer, bart)", "parent(homer, lisa)", "parent(homer, maggie)",
    "parent(marge, bart)", "parent(marge, lisa)", "parent(marge, maggie)",
    "parent(abraham, homer)", "parent(mona, homer)",
    "parent(clancy, marge)", "parent(jacqueline, marge)",
]
RULES = ["parent(X, Y) & parent(Y, Z) -> grandparent(X, Z)"]

def test_fc_homer_is_barts_parent():
    r = solve(LogicProgram(facts=FACTS, rules=[], query="parent(homer, bart)"))
    assert r.answer == True

def test_fc_abraham_is_grandparent_of_bart():
    r = solve(LogicProgram(facts=FACTS, rules=RULES, query="grandparent(abraham, bart)"))
    assert r.answer == True

def test_fc_clancy_is_not_homers_parent():
    r = solve(LogicProgram(facts=FACTS, rules=[], query="parent(clancy, homer)"))
    assert r.answer == False

def test_bc_homer_is_barts_parent():
    assert backward_chain("parent(homer, bart)", FACTS, []) == True

def test_bc_abraham_is_grandparent_of_bart():
    assert backward_chain("grandparent(abraham, bart)", FACTS, RULES) == True

def test_bc_jacqueline_is_grandparent_of_lisa():
    assert backward_chain("grandparent(jacqueline, lisa)", FACTS, RULES) == True

def test_bc_clancy_is_not_homers_parent():
    assert backward_chain("parent(clancy, homer)", FACTS, []) == False

def test_bc_mona_is_grandparent_of_maggie():
    assert backward_chain("grandparent(mona, maggie)", FACTS, RULES) == True
