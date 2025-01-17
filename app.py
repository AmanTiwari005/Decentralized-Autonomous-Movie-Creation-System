import streamlit as st
from transformers import GPT2LMHeadModel, GPT2Tokenizer

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
    inputs = tokenizer.encode(prompt, return_tensors="pt")
    outputs = model.generate(inputs, max_length=max_length, num_return_sequences=1, no_repeat_ngram_size=2)
    script = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return script

# Talent Pool
class Talent:
    def __init__(self, name, portfolio_url, skills):
        self.name = name
        self.portfolio_url = portfolio_url
        self.skills = skills

    def __repr__(self):
        return f"{self.name} - {self.skills}"

talent_pool = [
    Talent("Alice", "https://portfolio.alice.com", ["Acting", "Voiceover"]),
    Talent("Bob", "https://portfolio.bob.com", ["Directing", "Editing"]),
    Talent("Charlie", "https://portfolio.charlie.com", ["Animation", "VFX"]),
]

def match_talent(required_skills, talent_pool):
    """Matches talent based on required skills."""
    matches = [talent for talent in talent_pool if any(skill in talent.skills for skill in required_skills)]
    return matches

# Streamlit App
st.title("Decentralized Autonomous Movie Creation System")

# Section 1: Script Generation
st.header("AI-Powered Script Generator")
prompt = st.text_area("Enter a prompt for the movie script:")
if st.button("Generate Script"):
    if prompt:
        script_snippet = generate_script(prompt)
        st.subheader("Generated Script:")
        st.write(script_snippet)
    else:
        st.warning("Please enter a prompt to generate a script.")

# Section 2: Talent Matchmaking
st.header("Talent Matchmaking")
required_skills = st.multiselect("Select required skills:", ["Acting", "Directing", "Editing", "Animation", "VFX", "Voiceover"])
if st.button("Find Talent"):
    matches = match_talent(required_skills, talent_pool)
    if matches:
        st.subheader("Matched Talent:")
        for match in matches:
            st.write(f"- **{match.name}** ({', '.join(match.skills)}) [Portfolio]({match.portfolio_url})")
    else:
        st.warning("No matching talent found. Try selecting different skills.")
