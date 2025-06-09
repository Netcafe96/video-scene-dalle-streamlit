import streamlit as st
import tempfile
import os
from helpers.video_utils import detect_scenes
from helpers.ai_image_utils import generate_prompt_from_timecode, generate_image
from PIL import Image

st.set_page_config(page_title="🎬 Video Scene Snapshot + DALL·E AI", layout="wide")
st.title("🎬 Tự động chụp cảnh từ video & tạo ảnh minh họa bằng AI")

uploaded_video = st.file_uploader("📤 Tải lên video (.mp4, .mov)", type=["mp4", "mov"])

if uploaded_video:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_video:
        tmp_video.write(uploaded_video.read())
        video_path = tmp_video.name

    st.info("⏳ Đang xử lý video, trích ảnh mỗi 5 giây...")
    output_dir = tempfile.mkdtemp()
    scenes = detect_scenes(video_path, output_dir, interval=5)

    if scenes:
        st.success(f"✅ Đã trích xuất {len(scenes)} ảnh từ video!")

        for timecode, img_path in scenes:
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(img_path, caption=f"Cảnh tại {timecode}s", use_column_width=True)
            with col2:
                prompt = generate_prompt_from_timecode(timecode)
                st.markdown(f"**🧠 Prompt sinh ảnh:** `{prompt}`")

                if st.button(f"✨ Tạo ảnh AI từ cảnh {timecode}s", key=f"gen_{timecode}"):
                    with st.spinner("🎨 Đang tạo ảnh bằng DALL·E..."):
                        img_url = generate_image(prompt)
                        st.image(img_url, caption="📷 Ảnh AI", use_column_width=False, width=256)
    else:
        st.warning("⚠️ Không trích xuất được ảnh nào từ video.")
