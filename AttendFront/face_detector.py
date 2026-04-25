"""
face_detector.py – Background face detection using InsightFace.
"""

import threading
import time
import numpy as np
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
        self._thread = threading.Thread(target=self._detect_loop, daemon=True)
        self._thread.start()

    def _detect_loop(self):
        while self._running:
            frame = self.camera.get_raw_frame()
            if frame is not None:
                # Run the detector
                faces = self.app.get(frame)
                if len(faces) > 0:
                    self.on_face_detected_callback()
            
            # Run at ~2 Hz
            time.sleep(0.5)

    def stop(self):
        self._running = False
        if self._thread.is_alive():
            self._thread.join(timeout=2)
