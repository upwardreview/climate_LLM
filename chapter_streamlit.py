import io
import zipfile
import time
import streamlit as st
from chapter import ChapterGenerator

with st.sidebar:
    test = st.checkbox("testing/debugging?", value=False)
    st.write("Means if selected, openai credits wont be used, a sample chapter will be generated.")
if "chapters" not in st.session_state:
    st.session_state.chapters = []

# Initialize Chapter Generator
@st.cache_resource
def init_generator():
    return ChapterGenerator()
generator = init_generator()

st.title("AI-Powered Chapter Generator For Daniel")
st.write("Generate a chapter with structured sections from a given topic.")

if st.session_state.chapters:
    with st.sidebar:
        zip_buffer = io.BytesIO()

        # Create a zip file and add each transcript
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            for chapter in st.session_state.chapters:
                # Create a text file for each transcript inside the zip file
                filename = f"{chapter['topic']}.md"
                zf.writestr(filename, chapter['output'])
        
        # Seek to the beginning of the BytesIO buffer so it can be read
        zip_buffer.seek(0)

        # Provide a download button in Streamlit for the zip file
        st.download_button(
            label="Download All Chapters generated in this session as ZIP",
            data=zip_buffer,
            file_name="chapters.zip",
            mime="application/zip"
        )

# User input for topic


# Option to download the output as a file
topic = st.text_input("Enter a topic for the chapter:")
if st.session_state.chapters:
    with st.sidebar:
        st.download_button(
            label="Download latest Chapter you generated",
            data=st.session_state.chapters[-1]['output'],
            file_name="generated_chapter.md",
            mime="text/markdown"
        )

if st.button("Generate") and topic:
    with st.spinner("Generating chapter..."):
        with st.sidebar:
            st.write("Generating")
            if test:
                with open("test.md", "r") as c:
                    output = c.read()
                output, sources = output , "sources"
            else:
                output, sources = generator.generate_chapter(topic)
            st.success("Chapter generated successfully!")
            st.session_state.chapters.append({"topic":topic,"output": output,"sources": sources})
            st.rerun()
        
for chapter in st.session_state.chapters:
    with st.chat_message("user"):
        st.markdown(chapter['topic'], unsafe_allow_html=True)
    with st.chat_message("assistant"):
        st.markdown(f"\n\n{chapter['output']}", unsafe_allow_html=True)
        st.markdown(f"<small><strong>Sources:</strong> {chapter['sources']}</small>", unsafe_allow_html=True)
