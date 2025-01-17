import streamlit as st
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import requests

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

def fetch_talent_from_rapidapi(skills):
    """Fetch talent using a RapidAPI endpoint."""
    if not skills:
        return "Please select at least one skill to find talent."
    
    url = "https://indeed-indeed.p.rapidapi.com/apisearch?v=2&format=json&q=java&l=austin%2C%20tx&radius=25"
    headers = {
        "X-RapidAPI-Key": "29fbaab46cmsh500e2d10f5c50cdp14494cjsn004af6732618",  # Replace with your RapidAPI key
        "X-RapidAPI-Host": "indeed-indeed.p.rapidapi.com"
    }
    querystring = {
        "skills": ",".join(skills),  # Join the skills list as a comma-separated string
        "location": "global",       # Add location filtering if applicable
        "limit": "10"               # Limit the number of results
    }
    
    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
        data = response.json()
        return data.get("talent", [])  # Assuming API returns a list of talents under "talent"
    except requests.RequestException as e:
        st.error(f"Error fetching talent: {e}")
        return []

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

# Section 2: Talent Matchmaking with RapidAPI
st.header("Talent Matchmaking via RapidAPI")
skills_list = ["Acting", "Directing", "Editing", "Animation", "VFX", "Voiceover"]
required_skills = st.multiselect("Select required skills:", skills_list)
if st.button("Find Talent"):
    talents = fetch_talent_from_rapidapi(required_skills)
    if isinstance(talents, str):
        st.warning(talents)
    elif talents:
        st.subheader("Matched Talent:")
        for talent in talents:
            st.write(f"- **{talent['name']}** ({', '.join(talent['skills'])}) [Portfolio]({talent['portfolio_url']})")
    else:
        st.warning("No matching talent found. Try selecting different skills.")
