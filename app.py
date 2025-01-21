import os
import streamlit as st
from gtts import gTTS
from tempfile import NamedTemporaryFile
from llama_cpp import Llama  # Import LLaMA model support

# Function to initialize the LLaMA model
@st.cache_resource
def init_llama_model():
    model_path = os.getenv('LLAMA_MODEL_PATH', 'llama-3b.ggmlv3.q4_0.bin')  # Path to your LLaMA model file
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"LLaMA model file not found at {model_path}. Please set LLAMA_MODEL_PATH.")
    return Llama(model_path=model_path, n_ctx=2048)

# Initialize the LLaMA model
llama_model = init_llama_model()

# Function to generate script based on prompt and genre using LLaMA
def generate_script(prompt, genre, max_tokens=300):
    """Generates a meaningful movie script snippet based on the given prompt and genre using LLaMA."""
    if not prompt.strip():
        return "Please provide a valid prompt."
    
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
    
    # Generate text with LLaMA
    output = llama_model(full_prompt, max_tokens=max_tokens, stop=["SCENE", "\n\n"])
    return output["choices"][0]["text"].strip()

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
    script_snippet = generate_script(prompt, genre, max_tokens=max_tokens)
    st.subheader("Generated Script:")
    st.text_area("Script:", value=script_snippet, height=300)
    
    # Convert script to audio
    audio_file = text_to_audio(script_snippet)
    with open(audio_file, "rb") as audio:
        st.download_button("Download Audio File", audio, file_name="script_audio.mp3", mime="audio/mp3")

    # Clean up the temporary audio file
    os.remove(audio_file)
