import streamlit as st
import json
import os
from elevenlabs import generate, play, voices
from typing import List

# Function to load API keys from a file
def load_api_keys_from_file() -> List[str]:
    try:
        with open("api_keys.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return [""] * 5

# Function to save API keys to a file
def save_api_keys_to_file(api_keys: List[str]):
    with open("api_keys.json", "w") as f:
        json.dump(api_keys, f)

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

# Load API keys either from file or start with empty ones
if 'streamlit' not in os.getcwd() and os.path.exists("api_keys.json"):
    initial_api_keys = load_api_keys_from_file()
else:
    initial_api_keys = [""] * 5

# Sidebar for API key input
api_key_labels = [f"API Key {i+1}" for i in range(5)]
api_keys = [st.sidebar.text_input(label, value=initial_api_keys[i]) for i, label in enumerate(api_key_labels)]
marked_keys = st.session_state.get("marked_keys", [False]*5)

# Save API keys if not on Streamlit's cloud
if 'streamlit' not in os.getcwd():
    save_api_keys_to_file(api_keys)

# Manual API key selection
options = ["NONE"] + [f"API Key {i+1}" for i in range(5)]
selected_api_option = st.sidebar.selectbox("Manually select an API Key", options, index=0)

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

used_api_key = "NONE"  # Default as NONE

if st.button('SPEAK') and user_input:
    generated = False

    # Use manually selected API key if it's valid and not "NONE"
    if selected_api_option != "NONE":
        api_idx = options.index(selected_api_option) - 1
        if api_keys[api_idx] and not marked_keys[api_idx]:
            audio = get_audio(user_input, selected_voice, selected_model, api_keys[api_idx])
            if audio:
                st.audio(audio, format='audio/wav', autoplay=True)
                generated = True
                used_api_key = selected_api_option
            else:
                marked_keys[api_idx] = True

    # If manually selected API key failed or wasn't valid, or if "NONE" was selected, try the rest
    if not generated:
        for idx, api_key in enumerate(api_keys):
            if api_key and not marked_keys[idx]:
                audio = get_audio(user_input, selected_voice, selected_model, api_key)
                if audio:
                    st.audio(audio, format='audio/wav', autoplay=True)
                    generated = True
                    used_api_key = f"API Key {idx+1}"
                    break
                else:
                    marked_keys[idx] = True

    # If no valid API keys or they all failed
    if not generated:
        st.warning("No API key provided or all provided keys are exhausted. Cannot generate audio.")

    # Print the API key that was used
    st.write(f"Audio generated using: {used_api_key}")

# Store marked keys to session state
st.session_state["marked_keys"] = marked_keys
