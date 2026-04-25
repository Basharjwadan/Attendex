import cv2
import numpy as np
from insightface.app import FaceAnalysis
import time

def test_face_detection():
    print("Initializing FaceAnalysis with buffalo_s (detection only)...")
    # allowed_modules=['detection'] ensures only the detection model is loaded,
    # saving memory and improving initialization speed.
    try:
        app = FaceAnalysis(name='buffalo_s', allowed_modules=['detection'])
        app.prepare(ctx_id=0, det_size=(640, 640)) # ctx_id=0 for GPU, -1 for CPU
        print("Model initialized successfully.")
    except Exception as e:
        print(f"Failed to initialize model: {e}")
        return

    print("Attempting to capture a frame from the webcam...")
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        ret, img = cap.read()
        cap.release()
        if not ret:
            print("Failed to grab frame. Using a dummy blank image instead.")
            img = np.zeros((480, 640, 3), dtype=np.uint8)
    else:
        print("Could not open camera. Using a dummy blank image instead.")
        img = np.zeros((480, 640, 3), dtype=np.uint8)

    print("Running face detection...")
    start_time = time.time()
    
    # Run the detector
    faces = app.get(img)
    
    end_time = time.time()
    
    print(f"Detection took {(end_time - start_time) * 1000:.2f} ms.")
    print(f"Detected {len(faces)} face(s).")
    
    for i, face in enumerate(faces):
        # face contains bbox, kps, det_score
        bbox = face.bbox.astype(int)
        score = face.det_score
        print(f"Face {i+1}: BBox = {bbox}, Confidence = {score:.4f}")

if __name__ == '__main__':
    test_face_detection()
