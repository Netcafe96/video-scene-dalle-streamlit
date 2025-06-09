import os
from scenedetect import VideoManager, SceneManager
from scenedetect.detectors import ContentDetector
from moviepy.editor import VideoFileClip

def detect_scenes(video_path, output_dir, threshold=30.0):
    os.makedirs(output_dir, exist_ok=True)

    # Set up SceneDetect
    video_manager = VideoManager([video_path])
    scene_manager = SceneManager()
    scene_manager.add_detector(ContentDetector(threshold=threshold))

    video_manager.set_downscale_factor()
    video_manager.start()

    scene_manager.detect_scenes(frame_source=video_manager)
    scene_list = scene_manager.get_scene_list()

    clip = VideoFileClip(video_path)
    screenshots = []

    for idx, (start, end) in enumerate(scene_list):
        timestamp = int(start.get_seconds())
        frame = clip.get_frame(timestamp)
        img_path = os.path.join(output_dir, f"scene_{idx}.jpg")
        clip.save_frame(img_path, t=timestamp)
        screenshots.append((timestamp, img_path))

    video_manager.release()
    clip.close()

    return screenshots
