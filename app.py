import streamlit as st
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import re

# Load the AI Model
@st.cache_resource
def load_model():
    model_name = "gpt2"
    model = GPT2LMHeadModel.from_pretrained(model_name)
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    return model, tokenizer

model, tokenizer = load_model()

def generate_script(prompt, max_length=600):
    """Generates a longer movie script snippet based on the given prompt."""
    if not prompt.strip():
        return "Please provide a valid prompt."
    inputs = tokenizer.encode(prompt, return_tensors="pt")
    outputs = model.generate(inputs, max_length=max_length, num_return_sequences=1, no_repeat_ngram_size=2, temperature=0.7)
    script = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return script

# Extract skills/roles from the generated script
def extract_skills_from_script(script):
    """Extract possible skills/roles from the movie script."""
    roles_list = ["Acting", "Directing", "Editing", "Animation", "VFX", "Voiceover"]
    found_roles = []

    # Search for keywords in the script (simplified, can be expanded with more advanced NLP)
    for role in roles_list:
        if re.search(r'\b' + re.escape(role) + r'\b', script, re.IGNORECASE):
            found_roles.append(role)

    return found_roles

# Streamlit App
st.title("Decentralized Autonomous Movie Creation System")

# Section 1: Script Generation
st.header("AI-Powered Script Generator")
prompt = st.text_area("Enter a prompt for the movie script:")
max_length = st.slider("Select the script length (tokens):", min_value=300, max_value=1000, value=600)

if st.button("Generate Script"):
    script_snippet = generate_script(prompt, max_length=max_length)
    if script_snippet == "Please provide a valid prompt.":
        st.warning(script_snippet)
    else:
        st.subheader("Generated Script:")
        st.write(script_snippet)

        # Extract skills/roles from the generated script
        extracted_skills = extract_skills_from_script(script_snippet)
        
        if extracted_skills:
            st.subheader("Extracted Skills/Roles:")
            st.write(", ".join(extracted_skills))
        else:
            st.warning("No relevant skills or roles found in the script.")
