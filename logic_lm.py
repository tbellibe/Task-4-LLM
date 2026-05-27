"""
logic_lm.py
LangChain Logic-LM — logical inference engine
Based on Logic-LM (Pan et al., 2023)
"""

import os

# ── Knowledge Base ────────────────────────────────────────────────────────────

FACTS = {
    "mammal": ["bat", "whale"],
    "bird": ["penguin", "eagle"],
    "has_wings": ["bat", "penguin", "eagle"],
}

RULES = [
    "A bird with wings that is NOT a penguin can fly.",
    "A mammal with wings can fly.",
]


# ── Prolog-style inference ────────────────────────────────────────────────────

def can_fly(animal):
    trace = []
    if animal in FACTS["bird"]:
        trace.append(f"{animal} is a bird ✓")
        if animal in FACTS["has_wings"]:
            trace.append(f"{animal} has wings ✓")
            if animal == "penguin":
                trace.append(f"{animal} is a penguin → blocked by rule ✗")
                return False, trace
            return True, trace
    if animal in FACTS["mammal"]:
        trace.append(f"{animal} is a mammal ✓")
        if animal in FACTS["has_wings"]:
            trace.append(f"{animal} has wings ✓")
            return True, trace
    trace.append("no rule matched → FALSE")
    return False, trace


# ── LangChain explanation chain ───────────────────────────────────────────────

def explain(question, result, trace):
    from langchain_anthropic import ChatAnthropic
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser

    llm = ChatAnthropic(model="claude-sonnet-4-6", max_tokens=200)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a logic tutor. Explain the inference result in 2 sentences."),
        ("human", "Question: {question}\nResult: {result}\nTrace: {trace}"),
    ])
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({
        "question": question,
        "result": "TRUE" if result else "FALSE",
        "trace": "\n".join(trace),
    })


# ── Main ──────────────────────────────────────────────────────────────────────

QUERIES = [
    ("Can a bat fly?",     "bat"),
    ("Can a penguin fly?", "penguin"),
]

for question, animal in QUERIES:
    result, trace = can_fly(animal)
    print(f"\nQ: {question}")
    print(f"Result: {'TRUE ✓' if result else 'FALSE ✗'}")
    print("Trace:")
    for line in trace:
        print(f"  {line}")
    if os.environ.get("ANTHROPIC_API_KEY"):
        print("Explanation:", explain(question, result, trace))
