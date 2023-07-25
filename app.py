import streamlit as st
import json
import os
from elevenlabs import generate, play, voices

# Function to load API key from a file
def load_api_key_from_file() -> str:
    try:
        with open("api_key.json", "r") as f:
            return json.load(f).get('api_key', "")
    except FileNotFoundError:
        return ""

# Function to save API key to a file
def save_api_key_to_file(api_key: str):
    with open("api_key.json", "w") as f:
        json.dump({'api_key': api_key}, f)

# Function to generate audio
def get_audio(text, voice="Bella", model="eleven_monolingual_v1", api_key=None):
    try:
        audio = generate(text=text, voice=voice, model=model, api_key=api_key)
        return audio
    except Exception as e:
        st.warning(f"Error: {str(e)}")
        return None

# Display app title
st.title('ElevenLabs Audio Generator')

# Load API key either from file or start with an empty one
if 'streamlit' not in os.getcwd() and os.path.exists("api_key.json"):
    initial_api_key = load_api_key_from_file()
else:
    initial_api_key = ""

# Sidebar for API key input
api_key = st.sidebar.text_input("API Key", value=initial_api_key)

# Save API key if not on Streamlit's cloud
if 'streamlit' not in os.getcwd():
    save_api_key_to_file(api_key)

# Model selection dropdown
model_mapping = {
    'monolingual': 'eleven_monolingual_v1',
    'multilingual': 'eleven_multilingual_v1'
}
selected_model_name = st.selectbox("Select a model:", list(model_mapping.keys()))
selected_model = model_mapping[selected_model_name]

# Display the dropdown for voices
voice_list = ["Rachel", "Domi", "Bella", "Antoni", "Elli", "Josh", "Arnold", "Adam", "Sam"]
selected_voice = st.selectbox('Select a voice:', voice_list)

user_input = st.text_area('Enter/Paste your text here:', height=200)

if st.button('SPEAK') and user_input:
    audio = get_audio(user_input, selected_voice, selected_model, api_key or None)
    
    if audio:
        st.audio(audio, format='audio/wav', autoplay=True)
        if api_key:
            st.write(f"Audio generated using the provided API key.")
        else:
            st.write(f"Audio generated without an API key.")
    else:
        st.warning("Cannot generate audio. Please check the API key or try again.")
