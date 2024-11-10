import streamlit as st

pg = st.navigation(
    [
    st.Page("./chapter_streamlit.py", title="Chapter", url_path="chapter"),
    st.Page("./simpleqna.py", title="Simple", url_path="qna")
    ]
)
pg.run()
