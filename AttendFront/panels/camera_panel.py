"""
camera_panel.py – Camera view panel for the app layer.
"""

import asyncio
import flet as ft
from camera import Camera


def build_camera_panel(camera: Camera) -> tuple[ft.Container, ft.Image]:
    """
    Build the camera panel container.

    Returns (container, image_control) so the caller can run
    the update loop with the image control.
    """
    camera_image = ft.Image(
        src=None,
        fit=ft.BoxFit.COVER,
        expand=True,
        gapless_playback=True,
    )

    container = ft.Container(
        content=camera_image,
        expand=3,
        bgcolor="#424242",
        border_radius=12,
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
        padding=0,
    )

    return container, camera_image


async def camera_update_loop(camera: Camera, image_ctrl: ft.Image):
    """Continuously push camera frames into the Image control."""
    while True:
        frame = camera.get_frame()
        if frame:
            image_ctrl.src = f"data:image/jpeg;base64,{frame}"
            try:
                image_ctrl.update()
            except Exception:
                break
        await asyncio.sleep(0.033)  # ~30 fps
