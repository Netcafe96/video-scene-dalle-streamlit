import os
from moviepy.editor import VideoFileClip
from PIL import Image

def detect_scenes(video_path, output_dir, interval=5):
    os.makedirs(output_dir, exist_ok=True)
    clip = VideoFileClip(video_path)
    duration = int(clip.duration)
    results = []

    for t in range(0, duration, interval):
        frame = clip.get_frame(t)
        img_path = os.path.join(output_dir, f"scene_{t}.jpg")
        img = Image.fromarray(frame)
        img.save(img_path)
        results.append((t, img_path))

    clip.close()
    return results
