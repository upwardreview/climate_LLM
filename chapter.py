from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from data_ingestion import DocumentProcessor
import streamlit as st
from prompts import (
    introduction_prompt,
    future_outlook_prompt,
    controversies_impact_prompt,
    economic_geopolitical_prompt,
    history_development_prompt,
    learning_objectives_prompt,
    mcq_prompt,
    technical_details_prompt
)


class ChapterGenerator:
    def __init__(self, model="gpt-4o", temperature=0.2):
        self.llm = ChatOpenAI(api_key=st.secrets['OPENAI_API_KEY'],model=model, temperature=temperature)
        self.dp = DocumentProcessor()
        self.markdown_output = ""

    def add_to_output(self, heading, content):
        self.markdown_output += f"\n# {heading}\n" + content
        with open("chapter_out.txt", "w") as c:
            c.write("\n\n" + self.markdown_output)

    def get_context(self, user_input):
        context = self.dp.vector_store.similarity_search(user_input, k=100)
        self.sources = list(set([document.metadata['source'] for document in context]))
        return "\n\n".join([doc.page_content for doc in context])


    def generate_section(self, prompt_template, context, previous_section_text=""):
        chain = (
            {"context": RunnablePassthrough(), "answer": RunnablePassthrough()}
            | prompt_template
            | self.llm
            | StrOutputParser()
        )
        return chain.invoke({"context": context, "answer": previous_section_text})

    def create_section_prompts(self, formatted_context):
        # Learning Objectives
        learning_obj = self.generate_section(learning_objectives_prompt, formatted_context)
        self.add_to_output("Learning Objectives", learning_obj)
        st.info("Learning Objectives")

        # Introduction & Basics
        introduction = self.generate_section(introduction_prompt, formatted_context)
        self.add_to_output("1. Introduction & Basics (with Anecdote)", introduction)
        st.info("Introduction & Basics (with Anecdote) Done")
        print("Introduction & Basics Completed")

        # History & Development
        history = self.generate_section(history_development_prompt, formatted_context, previous_section_text=introduction)
        self.add_to_output("2. History & Development", history)
        st.info("History & Development Done")
        print("History & Development Completed")

        # Technical & Operational Details
        technical = self.generate_section(technical_details_prompt, formatted_context, previous_section_text=history)
        self.add_to_output("3. Technical & Operational Details", technical)
        st.info("Technical & Operational Details Done")
        print("Technical & Operational Details Completed")

        # Economic & Geopolitical Considerations
        economic = self.generate_section(economic_geopolitical_prompt, formatted_context, previous_section_text=technical)
        self.add_to_output("4. Economic & Geopolitical Considerations", economic)
        st.info("Economic & Geopolitical Considerations Done")
        print("Economic & Geopolitical Considerations Completed")

        # Controversies, Environmental Impact & Social Perspectives
        controversies = self.generate_section(controversies_impact_prompt, formatted_context, previous_section_text=economic)
        self.add_to_output("5. Controversies, Environmental Impact & Social Perspectives", controversies)
        st.info("Controversies, Environmental Impact & Social Perspectives Done")
        print("Controversies, Environmental Impact & Social Perspectives Completed")

        # Future Outlook & Innovations
        future = self.generate_section(future_outlook_prompt, formatted_context, previous_section_text=controversies)
        self.add_to_output("6. Future Outlook & Innovations", future)
        st.info("Future Outlook & Innovations Done")
        print("Future Outlook & Innovations Completed")

        # Multiple-Choice Questions based on the full chapter content
        combined_intro_and_detailed = f"{learning_obj}\n\n{introduction}\n\n{history}\n\n{technical}\n\n{economic}\n\n{controversies}\n\n{future}"
        mcq_chain = (
            {"context": RunnablePassthrough()}
            | mcq_prompt
            | self.llm
            | StrOutputParser()
        )
        mcqs = mcq_chain.invoke({"context": combined_intro_and_detailed})
        self.add_to_output("Multiple-Choice Questions Done", mcqs)
        st.info("### Multiple-Choice Questions\n")
        print("MCQs")

    def generate_chapter(self, user_topic):
        # Retrieve and format context
        print("Getting context")
        formatted_context = self.get_context(user_topic)
        # Generate chapter sections
        print("Getting output")
        self.create_section_prompts(formatted_context)
        print("Done")

        return self.markdown_output, self.sources
if __name__ == '__main__':
    resp = ChapterGenerator().get_context(user_input="Geothermal")