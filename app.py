import os
import requests
import streamlit as st
from gtts import gTTS
from tempfile import NamedTemporaryFile

# Function to generate text using Hugging Face's Inference API
def generate_script_hf(prompt, genre, max_tokens=300):
    """Generates a movie script snippet using Hugging Face's hosted LLaMA model."""
    api_key = os.getenv("HF_API_KEY")
    if not api_key:
        raise ValueError("Hugging Face API key not found. Set it as HF_API_KEY environment variable.")
    
    # Add a genre-specific prefix to the prompt
    genre_prompts = {
        "Action": "Write an intense and fast-paced action scene:",
        "Comedy": "Write a funny and humorous scene:",
        "Romance": "Write a romantic and heartfelt scene:",
        "Horror": "Write a spooky and suspenseful horror scene:",
        "Sci-Fi": "Write a futuristic science fiction scene:",
        "Drama": "Write an emotional and dramatic scene:"
    }
    genre_prefix = genre_prompts.get(genre, "Write a scene:")
    full_prompt = f"{genre_prefix} {prompt}"
    
    # API endpoint and parameters
    model = "meta-llama/Llama-2-7b-chat-hf"  # Replace with your chosen LLaMA model on Hugging Face
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {
        "inputs": full_prompt,
        "parameters": {
            "max_new_tokens": max_tokens,
            "temperature": 0.7,
            "stop": ["SCENE", "\n\n"]
        }
    }
    
    response = requests.post(
        f"https://api-inference.huggingface.co/models/{model}",
        headers=headers,
        json=payload
    )
    
    if response.status_code != 200:
        raise ValueError(f"Error from Hugging Face API: {response.text}")
    
    result = response.json()
    return result.get("generated_text", "No text generated")

# Function to convert text to audio using gTTS
def text_to_audio(text):
    """Converts the provided text to an audio file using gTTS."""
    tts = gTTS(text, lang='en')
    temp_audio = NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp_audio.name)
    return temp_audio.name

# Streamlit App
st.title("Decentralized Autonomous Movie Creation System")

# Section 1: Script Generation
st.header("AI-Powered Script Generator")
prompt = st.text_area("Enter a prompt for the movie script:")
genre = st.selectbox("Select Movie Genre", ["Action", "Comedy", "Romance", "Horror", "Sci-Fi", "Drama"])
max_tokens = st.slider("Select the script length (tokens):", min_value=100, max_value=1000, value=300)

if st.button("Generate Script"):
    try:
        script_snippet = generate_script_hf(prompt, genre, max_tokens=max_tokens)
        st.subheader("Generated Script:")
        st.text_area("Script:", value=script_snippet, height=300)
        
        # Convert script to audio
        audio_file = text_to_audio(script_snippet)
        with open(audio_file, "rb") as audio:
            st.download_button("Download Audio File", audio, file_name="script_audio.mp3", mime="audio/mp3")
        
        # Clean up the temporary audio file
        os.remove(audio_file)
    except Exception as e:
        st.error(f"Error: {e}")
