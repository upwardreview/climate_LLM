import streamlit as st

pg = st.navigation(
    [
    st.Page("./chapter_streamlit.py", title="Chapter", url_path="chapter",default=True),
    st.Page("./streamlit_ui.py", title="Simple", url_path="qna")
    ]
)
pg.run()
