from prompts import general_prompt, contextualize_q_system_prompt
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.vectorstores import FAISS
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import AIMessage
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from data_ingestion import DocumentProcessor
import os
from dotenv import load_dotenv
from warnings import filterwarnings

filterwarnings("ignore")
load_dotenv()

class ConversationalRAG:
    def __init__(self, k=30):
        self.k = k
        self.dl = DocumentProcessor("./data/")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.embeddings = OpenAIEmbeddings(api_key=self.openai_api_key)
        self.openai_llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
        self.vector_store = self.load_vector_store()
        self.store = {}
        
        self.contextualize_q_prompt = self.create_prompt(contextualize_q_system_prompt)
        self.history_aware_retriever = self.create_history_aware_retriever()
        self.qa_prompt = self.create_prompt(general_prompt)
        self.question_answer_chain = self.create_question_answer_chain()
        self.rag_chain = self.create_retrieval_chain()
        self.conversational_rag_chain = self.create_conversational_chain()

    def load_vector_store(self):
        print("Loading vector store")
        try:
            vector_store = self.dl.vector_store
            print("Loaded successfully")
            return vector_store
        except:
            print("Vector database not found. Creating vector database. This might take some time")
            # Logic to initialize a new vector store if needed

    def create_prompt(self, system_prompt):
        return ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )

    def create_history_aware_retriever(self):
        retriever = self.vector_store.as_retriever(search_kwargs={"k": self.k})
        return create_history_aware_retriever(self.openai_llm, retriever, self.contextualize_q_prompt)

    def create_question_answer_chain(self):
        return create_stuff_documents_chain(self.openai_llm, self.qa_prompt)

    def create_retrieval_chain(self):
        return create_retrieval_chain(self.history_aware_retriever, self.question_answer_chain)

    def create_conversational_chain(self):
        return RunnableWithMessageHistory(
            self.rag_chain,
            self.get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer",
        )

    def get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        if session_id not in self.store:
            self.store[session_id] = ChatMessageHistory()
        return self.store[session_id]

    def get_response(self, user_input: str, session_id: str = "user"):
        response = self.conversational_rag_chain.invoke(
            {"input": user_input},
            config={"configurable": {"session_id": session_id}}
        )
        sources = list(set([document.metadata['source'] for document in response["context"]]))
        return {"answer": response["answer"], "sources": sources}

# Usage
if __name__ == "__main__":
    conversational_rag = ConversationalRAG(k=10)  # Set k as desired
    while True:
        user_input = input("User --> ")
        response = conversational_rag.get_response(user_input)
        print("Answer:", response["answer"])
        print("Sources:", response["sources"])