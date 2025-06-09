import os
import subprocess
from PIL import Image

def detect_scenes_ffmpeg(video_path, output_dir, interval=5):
    os.makedirs(output_dir, exist_ok=True)
    pattern = os.path.join(output_dir, "scene_%03d.jpg")

    command = [
        "ffmpeg",
        "-i", video_path,
        "-vf", f"fps=1/{interval}",
        "-q:v", "2",
        pattern
    ]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    results = []
    for i, filename in enumerate(sorted(os.listdir(output_dir))):
        if filename.endswith(".jpg"):
            timecode = i * interval
            full_path = os.path.join(output_dir, filename)
            results.append((timecode, full_path))
    return results
