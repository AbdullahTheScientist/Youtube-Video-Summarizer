import streamlit as st
import google.generativeai as genai
import os
import pyperclip
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi

# Load API Key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

st.title("📝 Summarize YouTube Videos")

# Initialize session state
if "summary" not in st.session_state:
    st.session_state["summary"] = None

if "transcript" not in st.session_state:
    st.session_state["transcript"] = None

youtube_link = st.text_input("Enter YouTube Video Link:")

words = st.sidebar.number_input("Summary length in words:", min_value=100, max_value=1000, value=100, step=1)

def extract_transcript(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = " ".join([i["text"] for i in transcript_text])
        return transcript
    except Exception as e:
        st.error(f"Error fetching transcript: {e}")
        return None

def generate_summary(transcript_text, words):
    prompt = f"""
    Summarize the given transcript into {words} words, highlighting key points.
    """
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + transcript_text)
    return response.text

if st.button("Summarise Video"):
    if youtube_link:
        transcript_text = extract_transcript(youtube_link)
        if transcript_text:
            summary = generate_summary(transcript_text, words)
            st.session_state["summary"] = summary

# Display summary
if st.session_state["summary"]:
    st.markdown("## Detailed Notes:")
    st.text_area("Summary", st.session_state["summary"], height=200)
    # Copy button
    if st.button("Copy Summary"):
        pyperclip.copy(st.session_state["summary"])
        st.success("Summary copied to clipboard!")
# Chatbot
st.markdown("## 🤖 Chat with AI")

user_input = st.text_input("Ask a question about the summary:")

if st.button("Ask"):
    if user_input and st.session_state["summary"]:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(f"Answer based on the summary: {st.session_state['summary']} \n\nUser: {user_input}")

        # Display only the latest response
        st.markdown(f"**You:** {user_input}")
        st.markdown(f"**AI:** {response.text}")





# You can also include a chat section or other functionality as needed.
