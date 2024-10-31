
general_prompt = (
    "You are writing a textbook on energy and climate change, aimed at making complex topics accessible and engaging for modern students. "
    "Each topic should start by listing out the 8-10 bullet points for learning objectives of the chapter. "
    "Begin with a 500-word introduction that defines the term, explains its importance, and includes relatable examples using modern brands like Tesla and Apple. "
    "This MUST be followed by a no less than 4,000-word detailed explanation that starts with a personal anecdote, explains technical details, political issues, and the impact on energy and climate change. "
    "Provide at least one real-world example with numbers and formulas in LaTeX for every 1,000 words. "
    "Very important: Start all LaTeX equations with `$` for inline equations or `$$` for block equations. "
    "The explanation should cover why the topic is important today and in the future, and present major controversies with a balanced view of pros and cons. "
    "Do not take a position on the controversies but explain both sides objectively. "
    "At the end of the detailed section, include 10 multiple-choice questions: 2 on the introduction and 8 on the detailed explanation. "
    "If more context is needed to complete the detailed section, politely inform the user that additional context is required. "
    "Your response should be based solely on the provided context, without referencing any external sources."
    "\n\n"
    "Context:\n{context}"
)


testing_prompt = """
Write 4000 words using the about a topic using the context given, like writing a whole chapter, book on
the topic.
\nContext:\n{context}
"""

contextualize_q_system_prompt = (
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, "
    "just reformulate it if needed and otherwise return it as is."
)
