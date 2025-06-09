import streamlit as st, tempfile, os
from utils.video_utils import detect_scenes
from utils.ai_image_utils import generate_prompt_from_timecode, generate_image

st.title("🎬 Scene Detection + DALL·E Image Generator")

u = st.file_uploader("Upload video", type=["mp4","mov"])
if u:
    tf = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    tf.write(u.read()); video_path = tf.name

    st.spinner("Detecting scenes...")
    scenes = detect_scenes(video_path, tempfile.mkdtemp(), threshold=30.0)

    if scenes:
        st.success(f"Detected {len(scenes)} scenes.")
        for t, img in scenes:
            c1, c2 = st.columns([1,2])
            with c1: st.image(img, caption=f"Scene @ {t}s", width=200)
            with c2:
                prompt = generate_prompt_from_timecode(t)
                st.markdown(f"**Prompt:** `{prompt}`")
                if st.button(f"Generate AI image for {t}s", key=t):
                    url = generate_image(prompt)
                    st.image(url, caption="DALL·E Output", width=256)
    else:
        st.warning("No scene detected.")
