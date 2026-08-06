from pathlib import Path
import cv2


def extract_video_metadata(video_path: str) -> dict:
    """
    Extract metadata from a video file using OpenCV.
    """

    path = Path(video_path)

    cap = cv2.VideoCapture(str(path))

    if not cap.isOpened():
        raise ValueError(f"Cannot open video: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)

    duration = frame_count / fps if fps else 0

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    cap.release()

    size_mb = path.stat().st_size / (1024 * 1024)

    return {
        "duration": round(duration, 2),
        "fps": round(fps, 2),
        "width": width,
        "height": height,
        "size_mb": round(size_mb, 2),
    }