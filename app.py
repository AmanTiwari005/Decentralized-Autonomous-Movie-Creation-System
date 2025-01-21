import os
import streamlit as st
import re
from gtts import gTTS
from tempfile import NamedTemporaryFile
from langchain_groq import ChatGroq  

# Function to initialize the Groq model
def init_groq_model():
    groq_api_key = os.getenv('GROQ_API_KEY')
    if not groq_api_key:
        raise ValueError("GROQ_API_KEY not found in environment variables.")
    return ChatGroq(
        groq_api_key=groq_api_key, model_name="llama-3.1-70b-versatile", temperature=0.2
    )

# Initialize the Groq model
groq_model = init_groq_model()

# Function to generate script based on prompt and genre using Groq (Llama model)
def generate_script(prompt, genre, max_length=1000):
    """Generates a meaningful movie script snippet based on the given prompt and genre using Groq."""
    if not prompt.strip():
        return "Please provide a valid prompt."
    
    # Adjust the prompt based on the selected genre
    genre_prompts = {
        "Action": "Create an intense and fast-paced action scene where ",
        "Comedy": "Write a funny scene that involves a humorous misunderstanding where ",
        "Romance": "Write a heartfelt romantic scene where ",
        "Horror": "Write a spooky and suspenseful horror scene where ",
        "Sci-Fi": "Create a futuristic science fiction scene where ",
        "Drama": "Write a deep emotional drama scene where "
    }
    
    genre_prompt = genre_prompts.get(genre, "")
    full_prompt = genre_prompt + prompt
    
    # Format the prompt into a conversation-style input (list of message dicts)
    messages = [{"role": "user", "content": full_prompt}]
    
    # Query the Groq model using the correct method
    response = groq_model.generate(messages, max_length=max_length)  # Pass formatted messages
    script = response['generated_text'].strip()  # Extract generated text
    
    return script

# Function to enhance the script with formatting and structure
def enhance_script(script):
    """Enhances the script by adding basic structure like scene headers and dialogues."""
    scenes = script.split("\n\n")
    enhanced_script = ""
    for i, scene in enumerate(scenes):
        enhanced_script += f"SCENE {i+1}:\n"
        sentences = re.split(r'(?<=[.!?]) +', scene)
        for sentence in sentences:
            if sentence.strip():
                enhanced_script += f"    {sentence.strip()}\n"
        enhanced_script += "\n"
    return enhanced_script

# Function to convert text to audio using gTTS
def text_to_audio(text):
    """Converts the provided text to an audio file using gTTS."""
    tts = gTTS(text, lang='en')
    # Save audio to a temporary file
    temp_audio = NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp_audio.name)
    return temp_audio.name

# Streamlit App
st.title("Decentralized Autonomous Movie Creation System")

# Section 1: Script Generation
st.header("AI-Powered Script Generator")
prompt = st.text_area("Enter a prompt for the movie script:")
genre = st.selectbox("Select Movie Genre", ["Action", "Comedy", "Romance", "Horror", "Sci-Fi", "Drama"])
max_length = st.slider("Select the script length (tokens):", min_value=300, max_value=1500, value=1000)

if st.button("Generate Script"):
    script_snippet = generate_script(prompt, genre, max_length=max_length)
    if script_snippet == "Please provide a valid prompt.":
        st.warning(script_snippet)
    else:
        enhanced_snippet = enhance_script(script_snippet)
        st.subheader("Generated Script:")
        st.text_area("Enhanced Script:", value=enhanced_snippet, height=400)

        # Convert script to audio
        st.subheader("Audio Version of the Script:")
        audio_file = text_to_audio(enhanced_snippet)

        # Provide download link for the audio file
        with open(audio_file, "rb") as audio:
            st.download_button("Download Audio File", audio, file_name="script_audio.mp3", mime="audio/mp3")

        # Clean up the temporary audio file
        os.remove(audio_file)
