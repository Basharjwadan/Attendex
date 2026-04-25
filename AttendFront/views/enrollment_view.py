"""
enrollment_view.py – EnrollmentView: student registration view.

Layout:
  Left  – live camera feed with a Capture button below
  Right – captured photo preview, name text field, and Submit button
"""

import asyncio
import flet as ft

from camera import Camera
from panels.camera_panel import build_camera_panel, camera_update_loop

# 1×1 transparent GIF placeholder (avoids Flet's "src required" error)
_TRANSPARENT_SRC = (
    "data:image/gif;base64,"
    "R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"
)


class EnrollmentView:
    """Enrollment view – captures a photo of a new student and registers them."""

    def __init__(self, page: ft.Page):
        self.page = page

        # Page-level settings
        self.page.title = "AttendFlet – تسجيل طالب جديد"
        self.page.padding = 0
        self.page.spacing = 0
        self.page.bgcolor = "#1A1A2E"
        self.page.on_close = self._on_close

        # --- Camera ---
        self.camera = Camera(device=0, flip_horizontal=True)
        self.camera_container, self._camera_image = build_camera_panel(self.camera)

        # --- Right-panel state ---
        self._captured_b64: str | None = None
        self._build_right_panel()

    # ------------------------------------------------------------------
    # Right panel – preview + form
    # ------------------------------------------------------------------
    def _build_right_panel(self):
        # Captured photo preview
        self._preview_image = ft.Image(
            src=_TRANSPARENT_SRC,
            fit=ft.BoxFit.CONTAIN,
            expand=True,
            gapless_playback=True,
        )

        self._preview_container = ft.Container(
            content=ft.Stack(
                controls=[
                    ft.Container(
                        content=ft.Icon(
                            ft.Icons.PERSON_OUTLINED,
                            size=80,
                            color="#424242",
                        ),
                        alignment=ft.Alignment(0, 0),
                        expand=True,
                    ),
                    self._preview_image,
                ],
                expand=True,
            ),
            expand=True,
            bgcolor="#0F0F1E",
            border_radius=16,
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            border=ft.border.all(2, "#2D2D5E"),
        )

        # Name input
        self._name_field = ft.TextField(
            label="Student Name",
            hint_text="Enter full name…",
            border_radius=12,
            filled=True,
            bgcolor="#1E1E3F",
            border_color="#3D3D8F",
            focused_border_color="#7C5CBF",
            label_style=ft.TextStyle(color="#9090CC"),
            text_style=ft.TextStyle(color="#FFFFFF", size=16),
            cursor_color="#7C5CBF",
            content_padding=ft.Padding(16, 14, 16, 14),
        )

        # Submit button
        self._submit_btn = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE_ROUNDED, color="#FFFFFF", size=22),
                    ft.Text("Register Student", color="#FFFFFF", size=16, weight=ft.FontWeight.W_600),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10,
            ),
            bgcolor="#5C35A0",
            border_radius=12,
            padding=ft.Padding(0, 14, 0, 14),
            on_click=self._on_submit,
            ink=True,
            animate_scale=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
        )

        # Status message
        self._status_text = ft.Text(
            "",
            size=13,
            color="#7C5CBF",
            text_align=ft.TextAlign.CENTER,
        )

        self._right_panel = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "New Student",
                        size=22,
                        weight=ft.FontWeight.BOLD,
                        color="#FFFFFF",
                    ),
                    ft.Text(
                        "Capture a clear face photo, enter the name, then register.",
                        size=13,
                        color="#7070AA",
                    ),
                    ft.Container(height=8),
                    self._preview_container,
                    ft.Container(height=12),
                    self._name_field,
                    ft.Container(height=8),
                    self._submit_btn,
                    ft.Container(height=4),
                    self._status_text,
                ],
                expand=True,
                spacing=0,
            ),
            expand=2,
            padding=ft.Padding(20, 20, 20, 20),
            bgcolor="#12122A",
            border_radius=ft.BorderRadius(0, 0, 0, 0),
        )

    # ------------------------------------------------------------------
    # Capture button
    # ------------------------------------------------------------------
    def _build_capture_btn(self) -> ft.Container:
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.CAMERA_ALT_ROUNDED, color="#FFFFFF", size=22),
                    ft.Text("Capture", color="#FFFFFF", size=16, weight=ft.FontWeight.W_600),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10,
            ),
            bgcolor="#2E7D32",
            border_radius=12,
            padding=ft.Padding(0, 14, 0, 14),
            on_click=self._on_capture,
            ink=True,
        )

    # ------------------------------------------------------------------
    # Build & return the top-level control
    # ------------------------------------------------------------------
    def build(self) -> ft.Control:
        """Build and return the full-screen control."""
        background = ft.Container(bgcolor="#1A1A2E", expand=True)

        # Toolbar with home button
        home_btn = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.HOME_ROUNDED, color="#FFFFFF", size=18),
                    ft.Text("Home", color="#FFFFFF", size=13, weight=ft.FontWeight.W_500),
                ],
                spacing=6,
                tight=True,
            ),
            bgcolor="#2D2D5E",
            border_radius=20,
            padding=ft.Padding(14, 7, 14, 7),
            on_click=self._go_home,
            ink=True,
        )

        toolbar = ft.Container(
            content=ft.Row(controls=[home_btn], spacing=0),
            padding=ft.Padding(0, 0, 0, 4),
        )

        # Camera + capture button stacked in a column
        left_panel = ft.Container(
            content=ft.Column(
                controls=[
                    toolbar,
                    self.camera_container,
                    ft.Container(height=8),
                    self._build_capture_btn(),
                ],
                expand=True,
                spacing=0,
            ),
            expand=3,
            padding=ft.Padding(0, 0, 8, 0),
        )

        content_row = ft.Row(
            controls=[left_panel, self._right_panel],
            expand=True,
            spacing=0,
        )

        app_layer = ft.Container(
            content=content_row,
            expand=True,
            padding=16,
        )

        return ft.Stack(
            controls=[background, app_layer],
            expand=True,
        )

    def _go_home(self, e):
        """Stop everything and return to the root dashboard."""
        self.camera.stop()
        from views.root_view import build_root_view
        self.page.bgcolor = "#1E1E1E"
        self.page.controls.clear()
        self.page.controls.append(build_root_view(self.page))
        self.page.update()

    # ------------------------------------------------------------------
    # Callbacks
    # ------------------------------------------------------------------
    def _on_capture(self, e):
        """Grab the current camera frame and show it in the preview."""
        frame = self.camera.get_frame()
        if frame:
            self._captured_b64 = frame
            self._preview_image.src = f"data:image/jpeg;base64,{frame}"
            self._preview_image.update()
            self._set_status("Photo captured! Enter a name and press Register.", "#4CAF50")
        else:
            self._set_status("No frame available – is the camera on?", "#EF5350")

    def _on_submit(self, e):
        """Validate inputs and register the student."""
        name = self._name_field.value.strip() if self._name_field.value else ""

        if not name:
            self._set_status("Please enter the student's name.", "#EF5350")
            return
        if not self._captured_b64:
            self._set_status("Please capture a photo first.", "#EF5350")
            return

        # TODO: pass (name, self._captured_b64) to the embedding/database service
        
        self._set_status(f"✓ '{name}' registered successfully!", "#4CAF50")
        self._name_field.value = ""
        self._captured_b64 = None
        self._preview_image.src = _TRANSPARENT_SRC
        self._name_field.update()
        self._preview_image.update()

    def _set_status(self, message: str, color: str):
        self._status_text.value = message
        self._status_text.color = color
        self._status_text.update()

    def _on_close(self, e):
        self.camera.stop()

    # ------------------------------------------------------------------
    # Run (starts the camera frame loop)
    # ------------------------------------------------------------------
    async def run(self):
        """Start the camera update loop (call with await)."""
        await camera_update_loop(self.camera, self._camera_image)
