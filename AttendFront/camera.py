"""
camera.py – Abstracted camera capture with drawing utilities.

The Camera class captures frames from a webcam in a background thread
and exposes helpers to draw rectangles and text on the stored frame
before encoding it as a base64 JPEG for display in Flet.
"""

import cv2
import base64
import threading
import time
import numpy as np
from typing import Tuple, Optional


class Camera:
    """Threaded webcam capture with drawing helpers."""

    def __init__(self, device: int = 0, flip_horizontal: bool = True):
        self._cap = cv2.VideoCapture(device)
        self._flip = flip_horizontal
        self._raw_frame: Optional[np.ndarray] = None
        self._lock = threading.Lock()
        self._running = True
        self._annotations: list = []  # queued draw commands
        self._thread = threading.Thread(target=self._capture_loop, daemon=True)
        self._thread.start()

    # ------------------------------------------------------------------
    # Capture loop
    # ------------------------------------------------------------------
    def _capture_loop(self):
        while self._running:
            ret, frame = self._cap.read()
            if ret:
                if self._flip:
                    frame = cv2.flip(frame, 1)
                with self._lock:
                    self._raw_frame = frame
            time.sleep(0.01)

    # ------------------------------------------------------------------
    # Drawing helpers – mutate the *stored* frame copy
    # ------------------------------------------------------------------
    def put_text(
        self,
        text: str,
        position: Tuple[int, int] = (30, 30),
        color: Tuple[int, int, int] = (0, 255, 0),
        scale: float = 1.0,
        thickness: int = 2,
        font: int = cv2.FONT_HERSHEY_SIMPLEX,
    ):
        """Queue a text draw on the next encoded frame."""
        self._annotations.append(
            ("text", text, position, color, scale, thickness, font)
        )

    def draw_rect(
        self,
        top_left: Tuple[int, int],
        bottom_right: Tuple[int, int],
        color: Tuple[int, int, int] = (0, 255, 0),
        thickness: int = 2,
    ):
        """Queue a rectangle draw on the next encoded frame."""
        self._annotations.append(("rect", top_left, bottom_right, color, thickness))

    def clear_annotations(self):
        """Remove all queued annotations."""
        self._annotations.clear()

    # ------------------------------------------------------------------
    # Frame access
    # ------------------------------------------------------------------
    def _apply_annotations(self, frame: np.ndarray) -> np.ndarray:
        """Apply all queued annotations to a frame copy."""
        annotated = frame.copy()
        for ann in self._annotations:
            if ann[0] == "text":
                _, text, pos, color, scale, thick, font = ann
                cv2.putText(annotated, text, pos, font, scale, color, thick)
            elif ann[0] == "rect":
                _, tl, br, color, thick = ann
                cv2.rectangle(annotated, tl, br, color, thick)
        return annotated

    def get_raw_frame(self) -> Optional[np.ndarray]:
        """Return the latest raw BGR frame (no annotations)."""
        with self._lock:
            if self._raw_frame is None:
                return None
            return self._raw_frame.copy()

    def get_frame(self) -> Optional[str]:
        """Return the latest frame with annotations as a base64 JPEG string."""
        with self._lock:
            if self._raw_frame is None:
                return None
            frame = self._raw_frame.copy()

        annotated = self._apply_annotations(frame)
        _, buffer = cv2.imencode(".jpg", annotated)
        return base64.b64encode(buffer).decode("utf-8")

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------
    def stop(self):
        """Stop the capture thread and release the camera."""
        self._running = False
        self._thread.join(timeout=2)
        self._cap.release()
