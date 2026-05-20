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
    raise ValueError(f"No variable found in atom: {atom}")
