import streamlit as st
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import requests
import json

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
def fetch_talent_from_rapidapi(resume_data=None, resume_url=None, language="en"):
    """Fetch talent using the LinkedIn and Resume Analyzer API."""
    if not resume_data and not resume_url:
        return "Please provide either resume data or a resume URL."
    
    url = "https://professional-linkedin-and-resume-analyzer.p.rapidapi.com/generate-summary"
    headers = {
        "Content-Type": "application/json",
        "x-rapidapi-host": "professional-linkedin-and-resume-analyzer.p.rapidapi.com",
        "x-rapidapi-key": "29fbaab46cmsh500e2d10f5c50cdp14494cjsn004af6732618"  # Replace with your RapidAPI key
    }
    
    # Prepare the data to be sent in the POST request
    data = {
        "resumeData": resume_data,
        "resumeUrl": resume_url,
        "language": language
    }
    
    # Make the POST request to the API
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Raise an error for bad status codes
        result = response.json()
        
        # Extract and return relevant talent information from the response
        talent_summary = result.get("summary", "No summary found.")
        return talent_summary
    
    except requests.RequestException as e:
        st.error(f"Error fetching talent: {e}")
        return "Error fetching talent."

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

# Section 2: Talent Matchmaking with LinkedIn and Resume Analyzer API
st.header("Talent Matchmaking via LinkedIn and Resume Analyzer API")
resume_data = st.text_area("Enter resume data here (or provide a URL below):")
resume_url = st.text_input("Or provide a resume URL:")

if st.button("Find Talent"):
    talent_summary = fetch_talent_from_rapidapi(resume_data=resume_data, resume_url=resume_url)
    if talent_summary == "Please provide either resume data or a resume URL.":
        st.warning(talent_summary)
    else:
        st.subheader("Talent Summary:")
        st.write(talent_summary)
