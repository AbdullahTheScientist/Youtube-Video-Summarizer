import streamlit as st

st.set_page_config(page_title="YouTube Transcript & Notes", layout="wide")

st.title("🎬 YouTube Transcript & Notes Generator")

st.markdown("""
### Welcome to the YouTube Transcript & Notes Generator!
- Navigate to the **Transcription** or **Summarization** pages from the sidebar.
- Extract and summarize YouTube video transcripts.
- Chat with the AI to understand key points.
""")

st.sidebar.success("Select a page from the sidebar.")
