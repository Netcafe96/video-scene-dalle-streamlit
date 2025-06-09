import os, subprocess

def detect_scenes_ffmpeg(video_path, output_dir, interval=5):
    os.makedirs(output_dir, exist_ok=True)
    pattern = os.path.join(output_dir, "scene_%03d.jpg")
    subprocess.run(["ffmpeg", "-i", video_path, "-vf", f"fps=1/{interval}", "-q:v", "2", pattern],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return [(i * interval, os.path.join(output_dir, f"scene_{i:03d}.jpg"))
            for i, _ in enumerate(sorted(os.listdir(output_dir))) if _.endswith(".jpg")]
