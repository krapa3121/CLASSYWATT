from pathlib import Path

def get_occupancy(source, mode, simulated_count, capacity, camera_index=0):
    """Returns (count, status, note). Uses OpenCV HOG person detection as a basic demo."""
    if mode != "Camera / video":
        count = max(0, min(int(simulated_count), capacity + 10))
        return count, "SIMULATED", "Using occupancy simulator; not a live count."

    try:
        import cv2
    except Exception as exc:
        return 0, "CAMERA ERROR", f"OpenCV unavailable: {exc}. Use simulator or install requirements."

    cap = None
    try:
        if source and source.strip():
            src = source.strip()
            if src.isdigit():
                cap = cv2.VideoCapture(int(src))
            else:
                cap = cv2.VideoCapture(src)
        else:
            cap = cv2.VideoCapture(int(camera_index))
        if not cap or not cap.isOpened():
            return 0, "CAMERA ERROR", "Could not open source. Check URL/file permissions and use an authorized stream."

        ok, frame = cap.read()
        if not ok or frame is None:
            return 0, "CAMERA ERROR", "No frame received. Check stream availability; occupancy is unknown."
        # HOG is a simple baseline detector, not production-grade. Count detected person boxes.
        hog = cv2.HOGDescriptor()
        hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        frame = cv2.resize(frame, (min(960, frame.shape[1]), int(frame.shape[0] * min(960, frame.shape[1]) / frame.shape[1])))
        boxes, weights = hog.detectMultiScale(frame, winStride=(8, 8), padding=(8, 8), scale=1.05)
        count = len(boxes)
        return count, "CAMERA CONNECTED", "One-frame HOG estimate. Accuracy depends on camera angle, lighting and occlusion."
    except Exception as exc:
        return 0, "CAMERA ERROR", f"Camera read/detection failed: {exc}. Occupancy is unknown."
    finally:
        if cap is not None:
            cap.release()
