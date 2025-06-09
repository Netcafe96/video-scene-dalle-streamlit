import streamlit as st
import tempfile
import os
from helpers.video_utils import detect_scenes_ffmpeg
from helpers.ai_image_utils import generate_prompt_from_timecode, generate_image
from PIL import Image

# Cấu hình trang
st.set_page_config(page_title="🎬 Video → AI Image", layout="wide")
st.title("🎬 Tách cảnh từ video & tạo ảnh minh họa AI bằng DALL·E")

# Upload video
uploaded = st.file_uploader("📤 Tải lên video (.mp4 hoặc .mov)", type=["mp4", "mov"])

if uploaded:
    # Lưu video tạm
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
        tmp.write(uploaded.read())
        video_path = tmp.name

    st.info("⏳ Đang trích ảnh từ video bằng ffmpeg (mỗi 5 giây)...")
    output_dir = tempfile.mkdtemp()
    scenes = detect_scenes_ffmpeg(video_path, output_dir, interval=5)

    if scenes:
        st.success(f"✅ Đã trích được {len(scenes)} ảnh từ video.")

        # Hiển thị từng cảnh và prompt
        for t, img_path in scenes:
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(img_path, caption=f"🕒 Cảnh tại {t} giây", use_column_width=True)
            with col2:
                prompt = generate_prompt_from_timecode(t)
                st.markdown(f"**Prompt tạo ảnh AI:** `{prompt}`")
                if st.button(f"✨ Tạo ảnh AI cho cảnh {t}s", key=f"ai_{t}"):
                    with st.spinner("🧠 Đang tạo ảnh bằng DALL·E..."):
                        url = generate_image(prompt)
                        st.image(url, caption="📷 Ảnh AI", width=256)
    else:
        st.warning("⚠️ Không tìm thấy ảnh nào được trích từ video.")
