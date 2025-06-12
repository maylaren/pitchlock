import streamlit as st
import librosa
import soundfile as sf
import numpy as np
import io
import base64

st.set_page_config(page_title="Pitch Lock", layout="wide")

# --- Load and Encode Logo ---
def load_logo_base64(path):
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

logo_base64 = load_logo_base64("logo.png")  # Replace with your own logo path

# --- HEADER NAVIGATION BAR ---
st.markdown(f"""
    <style>
        .top-nav {{
            background-color: #0a004f;
            color: white;
            padding: 10px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .nav-left {{
            display: flex;
            align-items: center;
            gap: 15px;
        }}
        .logo {{
            width: 45px;
            height: 45px;
            border-radius: 50%;
            background-image: url("data:image/png;base64,{logo_base64}");
            background-size: cover;
            background-position: center;
        }}
        .nav-title {{
            font-size: 22px;
            font-weight: bold;
        }}
        .search-bar {{
            flex: 1;
            display: flex;
            justify-content: center;
        }}
        .search-bar input {{
            width: 300px;
            padding: 6px 15px;
            border-radius: 20px;
            border: none;
        }}
        .nav-right a {{
            color: white;
            margin-left: 20px;
            text-decoration: none;
            font-weight: 500;
        }}
    </style>
    <div class="top-nav">
        <div class="nav-left">
            <div class="logo"></div>
            <div class="nav-title">Pitch Lock</div>
        </div>
        <div class="search-bar">
            <input type="text" placeholder="Search..." />
        </div>
        <div class="nav-right">
            <a href="#">Help</a>
            <a href="#">About us</a>
            <a href="#">Sign In</a>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- Audio Tool Interface ---
st.markdown("<br><h3 style='text-align: center;'>Smart Audio Time-Stretching</h3>", unsafe_allow_html=True)
st.write("A web-based audio tool that adjusts playback speed while preserving pitch.")

uploaded_file = st.file_uploader("🎵 Upload Audio File (MP3 or WAV)", type=["mp3", "wav"])

if uploaded_file is not None:
    try:
        y, sr = librosa.load(uploaded_file, sr=None)
        st.success("✅ Audio file loaded successfully!")

        st.image("waveform.png", caption="Waveform")

        # Speed Control
        st.markdown("<div style='text-align: center;'>Speed</div>", unsafe_allow_html=True)
        speed = st.slider("", min_value=0.5, max_value=2.0, value=1.0, step=0.1, format="%.1fx")
        st.markdown(f"<div style='text-align: center;'>{speed:.1f}x</div>", unsafe_allow_html=True)

        y_stretched = librosa.effects.time_stretch(y, rate=speed) if speed != 1.0 else y

        # Playback button
        st.markdown("<div style='text-align: center;'><button style='font-size:24px; border:none;'>▶️</button></div>", unsafe_allow_html=True)

        # Audio Output
        buf = io.BytesIO()
        sf.write(buf, y_stretched, sr, format='WAV')
        st.audio(buf.getvalue(), format='audio/wav')

        # Download Button
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        st.download_button(
            label="Download File",
            data=buf.getvalue(),
            file_name="adjusted_audio.wav",
            mime="audio/wav",
            use_container_width=False
        )
        st.markdown("</div>", unsafe_allow_html=True)

        # Footer Features
        st.markdown("""
            <hr>
            <div style="display: flex; justify-content: space-around; padding: 20px 0;">
                <div style="width: 30%; text-align: center;">
                    <h4>Control Speed Without Losing Tone</h4>
                    <p>A web-based audio tool that adjusts playback speed while preserving the original pitch. Ideal for musicians, students, and audio engineers.</p>
                </div>
                <div style="width: 30%; text-align: center;">
                    <h4>Smart Audio Time-Stretching</h4>
                    <p>A web-based audio tool that adjusts playback speed while preserving the original pitch. Ideal for musicians, students, and audio engineers.</p>
                </div>
                <div style="width: 30%; text-align: center;">
                    <h4>Supported File Format</h4>
                    <p>Supports MP3 and WAV formats. For best results, use WAV for high-quality output.</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"⚠️ Error loading file: {e}")
else:
    st.info("📂 Please upload an audio file to get started.")
