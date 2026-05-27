For Task 8, I researched and implemented a LangChain-based logical inference engine based on the Logic-LM approach (Pan et al., 2023). The idea is to combine an LLM with symbolic logic — the LLM handles natural language while a Prolog engine handles the actual reasoning.

To get started, I installed LangChain and built the pipeline in logic_lm.py. I also created a Prolog knowledge base (knowledge_base.pl) with 17 facts and 8 rules about animals. The pipeline works in four steps: a RAG retriever finds relevant facts from the KB, a LangChain chain translates the question into a Prolog goal like can_fly(bat), the Prolog engine runs backward chaining and returns TRUE or FALSE with a full inference trace, and a second LangChain chain explains the result in plain English.

I tested the system on 8 queries and all returned correct results. The most interesting case was the penguin — the engine correctly returns FALSE because the can_fly rule uses negation-as-failure (+) to block penguins even though they are birds with wings.

Overall, this task helped me understand how LangChain can bridge natural language and symbolic reasoning, and how RAG helps reduce errors in the LLM output by providing relevant context.
