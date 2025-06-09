import streamlit as st
import tempfile
import os
from helpers.video_utils import detect_scenes                      # 🛠️ sửa import
from helpers.ai_image_utils import generate_prompt_from_timecode, generate_image
from PIL import Image

st.title("🎬 Scene Detection + DALL·E AI Image Generator")

uploaded_video = st.file_uploader("Tải lên video", type=["mp4", "mov"])

if uploaded_video:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_video:
        tmp_video.write(uploaded_video.read())
        video_path = tmp_video.name

    with st.spinner("Đang phát hiện cảnh từ video..."):
        output_dir = tempfile.mkdtemp()
        scenes = detect_scenes(video_path, output_dir, threshold=30.0)

    if scenes:
        st.success(f"🎞️ Đã phát hiện {len(scenes)} cảnh!")
        for timecode, img_path in scenes:
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(img_path, caption=f"Cảnh tại {timecode}s", width=250)
            with col2:
                prompt = generate_prompt_from_timecode(timecode)
                st.markdown(f"**Prompt:** `{prompt}`")
                if st.button(f"🧠 Tạo ảnh AI cho cảnh {timecode}s", key=f"btn_{timecode}"):
                    img_url = generate_image(prompt)
                    st.image(img_url, caption="Ảnh AI", width=256)
    else:
        st.warning("⚠️ Không phát hiện được cảnh nào.")
