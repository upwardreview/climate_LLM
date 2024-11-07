from langchain.prompts import ChatPromptTemplate

learning_objectives_prompt = ChatPromptTemplate.from_template(
    "List 8-10 bullet points for learning objectives of the from content of context: {context}. return bullet points only."
)

# 1. Introduction & Basics (with Anecdote)
introduction_prompt = ChatPromptTemplate.from_template(
    """
    Write a 500-word introduction that:
    - Defines the main term and explains its significance.
    - Engages the reader by linking the topic to everyday life and relatable modern brands like Tesla and Apple.
    - Includes examples of how these brands connect to the topic's themes (e.g., technology, sustainability).

    Important: Do not include a conclusion. Use markdown headings if needed for readability.
    
    Context: {context}
    """
)

#2. History & Development
history_development_prompt = ChatPromptTemplate.from_template(
    """
    Continue from the previous sections:
    
    Previous sections: {answer}<END OF PREVIOUS SECTIONS>
    
    Describe the historical development of this energy source:
    - Trace its journey from early discoveries or inventions to major breakthroughs and challenges.
    - Highlight notable events or incidents that shaped its perception, such as significant breakthroughs or crises (e.g., Chernobyl for nuclear power).
    - Use markdown for headings like "Early Discoveries" and "Key Events."

    Important: Keep a factual tone based on the provided context, and avoid including a conclusion.

    Context: {context}
    """
)

# 3. Technical & Operational Details

technical_details_prompt = ChatPromptTemplate.from_template(
    """
    Continue from the previous sections:
    
    Previous sections: {answer}<END OF PREVIOUS SECTIONS>
    
    Explain the technical and operational details of this energy source:
    - Describe its mechanics and infrastructure needs, covering aspects like energy conversion, storage, and distribution challenges.
    - Organize sections with headings like "Technical Mechanics" and "Infrastructure Needs."
    - Include real-world examples with numbers and formulas, formatted in LaTeX (`$` for inline equations, `$$` for block equations).

    Important: Base all information strictly on the provided context, with no conclusions.

    Context: {context}
    """
)

# 4. Economic & Geopolitical Considerations
economic_geopolitical_prompt = ChatPromptTemplate.from_template(
    """
    Continue from the previous sections:
    
    Previous sections: {answer}<END OF PREVIOUS SECTIONS>
    
    Discuss the economic and geopolitical factors associated with this energy source:
    - Cover aspects like production costs, market potential, and competitiveness.
    - Touch on geopolitical dynamics, including leading countries, supply chains, and international trade aspects.
    - Organize content with headings such as "Economic Viability" and "Global Influence."
    - Include real-world examples with numbers and formulas, formatted in LaTeX (`$` for inline equations, `$$` for block equations).

    Important: Draw only from the provided context, linking technical details to real-world economic and political perspectives.

    Context: {context}
    """
)

# 5. Controversies, Environmental Impact & Social Perspectives
controversies_impact_prompt = ChatPromptTemplate.from_template(
    """
    Continue from the previous sections:
    
    Previous sections: {answer}<END OF PREVIOUS SECTIONS>
    
    Examine the controversies, environmental impacts, and social perspectives of this energy source:
    - Highlight key debates and ethical concerns, such as environmental risks, waste management, and public perception.
    - Address regulatory frameworks and any incentives influencing the energy source's adoption.
    - Structure the response with headings like "Environmental Concerns," "Public Debate," and "Regulatory Factors."
    - Include real-world examples with numbers and formulas, formatted in LaTeX (`$` for inline equations, `$$` for block equations).

    Important: Ensure a balanced and factual tone, based solely on the provided context.

    Context: {context}
    """
)

future_outlook_prompt = ChatPromptTemplate.from_template(
    """
    Continue from the previous sections:
    
    Previous sections: {answer}<END OF PREVIOUS SECTIONS>
    
    Explore the future outlook for this energy source, focusing on recent innovations and emerging trends:
    - Discuss ongoing research and promising advancements that could shape the energy source's role in a sustainable future.
    - Present this section with a forward-looking tone, organized under headings like "Ongoing Research" and "Future Potential."
    - Include real-world examples with numbers and formulas, formatted in LaTeX (`$` for inline equations, `$$` for block equations).

    Important: Base your response strictly on the provided context, with no final conclusion.

    Context: {context}
    """
)

# Multiple-Choice Questions Chain
mcq_prompt = ChatPromptTemplate.from_template(
    "Generate 10 multiple-choice questions based on the following text: {context}, including 2 on the introduction "
    "and 8 on the detailed explanation."
)



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
