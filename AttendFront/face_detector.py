"""
face_detector.py – Background face detection using InsightFace.
"""

import threading
import time
import numpy as np
import cv2
from insightface.app import FaceAnalysis

class FaceDetector:
    def __init__(self, camera, on_face_detected_callback):
        self.camera = camera
        self.on_face_detected_callback = on_face_detected_callback
        
        # Initialize the detection model only
        self.app = FaceAnalysis(name='buffalo_s', allowed_modules=['detection'])
        # Use ctx_id=0 if GPU is available, otherwise it falls back to CPU. -1 forces CPU.
        self.app.prepare(ctx_id=0, det_size=(640, 640))
        
        self._running = True
        self._last_detection_time = 0
        self._last_face_crop = None
        self._thread = threading.Thread(target=self._detect_loop, daemon=True)
        self._thread.start()

    def _detect_loop(self):
        while self._running:
            current_time = time.time()
            # Only run inference if 3 seconds have passed since the last detection
            if current_time - self._last_detection_time >= 3.0:
                frame = self.camera.get_raw_frame()
                if frame is not None:
                    # Run the detector
                    faces = self.app.get(frame)
                    if len(faces) > 0:
                        # Extract face crop for similarity check
                        box = faces[0].bbox.astype(int)
                        h, w = frame.shape[:2]
                        x1, y1 = max(0, box[0]), max(0, box[1])
                        x2, y2 = min(w, box[2]), min(h, box[3])
                        
                        face_crop = frame[y1:y2, x1:x2]
                        
                        is_new_face = True
                        if self._last_face_crop is not None and face_crop.size > 0 and self._last_face_crop.size > 0:
                            # Resize to a fixed size for comparison
                            curr_resized = cv2.resize(face_crop, (100, 100))
                            prev_resized = cv2.resize(self._last_face_crop, (100, 100))
                            
                            # Mean Squared Error
                            mse = np.mean((curr_resized.astype("float") - prev_resized.astype("float")) ** 2)
                            
                            # If MSE is low, it's likely the same face
                            if mse < 1500:
                                is_new_face = False
                        
                        # Only trigger if it's a new face
                        if is_new_face and face_crop.size > 0:
                            self._last_face_crop = face_crop.copy()
                            self.on_face_detected_callback()
                        
                        # Reset cooldown even if it's the same face, so we don't spam inference while someone is standing there
                        self._last_detection_time = time.time()
                    else:
                        # Clear last face crop if no one is in the frame
                        self._last_face_crop = None
            
            # Run at ~2 Hz
            time.sleep(0.5)

    def stop(self):
        self._running = False
        if self._thread.is_alive():
            self._thread.join(timeout=2)
