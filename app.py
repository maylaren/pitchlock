import streamlit as st
import librosa
import soundfile as sf
import tempfile
import os

st.set_page_config(page_title="Audio Speed Adjuster", page_icon="🎧")
st.title("🎧 Audio Speed Adjuster")
st.markdown("Upload an audio file and change its playback speed **without changing the pitch**.")

# Upload audio file
uploaded_file = st.file_uploader("Choose an audio file", type=["wav", "mp3"])

# Speed slider
speed = st.slider("Adjust Speed", min_value=0.5, max_value=2.0, value=1.0, step=0.1)

if uploaded_file is not None:
    # Save uploaded file to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_input:
        temp_input.write(uploaded_file.read())
        temp_input_path = temp_input.name

    # Load audio with librosa
    try:
        y, sr = librosa.load(temp_input_path)
    except Exception as e:
        st.error(f"Error loading audio: {e}")
        os.remove(temp_input_path)
        st.stop()

    # Time-stretch without changing pitch
    try:
        y_stretched = librosa.effects.time_stretch(y, speed)
    except Exception as e:
        st.error(f"Error adjusting speed: {e}")
        os.remove(temp_input_path)
        st.stop()

    # Save processed audio to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_output:
        sf.write(temp_output.name, y_stretched, sr)
        temp_output_path = temp_output.name

    # Playback and download
    st.audio(temp_output_path, format="audio/wav")
    with open(temp_output_path, "rb") as f:
        st.download_button(
            label="Download Adjusted Audio",
            data=f,
            file_name="adjusted_audio.wav",
            mime="audio/wav"
        )

    # Clean up
    os.remove(temp_input_path)
    # Do not delete output until download is complete
