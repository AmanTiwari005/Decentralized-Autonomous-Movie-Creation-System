import streamlit as st
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import requests
import json
import re

# Load the AI Model
@st.cache_resource
def load_model():
    model_name = "gpt2"
    model = GPT2LMHeadModel.from_pretrained(model_name)
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    return model, tokenizer

model, tokenizer = load_model()

def generate_script(prompt, max_length=300):
    """Generates a movie script snippet based on the given prompt."""
    if not prompt.strip():
        return "Please provide a valid prompt."
    inputs = tokenizer.encode(prompt, return_tensors="pt")
    outputs = model.generate(inputs, max_length=max_length, num_return_sequences=1, no_repeat_ngram_size=2)
    script = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return script

# Function to fetch talent using LinkedIn and Resume Analyzer API
def fetch_talent_from_rapidapi(skills, language="en"):
    """Fetch talent based on the extracted skills from the script using the LinkedIn and Resume Analyzer API."""
    if not skills:
        return "Please select at least one skill to find talent."

    url = "https://professional-linkedin-and-resume-analyzer.p.rapidapi.com/generate-summary"
    headers = {
        "Content-Type": "application/json",
        "x-rapidapi-host": "professional-linkedin-and-resume-analyzer.p.rapidapi.com",
        "x-rapidapi-key": "29fbaab46cmsh500e2d10f5c50cdp14494cjsn004af6732618"  # Replace with your RapidAPI key
    }
    
    # Prepare the data to be sent in the POST request (dummy data for the moment)
    data = {
        "resumeData": "",  # Would be fetched dynamically later
        "resumeUrl": "",   # Could also be dynamically handled
        "language": language
    }

    # Placeholder: Actual implementation would use skills to create resumes or data matching
    # For now, return skills as talent matched
    return skills

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
if st.button("Generate Script"):
    script_snippet = generate_script(prompt)
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

            # Use the extracted skills to fetch talent
            talents = fetch_talent_from_rapidapi(extracted_skills)
            if isinstance(talents, str):
                st.warning(talents)
            else:
                st.subheader("Matched Talent:")
                for talent in talents:
                    st.write(f"- **{talent}**")  # Displaying skill as talent for now
        else:
            st.warning("No relevant skills or roles found in the script.")

