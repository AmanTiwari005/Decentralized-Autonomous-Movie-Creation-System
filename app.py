import os
import openai
import streamlit as st
import re
from gtts import gTTS
from tempfile import NamedTemporaryFile

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to generate script using GPT-4
def generate_script(prompt, genre, max_tokens=1000):
    """Generates a meaningful movie script snippet based on the given prompt and genre using GPT-4."""
    if not prompt.strip():
        return "Please provide a valid prompt."
    
    # Adjust the prompt based on the selected genre
    genre_prompts = {
        "Action": "Write an intense and fast-paced action scene where ",
        "Comedy": "Create a funny scene that involves a humorous misunderstanding where ",
        "Romance": "Write a heartfelt romantic scene where ",
        "Horror": "Create a spooky and suspenseful horror scene where ",
        "Sci-Fi": "Write a futuristic science fiction scene where ",
        "Drama": "Create a deep emotional drama scene where "
    }
    
    genre_prompt = genre_prompts.get(genre, "")
    full_prompt = genre_prompt + prompt

    try:
        # Call GPT-4
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a scriptwriter AI specialized in creating movie scripts."},
                {"role": "user", "content": full_prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.7,
        )
        
        script = response['choices'][0]['message']['content'].strip()
        return script
    except Exception as e:
        return f"Error generating script: {str(e)}"

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
max_tokens = st.slider("Select the script length (tokens):", min_value=300, max_value=1500, value=1000)

if st.button("Generate Script"):
    script_snippet = generate_script(prompt, genre, max_tokens=max_tokens)
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
