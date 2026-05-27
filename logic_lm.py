"""
logic_lm.py
LangChain Logic-LM — logical inference engine
Based on Logic-LM (Pan et al., 2023) logic
"""

# ── Knowledge Base ────────────────────────────────────────────────────────────
# 11 clean facts, 2 structured rules

FACTS = {
    "mammal": ["dog", "cat", "whale", "bat", "human"],
    "bird": ["eagle", "penguin", "parrot"],
    "has_wings": ["eagle", "bat", "parrot", "penguin"],
}

RULES = [
    "A bird with wings that is NOT a penguin can fly.",
    "A mammal with wings can fly.",
]


# ── Prolog-style inference ────────────────────────────────────────────────────

def can_fly(animal):
    trace = []
    
    # Rule 1: A bird with wings that is NOT a penguin can fly
    if animal in FACTS["bird"]:
        trace.append(f"{animal} is a bird ✓")
        if animal in FACTS["has_wings"]:
            trace.append(f"{animal} has wings ✓")
            if animal == "penguin":
                trace.append(f"{animal} is a penguin → blocked by rule ✗")
                return False, trace
            return True, trace
            
    # Rule 2: A mammal with wings can fly
    if animal in FACTS["mammal"]:
        trace.append(f"{animal} is a mammal ✓")
        if animal in FACTS["has_wings"]:
            trace.append(f"{animal} has wings ✓")
            return True, trace
            
    trace.append("no rule matched → FALSE")
    return False, trace


# ── Main Execution ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    QUERIES = [
        ("Can a bat fly?",     "bat"),
        ("Can a penguin fly?", "penguin"),
        ("Can a dog fly?",     "dog")
    ]

    print("========================================")
    print("LOGICAL INFERENCE ENGINE RESULTS (LOGIC-LM)")
    print("========================================")

    for question, animal in QUERIES:
        result, trace = can_fly(animal)
        print(f"\nQ: {question}")
        print(f"Result: {'TRUE ✓' if result else 'FALSE ✗'}")
        print("Trace:")
        for line in trace:
            print(f"  {line}")
        print("-" * 40)
