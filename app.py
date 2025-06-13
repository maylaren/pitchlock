import streamlit as st
import librosa
import librosa.display
import soundfile as sf
import numpy as np
import io
import base64
import matplotlib.pyplot as plt

st.set_page_config(page_title="Pitch Lock", layout="wide")

# --- Load and Encode Logo ---
def load_logo_base64(path):
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

logo_base64 = load_logo_base64("logo.png")  # Replace with your logo file

# --- HEADER NAVIGATION BAR ---
st.markdown(f"""
    <style>
        .top-nav {{
            background-color: #0a004f;
            color: white;
            padding: 10px 20px;
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        .nav-center {{
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
            font-size: 24px;
            font-weight: bold;
        }}
    </style>
    <div class="top-nav">
        <div class="nav-center">
            <div class="logo"></div>
            <div class="nav-title">Pitch Lock</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- Audio Tool Interface ---
st.markdown("<br><h3 style='text-align: center;'>Smart Audio Time-Stretching</h3>", unsafe_allow_html=True)
st.write("A web-based audio tool that adjusts playback speed while preserving pitch.")

uploaded_file = st.file_uploader("🎵 Upload Audio File (MP3 or WAV)", type=["mp3", "wav"])

if uploaded_file is not None:
    try:
        y, sr = librosa.load(uploaded_file, sr=None, mono=False)
        st.success("✅ Audio file loaded successfully!")

        # --- Display Original Waveform ---
        st.markdown("#### 📈 Original Audio Waveform")
        fig, ax = plt.subplots(figsize=(10, 3))
        if y.ndim == 1:
            librosa.display.waveshow(y, sr=sr, ax=ax)
        else:
            for ch in y:
                librosa.display.waveshow(ch, sr=sr, ax=ax)
        ax.set_title("Waveform (Original Audio)")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Amplitude")
        st.pyplot(fig)

        # Speed Control
        st.markdown("<div style='text-align: center;'>Speed</div>", unsafe_allow_html=True)
        speed = st.slider("", min_value=0.5, max_value=2.0, value=1.0, step=0.1, format="%.1fx")
        st.markdown(f"<div style='text-align: center;'>{speed:.1f}x</div>", unsafe_allow_html=True)

        # Time-stretching
        if y.ndim == 1:
            y_stretched = librosa.effects.time_stretch(y, rate=speed)
        else:
            y_stretched = np.vstack([
                librosa.effects.time_stretch(y[ch], rate=speed)
                for ch in range(y.shape[0])
            ])

        # --- Display Time-Stretched Waveform ---
        st.markdown("#### 🌀 Time-Stretched Waveform")
        fig2, ax2 = plt.subplots(figsize=(10, 3))
        if y_stretched.ndim == 1:
            librosa.display.waveshow(y_stretched, sr=sr, ax=ax2)
        else:
            for ch in y_stretched:
                librosa.display.waveshow(ch, sr=sr, ax=ax2)
        ax2.set_title(f"Waveform ({speed:.1f}x Speed)")
        ax2.set_xlabel("Time (s)")
        ax2.set_ylabel("Amplitude")
        st.pyplot(fig2)

        # --- Audio Output ---
        buf = io.BytesIO()
        if y_stretched.ndim == 2:
            sf.write(buf, y_stretched.T, sr, format='WAV')
        else:
            sf.write(buf, y_stretched, sr, format='WAV')

        st.markdown("<div style='text-align: center;'><button style='font-size:24px; border:none;'>▶️</button></div>", unsafe_allow_html=True)
        st.audio(buf.getvalue(), format='audio/wav')

        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        st.download_button(
            label="Download File",
            data=buf.getvalue(),
            file_name="adjusted_audio.wav",
            mime="audio/wav",
            use_container_width=False
        )
        st.markdown("</div>", unsafe_allow_html=True)

        # --- Footer Section ---
        st.markdown("""
            <hr>
            <div style="display: flex; justify-content: space-around; padding: 20px 0;">
                <div style="width: 30%; text-align: center;">
                    <h4>Control Speed Without Losing Tone</h4>
                    <p>A web-based audio tool that adjusts playback speed while preserving the original pitch. Ideal for musicians, students, and audio engineers.</p>
                </div>
                <div style="width: 30%; text-align: center;">
                    <h4>Smart Audio Time-Stretching</h4>
                    <p>Powered by Librosa, this app lets you stretch time without sacrificing pitch or clarity.</p>
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

# --- About Pitch Lock Expander ---
st.markdown("<hr>", unsafe_allow_html=True)
with st.expander("📘 About Pitch Lock"):
    st.markdown("""
    **Pitch Lock** is a user-friendly audio processing web app that allows users to change the playback speed of MP3 and WAV files **without altering their pitch**.  
    It's perfect for musicians, educators, language learners, and audio engineers who need precision and clarity while modifying tempo.
    """)
