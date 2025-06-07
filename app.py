import streamlit as st
import librosa
import soundfile as sf
import io

# Page config
st.set_page_config(page_title="Audio Speed Adjuster", layout="centered")

# Custom CSS to adjust fonts and spacing (you can tweak colors/fonts here)
st.markdown("""
<style>
h1 {
    font-size: 3rem;
    font-weight: 700;
    margin-bottom: 0.3rem;
    text-align: center;
}
h2 {
    font-size: 1.5rem;
    margin-top: 1.5rem;
    margin-bottom: 0.5rem;
    text-align: center;
}
.section {
    padding: 1.5rem 2rem;
    border-radius: 10px;
    background-color: #f5f5f7;
    margin-bottom: 2rem;
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
}
.upload-btn {
    text-align: center;
    margin-bottom: 1.5rem;
}
.stSlider > div[data-baseweb="slider"] {
    margin: 0 auto !important;
    max-width: 400px;
}
</style>
""", unsafe_allow_html=True)

# Title section
st.markdown('<h1>🎧 Audio Speed Adjuster</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; max-width:600px; margin:auto;">Upload an audio file and adjust its playback speed without altering the pitch.</p>', unsafe_allow_html=True)

# Upload section
with st.container():
    st.markdown('<div class="section upload-btn">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("📁 Browse an audio file (.wav or .mp3)", type=["wav", "mp3"], label_visibility="visible")
    st.markdown('</div>', unsafe_allow_html=True)

if uploaded_file is not None:
    with st.container():
        st.markdown('<div class="section">', unsafe_allow_html=True)
        st.info("Loading audio... Please wait.")
        try:
            y, sr = librosa.load(uploaded_file, sr=None)
            st.success("✅ Audio loaded successfully!")
            
            # Speed slider centered and styled
            speed = st.slider("🎚️ Choose Playback Speed", 0.5, 2.0, 1.0, 0.1)
            
            if speed != 1.0:
                y_stretched = librosa.effects.time_stretch(y, rate=speed)
            else:
                y_stretched = y

            # Audio preview with heading
            st.markdown('<h2>▶️ Preview Adjusted Audio</h2>', unsafe_allow_html=True)
            buf = io.BytesIO()
            sf.write(buf, y_stretched, sr, format='WAV')
            st.audio(buf.getvalue(), format="audio/wav")

            # Download button centered
            st.markdown('<div style="text-align:center; margin-top:1.5rem;">', unsafe_allow_html=True)
            st.download_button(
                label="⬇️ Download Adjusted Audio",
                data=buf.getvalue(),
                file_name="adjusted_audio.wav",
                mime="audio/wav",
                use_container_width=False
            )
            st.markdown('</div>', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"⚠️ Error processing file: {e}")
        st.markdown('</div>', unsafe_allow_html=True)
