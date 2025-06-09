import streamlit as st
import tempfile
import os
from helpers.video_utils import detect_scenes_ffmpeg
from helpers.ai_image_utils import generate_prompt_from_timecode, generate_image
from PIL import Image

st.title("🎬 Video Scene Snapshot + AI Image Generator (ffmpeg-based)")

uploaded = st.file_uploader("Upload a video (.mp4, .mov)", type=["mp4", "mov"])

if uploaded:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
        tmp.write(uploaded.read())
        video_path = tmp.name

    st.info("Processing video and extracting frames every 5 seconds using ffmpeg...")
    output_dir = tempfile.mkdtemp()
    scenes = detect_scenes_ffmpeg(video_path, output_dir, interval=5)

    if scenes:
        st.success(f"Extracted {len(scenes)} frames.")
        for t, img_path in scenes:
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(img_path, caption=f"{t}s", width=240)
            with col2:
                prompt = generate_prompt_from_timecode(t)
                st.markdown(f"**Prompt:** `{prompt}`")
                if st.button(f"Generate AI Image at {t}s", key=f"ai_{t}"):
                    with st.spinner("Creating image..."):
                        url = generate_image(prompt)
                        st.image(url, caption="AI Generated", width=256)
    else:
        st.warning("No frames extracted.")
