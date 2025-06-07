import streamlit as st
import librosa
import soundfile as sf
import os
import tempfile

st.set_page_config(page_title="Audio Speed Adjuster", page_icon="🎧")
st.title("🎧 Audio Speed Adjuster (Pitch Preserved)")

uploaded_file = st.file_uploader("Upload an audio file", type=["wav", "mp3"])

speed = st.slider("Adjust Speed (0.5x to 2.0x)", 0.5, 2.0, 1.0, 0.1)

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_input:
        tmp_input.write(uploaded_file.read())
        tmp_input.flush()

        y, sr = librosa.load(tmp_input.name)
        y_stretched = librosa.effects.time_stretch(y, speed)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_output:
            sf.write(tmp_output.name, y_stretched, sr)
            st.audio(tmp_output.name, format='audio/wav')
            with open(tmp_output.name, "rb") as f:
                st.download_button("Download Processed Audio", f, file_name="adjusted_audio.wav")
