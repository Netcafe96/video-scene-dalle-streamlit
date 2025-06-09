import streamlit as st, tempfile, os
from helpers.video_utils import detect_scenes_ffmpeg
from helpers.ai_image_utils import generate_prompt_from_timecode, generate_image

st.title("🎬 Video to AI Images (Replit Template)")

uploaded = st.file_uploader("Upload video (.mp4 / .mov)", type=["mp4", "mov"])
if uploaded:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
        tmp.write(uploaded.read())
        video_path = tmp.name

    output_dir = tempfile.mkdtemp()
    scenes = detect_scenes_ffmpeg(video_path, output_dir, interval=5)

    for t, img in scenes:
        col1, col2 = st.columns([1,2])
        with col1: st.image(img, caption=f"{t}s")
        with col2:
            prompt = generate_prompt_from_timecode(t)
            st.markdown(f"**Prompt:** `{prompt}`")
            if st.button(f"Gen AI Image at {t}s", key=t):
                img_url = generate_image(prompt)
                st.image(img_url, width=256, caption="AI Image")
