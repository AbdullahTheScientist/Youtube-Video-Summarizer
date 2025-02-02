import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
import os
import pyperclip

from dotenv import load_dotenv

# Load API Key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

st.title("📜 YouTube Video Transcription")

# Initialize session state
if "transcript" not in st.session_state:
    st.session_state["transcript"] = None

youtube_link = st.text_input("Enter YouTube Video Link:")

def extract_transcript(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = " ".join([i["text"] for i in transcript_text])
        return transcript
    except Exception as e:
        st.error(f"Error fetching transcript: {e}")
        return None

if st.button("Get Transcript"):
    if youtube_link:
        transcript_text = extract_transcript(youtube_link)
        if transcript_text:
            st.session_state["transcript"] = transcript_text


# Display transcript
if st.session_state["transcript"]:
    st.markdown("## Video Transcript:")
    st.text_area("Transcript", st.session_state["transcript"], height=200)
    # Copy button
    if st.button("Copy Transcript"):
        pyperclip.copy(st.session_state["transcript"])
        st.success("Transcript copied to clipboard!")

# Chatbot
st.markdown("## 🤖 Chat with AI")

user_input = st.text_input("Ask a question about the transcript:")

if st.button("Ask"):
    if user_input and st.session_state["transcript"]:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(f"Answer based on the transcript: {st.session_state['transcript']} \n\nUser: {user_input}")
        
        # Display only the latest response
        st.markdown(f"**You:** {user_input}")
        st.markdown(f"**AI:** {response.text}")
