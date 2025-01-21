import streamlit as st
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import re
from gtts import gTTS
import os
from tempfile import NamedTemporaryFile

# Load the AI Model
@st.cache_resource
def load_model():
    model_name = "gpt2"
    model = GPT2LMHeadModel.from_pretrained(model_name)
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    return model, tokenizer

model, tokenizer = load_model()

# Function to generate script based on prompt
def generate_script(prompt, max_length=1000):
    """Generates a meaningful movie script snippet based on the given prompt."""
    if not prompt.strip():
        return "Please provide a valid prompt."
    inputs = tokenizer.encode(prompt, return_tensors="pt")
    outputs = model.generate(
        inputs,
        max_length=max_length,
        num_return_sequences=1,
        no_repeat_ngram_size=3,
        temperature=0.8,
        top_p=0.95,
        top_k=50,
        do_sample=True
    )
    script = tokenizer.decode(outputs[0], skip_special_tokens=True)
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
max_length = st.slider("Select the script length (tokens):", min_value=300, max_value=1500, value=1000)

if st.button("Generate Script"):
    script_snippet = generate_script(prompt, max_length=max_length)
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

# Section 2: Genre-Specific Script Templates (optional)
st.header("Generate Scripts from Templates")
genres = ["action", "romance", "comedy"]
genre = st.selectbox("Choose a Genre", genres)

genre_scripts = {
    "action": """
INT. ABANDONED WAREHOUSE - NIGHT

The camera pans across a dimly lit warehouse filled with crates and flickering fluorescent lights. 
Suddenly, JACKSON (30s, rugged and determined) bursts through the door, gun in hand.

JACKSON: (whispering to himself) They thought they could hide here.

From the shadows, a gang of masked men appear, led by MARCUS (40s, calm and menacing).

MARCUS: (smirking) You’re brave, Jackson. But bravery only gets you so far.

Cue an intense fight sequence: punches, gunfire, and high-octane stunts. Jackson takes down the gang one by one.
""",
    "romance": """
EXT. PARK - SUNSET

EMILY (20s, shy but warm-hearted) sits on a bench, sketching in her notebook. JAMES (30s, charming but hesitant) approaches nervously.

JAMES: (clears throat) Mind if I sit here?

EMILY: (smiling) It’s a free country.

They share a laugh. A breeze carries a page from Emily’s notebook, and James catches it. It’s a sketch of him.

JAMES: (teasing) Is this me?

EMILY: (blushing) I... uh, it might be.

They lock eyes, and the world around them seems to fade.
""",
    "comedy": """
INT. OFFICE BREAK ROOM - DAY

The office is quiet except for the hum of the vending machine. LARRY (30s, clumsy and eccentric) tries to wrestle a bag of chips stuck in the machine.

LARRY: (grunting) Come on, you overpriced snack! Don’t make me look bad.

KAREN (40s, sarcastic and sharp) walks in, holding her coffee.

KAREN: Too late for that, Larry.

Suddenly, the machine spits out three bags of chips, hitting Larry in the face. He stumbles, spilling Karen’s coffee.

KAREN: (deadpan) Great. Now I need another coffee... and a new coworker.
""",
}

# Section 3: Genre-Specific Script Generation
if st.button(f"Generate {genre} Script"):
    st.subheader(f"{genre.capitalize()} Script:")
    st.text_area(f"{genre.capitalize()} Script Snippet:", value=genre_scripts[genre], height=200)
