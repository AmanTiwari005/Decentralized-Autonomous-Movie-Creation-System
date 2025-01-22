import streamlit as st
import os
import pyttsx3
import re
from langchain_groq import ChatGroq  # Import Groq for LLaMA integration
from dotenv import load_dotenv


load_dotenv()
# Load API keys
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables.")

groq_model = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="llama-3.1-70b-versatile",  # Use the LLaMA model from Groq
    temperature=0.7
)

def generate_script(prompt, max_length=600):
    """Generates a movie script snippet using Groq LLaMA."""
    try:
        messages = [
            {"role": "system", "content": "You are a professional movie script writer. Write creative, engaging, and detailed movie scripts."},
            {"role": "user", "content": prompt}
        ]
        response = groq_model.generate(messages, max_length=max_length)
        script = response.get('generated_text', '').strip()
        if not script:
            raise ValueError("The model returned an empty response.")
        return script
    except Exception as e:
        return f"Error generating script: {e}"

# Extract skills/roles from the generated script
def extract_skills_from_script(script):
    """Extract possible skills/roles from the movie script."""
    roles_list = ["Acting", "Directing", "Editing", "Animation", "VFX", "Voiceover"]
    found_roles = []
    for role in roles_list:
        if re.search(r'\b' + re.escape(role) + r'\b', script, re.IGNORECASE):
            found_roles.append(role)
    return found_roles

# Offline TTS with pyttsx3
def text_to_audio(text):
    """Converts the provided text to an audio file using pyttsx3."""
    engine = pyttsx3.init()
    temp_audio = "output_audio.mp3"
    engine.save_to_file(text, temp_audio)
    engine.runAndWait()
    return temp_audio

# Streamlit App
st.title("Decentralized Autonomous Movie Creation System")

# Section 1: Script Generation
st.header("AI-Powered Script Generator")
prompt = st.text_area("Enter a prompt for the movie script:")
max_length = st.slider("Select the script length (tokens):", min_value=300, max_value=1000, value=600)

if st.button("Generate Script"):
    script_snippet = generate_script(prompt, max_length=max_length)
    if "Error" in script_snippet:
        st.warning(script_snippet)
    else:
        st.subheader("Generated Script:")
        st.write(script_snippet)

        # Extract skills/roles
        extracted_skills = extract_skills_from_script(script_snippet)
        if extracted_skills:
            st.subheader("Extracted Skills/Roles:")
            st.write(", ".join(extracted_skills))
        else:
            st.warning("No relevant skills or roles found in the script.")
        
        # Convert script to audio
        st.subheader("Audio Version of the Script:")
        audio_file = text_to_audio(script_snippet)
        with open(audio_file, "rb") as audio:
            st.download_button("Download Audio File", audio, file_name="script_audio.mp3", mime="audio/mp3")
        os.remove(audio_file)
