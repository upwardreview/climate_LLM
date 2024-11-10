import streamlit as st
from st_copy_to_clipboard import st_copy_to_clipboard
from data_ingestion import DocumentProcessor
from chain_setup import ConversationalRAG

# Title for the app
st.title("AI Assistant")

# Sidebar inputs for RSS URL, index name, folder ID, and latest podcast number
with st.sidebar:
    debug = st.checkbox("Debugging mode?",value=False)
    index_name = st.text_input("Enter the Pinecone index name:", value="test").strip()
    folder_id = st.text_input("Enter the folder ID in Google Drive").strip()
    k_value = st.slider("Set the value of k (number of documents to retrieve):", 0, 100, value=30)
    download = st.checkbox("Download latest podcasts instead?",value=False)
    latest_n = st.number_input("Latest number of podcasts to be ingested (-1 for all)", value=10)
    rss_url = st.text_input("Enter podcast RSS feed URL", value="https://feeds.simplecast.com/XFfCG1w8")

    

# Initialize session state for storing chat history, sources, user input, and processor if not already initialized
for key in ['conversation_history', 'sources', 'submitted_input', 'processor']:
    if key not in st.session_state:
        st.session_state[key] = [] if key in ['conversation_history', 'sources'] else ""

# Cached function to initialize DocumentProcessor
@st.cache_resource
def init_document_processor(index_name):
    if index_name:
        return DocumentProcessor(index_name=index_name)
    return None

# Cached function to initialize ConversationalRAG
@st.cache_resource
def init_conversational_rag(k):
    return ConversationalRAG(k=k)

# Initialize DocumentProcessor and ConversationalRAG with desired values
st.session_state.processor = init_document_processor(index_name)
conversational_rag = init_conversational_rag(k=k_value)

with st.sidebar:
    ingest = st.button("Ingest/Check for new docs in your Drive data folder")
    if download:
        podcast = st.button("Process podcasts transcriptions for download")
    else:
        podcast = st.button("Ingest podcasts (may take time)")

## Drive
if ingest and folder_id and index_name:
    st.session_state.processor.process_and_add_documents_from_drive(folder_id)
elif ingest:
    with st.sidebar:
        st.error("Enter folder ID and index name")

## Podcasts
if podcast and latest_n and index_name and rss_url:
    st.session_state.processor.process_and_add_new_podcasts(rss_url=rss_url, latest_n=latest_n, download=download, debug=debug)
else:
    if podcast:
        with st.sidebar:
            st.error("Enter latest number of podcasts and index name or rss_url")

# Cached function to initialize ConversationalRAG
@st.cache_resource
def init_conversational_rag(k):
    return ConversationalRAG(k=k)

# Initialize ConversationalRAG with desired `k` value
conversational_rag = init_conversational_rag(k=10)

# Function to invoke the conversational chain and update the chat history
def process_message():
    user_input = st.session_state.get('submitted_input', '')  # Get the submitted input
    if user_input.strip():
        # Add user message to chat history
        st.session_state.conversation_history.append({
            "role": "user",
            "content": user_input
        })
        
        # Call get_response from ConversationalRAG instance
        try:
            response = conversational_rag.get_response(user_input, session_id="user")
            st.session_state.sources = response["sources"]
            ai_response = response["answer"]
            
            # Add AI response to chat history
            st.session_state.conversation_history.append({
                "role": "assistant",
                "content": ai_response,
                "sources": st.session_state.sources
            })

        except Exception as e:
            st.session_state.conversation_history.append({
                "role": "assistant",
                "content": f"Error generating response: {e}",
                "sources": "None"
            })
            print(f"Error occurred: {e}")
        
        # Clear the input after sending the message
        st.session_state.submitted_input = ""  # Clear the submitted input
# Define the style for the chat display
style = """
    <style>
    h1, h2, h3, h4, h5, h6 {
        color: #000000 !important;
    }
    </style>
"""

# Display conversation history with containers and a copy button for each message
for idx, message in enumerate(st.session_state.conversation_history):
    role = message['role']
    
    if role == "user":
        with st.chat_message("user"):
            st.markdown(f'<div style="padding: 10px; color: #000000; border-radius: 10px;">\n{message["content"]}</div>', unsafe_allow_html=True)
    
    elif role == "assistant":
        with st.chat_message("assistant"):
            sources = " | ".join(message.get('sources', []))
            st.markdown(f'<div style="background-color: #F5F5F5; padding: 10px; color: #000000; border-radius: 10px;">\n{message["content"]}</div>', unsafe_allow_html=True)
            st.markdown(f"<small><strong>Sources:</strong> {sources}</small>", unsafe_allow_html=True)
       
        # Display the message with custom styling
        # st.markdown(title, unsafe_allow_html=True)
        # st.markdown(f'{style}{message_html}', unsafe_allow_html=True)
        

# Use a text_area for user input and store its value in 'submitted_input'
user_input = st.text_area(
    "You:", 
    value="", 
    placeholder="Type your message here...", 
    height=100,
)

# Button to send the message
if st.button("Send"):
    st.session_state.submitted_input = user_input
    process_message()
    st.rerun()
# Display the sources in a readable format
st.write("Sources:")
for source in st.session_state.sources:
    st.write(f"- {source}")
