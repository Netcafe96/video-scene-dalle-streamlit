import cv2, os

def detect_scenes(video_path, output_dir, threshold=30.0):
    os.makedirs(output_dir, exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    prev_frame = None
    frame_count = 0
    scene_idx = 0
    scenes=[]

    while True:
        ret, frame = cap.read()
        if not ret: break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if prev_frame is not None:
            diff = cv2.absdiff(gray, prev_frame)
            score = diff.mean()
            if score > threshold:
                timestamp = int(frame_count / fps)
                path = os.path.join(output_dir, f"scene_{scene_idx}.jpg")
                cv2.imwrite(path, frame)
                scenes.append((timestamp, path))
                scene_idx += 1
        prev_frame = gray
        frame_count += 1

    cap.release()
    return scenes
