import os
import streamlit as st
from dotenv import load_dotenv
import re
from gtts import gTTS
from tempfile import NamedTemporaryFile
from transformers import AutoModelForCausalLM, AutoTokenizer

# Load environment variables (e.g., for API keys, etc.)
load_dotenv()

# Load API keys
huggingface_api_key = os.getenv("HUGGINGFACEHUB_API_TOKEN")
if not huggingface_api_key:
    raise ValueError("HUGGINGFACE_API_KEY not found in environment variables.")

# Initialize Hugging Face model (OPT model)
model_name = "facebook/opt-125m"  # Smaller model
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

def generate_script(prompt, genre, max_length=1000):
    """Generates a meaningful movie script snippet based on the given prompt and genre using the OPT model."""
    if not prompt.strip():
        return "Please provide a valid prompt."
    
    # Define genre-specific instructions
    genre_prompts = {
        "Action": "Write an intense and fast-paced action movie scene.",
        "Comedy": "Write a humorous and lighthearted comedy scene.",
        "Romance": "Write a heartfelt and emotional romantic scene.",
        "Horror": "Write a suspenseful and spooky horror movie scene.",
        "Sci-Fi": "Write a futuristic science fiction scene.",
        "Drama": "Write a deep and emotionally charged drama scene."
    }
    
    # Combine genre instructions and user prompt
    full_prompt = f"{genre_prompts.get(genre, '')} {prompt}"
    
    # Encode the input prompt and generate the response using the OPT model
    inputs = tokenizer(full_prompt, return_tensors="pt")
    outputs = model.generate(inputs["input_ids"], max_length=max_length, num_return_sequences=1)
    
    # Decode the output and clean up the generated script
    script = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
    if not script:
        return "Error: The model returned an empty response."
    
    return script

def enhance_script(script):
    """Enhances the script by adding structure like scene headers and dialogues."""
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

def text_to_audio(text):
    """Converts the provided text to an audio file using gTTS."""
    tts = gTTS(text, lang='en')
    temp_audio = NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp_audio.name)
    return temp_audio.name

# Streamlit App
st.title("Decentralized Autonomous Movie Creation System")

st.header("AI-Powered Script Generator")
prompt = st.text_area("Enter a prompt for the movie script:")
genre = st.selectbox("Select Movie Genre", ["Action", "Comedy", "Romance", "Horror", "Sci-Fi", "Drama"])
max_length = st.slider("Select the script length (tokens):", min_value=300, max_value=1500, value=1000)

if st.button("Generate Script"):
    script_snippet = generate_script(prompt, genre, max_length=max_length)
    if "Error" in script_snippet:
        st.warning(script_snippet)
    else:
        enhanced_snippet = enhance_script(script_snippet)
        st.subheader("Generated Script:")
        st.text_area("Enhanced Script:", value=enhanced_snippet, height=400)

        st.subheader("Audio Version of the Script:")
        audio_file = text_to_audio(enhanced_snippet)
        with open(audio_file, "rb") as audio:
            st.download_button("Download Audio File", audio, file_name="script_audio.mp3", mime="audio/mp3")

        os.remove(audio_file)
