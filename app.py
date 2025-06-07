import streamlit as st
import librosa
import soundfile as sf
import numpy as np
import io

st.set_page_config(page_title="Audio Speed Adjuster", layout="centered")
st.title("🎧 Audio Speed Adjuster")
st.write("Upload an audio file to adjust its playback speed **without changing its pitch**.")

# Step 1: Upload
uploaded_file = st.file_uploader("Browse an audio file (.wav or .mp3)", type=["wav", "mp3"])

if uploaded_file is not None:
    # Step 2: Read and process the uploaded file
    st.info("Reading the audio file...")
    try:
        y, sr = librosa.load(uploaded_file, sr=None)
        st.success("Audio file loaded successfully!")

        # Step 3: Show slider to adjust speed
        speed = st.slider("🎚️ Choose Playback Speed (1.0 = Normal)", 0.5, 2.0, 1.0, 0.1)
        if speed != 1.0:
            y_stretched = librosa.effects.time_stretch(y, speed)
        else:
            y_stretched = y

        # Step 4: Allow user to listen to adjusted audio
        st.markdown("### ▶️ Preview Adjusted Audio")
        buf = io.BytesIO()
        sf.write(buf, y_stretched, sr, format='WAV')
        st.audio(buf.getvalue(), format="audio/wav")

        # Step 5: Download button
        st.download_button(
            label="⬇️ Download Adjusted Audio",
            data=buf.getvalue(),
            file_name="adjusted_audio.wav",
            mime="audio/wav"
        )
    except Exception as e:
        st.error(f"⚠ Error processing file: {e}")
