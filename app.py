import streamlit as st
import librosa
import soundfile as sf
import numpy as np
import io

st.set_page_config(page_title="Pitch Lock", layout="centered")

# --- HEADER STYLE ---
st.markdown("""
    <style>
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: #333;
            padding: 10px 30px;
            border-radius: 8px;
            color: white;
        }
        .header-left {
            display: flex;
            align-items: center;
            gap: 15px;
        }
        .header-logo {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            background: white;
        }
        .header-title {
            font-size: 24px;
            font-weight: bold;
        }
        .header-center input {
            padding: 5px 15px;
            border-radius: 20px;
            border: none;
            width: 250px;
        }
        .header-right button {
            background-color: #6a62d5;
            color: white;
            border: none;
            padding: 6px 16px;
            border-radius: 20px;
            cursor: pointer;
        }
    </style>
    <div class="header">
        <div class="header-left">
            <div class="header-logo"></div>
            <div class="header-title">Pitch Lock</div>
        </div>
        <div class="header-center">
            <input type="text" placeholder="Search..." />
        </div>
        <div class="header-right">
            <button>Sign In</button>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- MAIN TITLE ---
st.markdown("### 🎧 Audio Speed Adjuster")
st.write("Upload audio and adjust its speed **without changing pitch**.")

# --- UPLOAD AUDIO ---
uploaded_file = st.file_uploader("🎵 Upload Audio File (MP3 or WAV)", type=["mp3", "wav"])

if uploaded_file is not None:
    try:
        y, sr = librosa.load(uploaded_file, sr=None)
        st.success("✅ Audio file loaded successfully!")

        # --- TRANSPORT BAR: Speed Slider + Buttons ---
        st.markdown("#### 🎚️ Playback Speed")
        col1, col2, col3 = st.columns([1, 5, 1])
        with col1:
            play_button = st.button("⏵ Play")
        with col2:
            speed = st.slider("", min_value=0.5, max_value=2.0, value=1.0, step=0.1, format="%.1fx")
        with col3:
            pause_button = st.button("⏸ Pause")

        if speed != 1.0:
            y_stretched = librosa.effects.time_stretch(y, rate=speed)
        else:
            y_stretched = y

        # --- AUDIO WAVEFORM PLACEHOLDER ---
        st.markdown("##### 📈 Waveform (Placeholder)")
        st.image("https://upload.wikimedia.org/wikipedia/commons/1/1a/Waveform_example.svg", use_column_width=True)

        # --- PREVIEW AUDIO ---
        st.markdown("#### ▶️ Preview Adjusted Audio")
        buf = io.BytesIO()
        sf.write(buf, y_stretched, sr, format='WAV')
        st.audio(buf.getvalue(), format='audio/wav')

        # --- DOWNLOAD BUTTON ---
        st.download_button(
            label="⬇️ Download Adjusted Audio",
            data=buf.getvalue(),
            file_name="adjusted_audio.wav",
            mime="audio/wav"
        )

    except Exception as e:
        st.error(f"⚠️ Error loading file: {e}")
else:
    st.info("📂 Please upload an audio file to get started.")
