import streamlit as st
from groq import Groq
from gtts import gTTS
import os
import io

from dotenv import load_dotenv
load_dotenv()
# Initialize Groq Client
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

def transcribe_audio(audio_bytes):
    """Convert audio to text using Groq Whisper."""
    # Whisper requires a named file-like object
    audio_file = io.BytesIO(audio_bytes)
    audio_file.name = "input.wav" 
    
    transcription = client.audio.transcriptions.create(
        file=audio_file,
        model="whisper-large-v3",
        response_format="text"
    )
    return transcription

def generate_ai_response(text_input):
    """Get a response from Llama 3 using Groq."""
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": text_input}],
        model="llama-3.3-70b-versatile",
    )
    return chat_completion.choices[0].message.content

def text_to_speech(text):
    """Convert AI response text to audio."""
    tts = gTTS(text=text, lang='en')
    tts.save("response.mp3")
    return "response.mp3"

# --- Streamlit UI ---
st.title("🎙️ Gen-AI Voice Assistant")
st.write("Powered by **Groq** for lightning-fast inference.")

# 1. Capture Voice
audio_data = st.audio_input("Speak to your assistant")

if audio_data:
    with st.spinner("Processing..."):
        # 2. Transcription (STT)
        user_text = transcribe_audio(audio_data.getvalue())
        st.info(f"You said: {user_text}")

        # 3. Reasoning (LLM)
        ai_response = generate_ai_response(user_text)
        st.success(f"AI: {ai_response}")

        # 4. Voice Generation (TTS)
        audio_file_path = text_to_speech(ai_response)
        
        # 5. Playback
        st.audio(audio_file_path, format="audio/mp3", autoplay=True)