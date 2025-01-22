
import os
import streamlit as st
from dotenv import load_dotenv
import re
from gtts import gTTS
from tempfile import NamedTemporaryFile
from langchain_groq import ChatGroq  

load_dotenv()
# Initialize GROQ chat model
def init_groq_model():
    groq_api_key = os.getenv('GROQ_API_KEY')
    if not groq_api_key:
        raise ValueError("GROQ_API_KEY not found in environment variables.")
    return ChatGroq(
        groq_api_key=groq_api_key, model_name="llama-3.1-70b-versatile", temperature=0.2
    )
llm_groq = init_groq_model()

def generate_script(prompt, genre, max_length=1000):
    """Generates a meaningful movie script snippet based on the given prompt and genre using Groq."""
    if not prompt.strip():
        return "Please provide a valid prompt."

    genre_prompts = {
        "Action": "Write an intense and fast-paced action scene where ",
        "Comedy": "Write a humorous scene involving a misunderstanding where ",
        "Romance": "Write a heartfelt romantic moment where ",
        "Horror": "Write a spooky and suspenseful horror moment where ",
        "Sci-Fi": "Write a futuristic science fiction sequence where ",
        "Drama": "Write a deep emotional drama moment where ",
    }

    genre_prompt = genre_prompts.get(genre, "")
    full_prompt = genre_prompt + prompt

    # Test with a variety of roles or without a role
    possible_roles = ["user", "assistant", "system", None]

    for role in possible_roles:
        try:
            messages = [{"role": role, "content": full_prompt}] if role else [{"content": full_prompt}]
            print(f"Debugging messages (role={role}):", messages)

            # Generate script using the Groq model
            response = llm_groq.generate(messages, max_length=max_length)
            print("Groq Response:", response)

            script = response.get('generated_text', '').strip()
            if script:
                return script
            else:
                raise ValueError("The model did not generate a response. Trying the next role...")
        except TypeError as e:
            print(f"TypeError with role={role}: {e}. Trying the next role...")
        except Exception as e:
            print(f"Error with role={role}: {e}. Trying the next role...")

    return "All attempts failed. Please check the Groq API documentation or contact support."


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
