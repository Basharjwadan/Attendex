"""
face_detector.py – Background face detection using InsightFace.
"""

import threading
import time
import numpy as np
import cv2
import base64
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
        self._face_cache = []
        self._lock = threading.Lock()
        self._thread = threading.Thread(target=self._detect_loop, daemon=True)
        self._thread.start()

    def _process_and_filter_new_faces(self, frame, faces):
        """Processes faces, updates cache, and returns a list of base64 strings for new faces."""
        new_faces_b64 = []
        h, w = frame.shape[:2]
        
        for face in faces:
            box = face.bbox.astype(int)
            x1, y1 = max(0, box[0]), max(0, box[1])
            x2, y2 = min(w, box[2]), min(h, box[3])
            
            if x2 <= x1 or y2 <= y1:
                continue
                
            face_crop = frame[y1:y2, x1:x2]
            curr_resized = cv2.resize(face_crop, (100, 100))
            
            is_new_face = True
            for cached_face in self._face_cache:
                mse = np.mean((curr_resized.astype("float") - cached_face.astype("float")) ** 2)
                if mse < 1500:
                    is_new_face = False
                    break
            
            if is_new_face:
                self._face_cache.append(curr_resized.copy())
                
                _, buffer = cv2.imencode(".jpg", face_crop)
                face_b64 = base64.b64encode(buffer).decode("utf-8")
                new_faces_b64.append(face_b64)
                
        if len(self._face_cache) > 100:
            self._face_cache = self._face_cache[-100:]
            
        return new_faces_b64

    def _detect_loop(self):
        while self._running:
            current_time = time.time()
            # Only run inference if 3 seconds have passed since the last detection
            if current_time - self._last_detection_time >= 3.0:
                frame = self.camera.get_raw_frame()
                if frame is not None:
                    # Run the detector safely
                    with self._lock:
                        faces = self.app.get(frame)
                    if len(faces) > 0:
                        new_faces_b64 = self._process_and_filter_new_faces(frame, faces)
                        for face_b64 in new_faces_b64:
                            self.on_face_detected_callback(face_b64)
                        
                        # Reset cooldown so we don't spam inference
                        self._last_detection_time = time.time()
            
            # Run at ~2 Hz
            time.sleep(0.5)

    def force_extract_faces(self):
        """Immediately extract all faces from the current frame and push to queue."""
        frame = self.camera.get_raw_frame()
        if frame is not None:
            with self._lock:
                faces = self.app.get(frame)
            if len(faces) > 0:
                new_faces_b64 = self._process_and_filter_new_faces(frame, faces)
                for face_b64 in new_faces_b64:
                    self.on_face_detected_callback(face_b64)
                
                # Reset background cooldown
                self._last_detection_time = time.time()

    def stop(self):
        self._running = False
        if self._thread.is_alive():
            self._thread.join(timeout=2)
