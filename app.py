import streamlit as st
import tempfile
import os
from helpers.video_utils import detect_scenes
from helpers.ai_image_utils import generate_prompt_from_timecode, generate_image

st.set_page_config(page_title="Video → AI Images", layout="wide")
st.title("🎬 Scene Snapshot + DALL·E AI Generator")

uploaded = st.file_uploader("Upload video (.mp4/.mov)", type=["mp4", "mov"])
if uploaded:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as f:
        f.write(uploaded.read())
        video_path = f.name

    st.info("Processing video... extracting frames every 5 seconds.")
    output_dir = tempfile.mkdtemp()
    scenes = detect_scenes(video_path, output_dir, interval=5)

    if scenes:
        st.success(f"Extracted {len(scenes)} frames.")
        for t, img in scenes:
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(img, caption=f"{t}s frame")
            with col2:
                prompt = generate_prompt_from_timecode(t)
                st.markdown(f"**Prompt:** `{prompt}`")
                if st.button(f"Generate AI image at {t}s", key=t):
                    with st.spinner("Generating image..."):
                        url = generate_image(prompt)
                        st.image(url, width=256, caption="DALL·E output")
    else:
        st.warning("No frames extracted.")
