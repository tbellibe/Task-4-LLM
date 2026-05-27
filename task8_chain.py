"""
task8_chain.py - Simplified Logic-LM Chain using real kb.pl
"""
from pyswip import Prolog

KB_FILE = "kb.pl"

def run_chain(question, animal):
    trace = [f"Parsing query for: {animal}"]
    
    # Initialize Prolog and load your actual kb.pl file
    prolog = Prolog()
    prolog.consult(KB_FILE)
    
    # Formulate the query goal based on your kb.pl rule: can_fly(X)
    goal = f"can_fly({animal})"
    trace.append(f"  → Formulated Prolog goal: {goal}")
    
    # Execute the query against your real knowledge base
    try:
        solutions = list(prolog.query(goal))
        is_true = len(solutions) > 0
    except Exception as e:
        trace.append(f"  ✗ Solver Error: {str(e)}")
        return False, trace

    # Build the inference trace dynamically based on what the KB returned
    if is_true:
        trace.append(f"  ✓ '{animal}' matched factual pathways and rules in {KB_FILE}")
    else:
        trace.append(f"  ✗ '{animal}' failed constraints or is missing from {KB_FILE}")
        
    return is_true, trace

if __name__ == "__main__":
    QUERIES = [
        ("Can a bat fly?", "bat"),
        ("Can a penguin fly?", "penguin"),
        ("Can a dog fly?", "dog")
    ]

    print("=== TASK 8 RUN (CONNECTED TO KB.PL) ===")
    for q, a in QUERIES:
        result, trace = run_chain(q, a)
        print(f"\nQ: {q}")
        print(f"Result: {'TRUE' if result else 'FALSE'}")
        print("Trace:")
        for line in trace:
            print(f"  {line}")
