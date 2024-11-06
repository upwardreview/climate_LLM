import io
import zipfile
import time
import streamlit as st
from chapter import ChapterGenerator


if "chapters" not in st.session_state:
    st.session_state.chapters = []

# Initialize Chapter Generator
@st.cache_resource
def init_generator():
    return ChapterGenerator()
generator = init_generator()

st.title("AI-Powered Chapter Generator For Daniel")
st.write("Generate a chapter with structured sections from a given topic.")

topic = st.text_input("Enter a topic for the chapter:")
if st.session_state.chapters:
    with st.sidebar:
        zip_buffer = io.BytesIO()

        # Create a zip file and add each transcript
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            for id, chapter in st.session_state.chapters:
                # Create a text file for each transcript inside the zip file
                filename = f"{id}."
                zf.writestr(filename, chapter)
        
        # Seek to the beginning of the BytesIO buffer so it can be read
        zip_buffer.seek(0)

        # Provide a download button in Streamlit for the zip file
        st.download_button(
            label="Download All Chapters generated in this session as ZIP",
            data=zip_buffer,
            file_name="transcripts.zip",
            mime="application/zip"
        )

# User input for topic

if st.button("Generate") and topic:
    with st.spinner("Generating chapter..."):
        with st.sidebar:
            st.write("Generating")
            final_output = generator.generate_chapter(topic)
            # final_output = "niggasd"
            st.success("Chapter generated successfully!")
        st.markdown(final_output, unsafe_allow_html=True)
        st.session_state.chapters.append([topic, final_output])

# Option to download the output as a file
if st.session_state.chapters:
    with st.sidebar:
        st.download_button(
            label="Download latest Chapter you generated",
            data=st.session_state.chapters[-1][1],
            file_name="generated_chapter.md",
            mime="text/markdown"
        )