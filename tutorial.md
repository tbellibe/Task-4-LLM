For Task 9, I researched and implemented a LangChain-based logical inference engine based on the Logic-LM approach (Pan et al., 2023). The idea is to combine an LLM with symbolic logic — the LLM handles natural language while a Prolog engine handles the actual reasoning.

To get started, I installed LangChain and built the pipeline in logic_lm.py. I also created a Prolog knowledge base (knowledge_base.pl) with 17 facts and 8 rules about animals. The pipeline takes a natural language question, uses RAG to find relevant facts from the KB, translates the question into a Prolog goal using a LangChain chain, then runs backward chaining to return TRUE or FALSE with a full inference trace.

I tested the system on 2 queries. First, "Can a bat fly?" returned TRUE because the engine matched mammal(bat) and has_wings(bat) through the rule can_fly(X) :- mammal(X), has_wings(X). Second, "Can a penguin fly?" returned FALSE because the can_fly rule uses negation-as-failure (+) to block penguins even though they are birds with wings.

Overall, this task helped me understand how LangChain can bridge natural language and symbolic reasoning, and how RAG helps the LLM output the correct Prolog goal by providing relevant context.
