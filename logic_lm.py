
from dataclasses import dataclass, field
from typing import Optional
import re

@dataclass
class LogicProgram:
    facts: list = field(default_factory=list)
    rules: list = field(default_factory=list)
    query: str = ""
    raw: str = ""

@dataclass
class SolverResult:
    answer: Optional[bool] = None
    proof: list = field(default_factory=list)
    error: Optional[str] = None

def solve(program):
    try:
        kb = set(program.facts)
        proof = list(program.facts)
        for _ in range(50):
            new_facts = set()
            for rule in program.rules:
                if "->" not in rule:
                    raise ValueError("Rule missing arrow: " + str(rule))
                antecedent_str, consequent_tpl = rule.split("->", 1)
                antecedents = [a.strip() for a in antecedent_str.split("&")]
                consequent_tpl = consequent_tpl.strip()
                for binding in _find_bindings(antecedents, kb):
                    new_fact = _apply_binding(consequent_tpl, binding)
                    if new_fact not in kb:
                        new_facts.add(new_fact)
                        proof.append(f"{rule} -> {new_fact}")
            if not new_facts:
                break
            kb |= new_facts
        return SolverResult(answer=program.query.strip() in kb, proof=proof)
    except Exception as exc:
        return SolverResult(error=str(exc))

def _find_bindings(antecedents, kb):
    bindings = [{}]
    for ant in antecedents:
        next_bindings = []
        for binding in bindings:
            grounded = _apply_binding(ant, binding)
            if _is_ground(grounded):
                if grounded in kb:
                    next_bindings.append(binding)
            else:
                pred = ant.split("(")[0]
                inner_template = ant[len(pred)+1:-1]
                for fact in kb:
                    if fact.startswith(pred + "("):
                        fact_inner = fact[len(pred)+1:-1]
                        fact_args = [a.strip() for a in fact_inner.split(",")]
                        tmpl_args = [a.strip() for a in inner_template.split(",")]
                        new_binding = dict(binding)
                        match = True
                        for t, f in zip(tmpl_args, fact_args):
                            if t[0].isupper():
                                if t in new_binding and new_binding[t] != f:
                                    match = False; break
                                new_binding[t] = f
                            elif t != f:
                                match = False; break
                        if match:
                            next_bindings.append(new_binding)
        bindings = next_bindings
    return bindings

def _apply_binding(template, binding):
    for var, val in binding.items():
        template = template.replace(var, val)
    return template

def _is_ground(atom):
    inner = re.search(r"\((.+)\)", atom)
    if not inner:
        return True
    return inner.group(1) == inner.group(1).lower()

def _extract_variable(atom):
    inner = re.search(r"\(([^)]+)\)", atom)
    if inner:
        for token in inner.group(1).split(","):
            token = token.strip()
            if token[0].isupper():
                return token
    raise ValueError("No variable found in atom: " + str(atom))

def backward_chain(query, facts, rules, depth=0, max_depth=20):
    if depth > max_depth:
        return False
    if query in facts:
        return True
    for rule in rules:
        if "->" not in rule:
            continue
        antecedent_str, consequent_tpl = rule.split("->", 1)
        antecedents = [a.strip() for a in antecedent_str.split("&")]
        consequent_tpl = consequent_tpl.strip()
        binding = _unify(consequent_tpl, query)
        if binding is None:
            continue
        if _prove_antecedents(antecedents, binding, facts, rules, depth):
            return True
    return False

def _prove_antecedents(antecedents, binding, facts, rules, depth):
    if not antecedents:
        return True
    ant = antecedents[0]
    rest = antecedents[1:]
    bound = _apply_binding(ant, binding)
    if _is_ground(bound):
        if not backward_chain(bound, facts, rules, depth+1):
            return False
        return _prove_antecedents(rest, binding, facts, rules, depth)
    else:
        pred = ant.split("(")[0]
        for fact in facts:
            if fact.startswith(pred + "("):
                new_binding = _unify(bound, fact, dict(binding))
                if new_binding is not None:
                    if _prove_antecedents(rest, new_binding, facts, rules, depth):
                        return True
        return False

def _unify(template, ground, existing_binding=None):
    if existing_binding is None:
        existing_binding = {}
    t_pred = template.split("(")[0]
    g_pred = ground.split("(")[0]
    if t_pred != g_pred:
        return None
    t_inner = re.search(r"\(([^)]+)\)", template)
    g_inner = re.search(r"\(([^)]+)\)", ground)
    if not t_inner or not g_inner:
        return None
    t_args = [a.strip() for a in t_inner.group(1).split(",")]
    g_args = [a.strip() for a in g_inner.group(1).split(",")]
    if len(t_args) != len(g_args):
        return None
    binding = dict(existing_binding)
    for t, g in zip(t_args, g_args):
        if t[0].isupper():
            if t in binding and binding[t] != g:
                return None
            binding[t] = g
        elif t != g:
            return None
    return binding
