"""
detection_view.py – DetectionView: the main camera/attendance view.

Builds a 4-layer ft.Stack:
  1. Background  – solid gray
  2. App layer   – camera | names | pending+take
  3. Overlay     – welcome banner (shown on Take press)
  4. Snapshot animation layer – pop-in then fly to pending
"""

import asyncio
import flet as ft

from camera import Camera
from panels.camera_panel import build_camera_panel, camera_update_loop
from panels.names_panel import build_names_panel
from panels.pending_panel import PendingPanel
from overlay import build_overlay
from face_detector import FaceDetector


class DetectionView:
    """Detection view – plain class that builds a full-screen ft.Stack."""

    def __init__(self, page: ft.Page):
        self.page = page

        # Page-level settings
        self.page.title = "AttendFlet – نظام الحضور"
        self.page.padding = 0
        self.page.spacing = 0
        self.page.bgcolor = "#616161"
        self.page.on_close = self._on_close

        # --- Camera ---
        self.camera = Camera(device=0, flip_horizontal=True)

        # --- Panels ---
        self.camera_container, self._camera_image = build_camera_panel(self.camera)
        self.names_panel = build_names_panel()
        self._pending = PendingPanel(on_take=self._on_take)
        self.pending_panel = self._pending.container

        # --- Overlay ---
        self.overlay = build_overlay()

        # --- Snapshot animation ---
        self._build_snapshot_anim()

        # --- Face Detection ---
        self.face_detector = FaceDetector(
            camera=self.camera,
            on_face_detected_callback=self._on_face_detected
        )

    # ------------------------------------------------------------------
    # Snapshot animation container
    # ------------------------------------------------------------------
    def _build_snapshot_anim(self):
        """Create the animated snapshot container for the fly-to-pending effect."""
        self._snap_image = ft.Image(
            src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7",  # 1x1 transparent
            fit=ft.BoxFit.COVER,
            gapless_playback=True,
        )

        self._snap_container = ft.Container(
            content=self._snap_image,
            width=300,
            height=200,
            border_radius=16,
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            bgcolor="#000000",
            scale=0,
            offset=ft.Offset(0, 0),
            opacity=0,
            animate_scale=ft.Animation(400, ft.AnimationCurve.EASE_OUT_BACK),
            animate_offset=ft.Animation(600, ft.AnimationCurve.EASE_IN_OUT_CUBIC),
            animate_opacity=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
            visible=False,
        )

        # Full-screen wrapper – invisible initially so clicks pass through
        self._snap_layer = ft.Container(
            content=self._snap_container,
            alignment=ft.Alignment(-0.25, -0.2),
            expand=True,
            visible=False,
        )

    # ------------------------------------------------------------------
    # Build the layered stack and return it
    # ------------------------------------------------------------------
    def build(self) -> ft.Control:
        """Build and return the top-level ft.Stack control."""
        background = ft.Container(bgcolor="#616161", expand=True)

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
            bgcolor="#424242",
            border_radius=20,
            padding=ft.Padding(14, 7, 14, 7),
            on_click=self._go_home,
            ink=True,
        )

        toolbar = ft.Container(
            content=ft.Row(controls=[home_btn], spacing=0),
            padding=ft.Padding(0, 0, 0, 4),
        )

        # Top section: camera + names side by side
        top_row = ft.Row(
            controls=[
                self.camera_container,
                self.names_panel,
            ],
            expand=True,
            spacing=8,
        )

        # App layout: toolbar + top row + pending panel at bottom
        app_layer = ft.Container(
            content=ft.Column(
                controls=[
                    toolbar,
                    ft.Container(content=top_row, expand=4),
                    ft.Container(content=self.pending_panel, expand=1),
                ],
                expand=True,
                spacing=8,
            ),
            expand=True,
            padding=8,
        )

        return ft.Stack(
            controls=[background, app_layer, self.overlay, self._snap_layer],
            expand=True,
        )

    def _go_home(self, e):
        """Stop everything and return to the root dashboard."""
        self.face_detector.stop()
        self.camera.stop()
        from views.root_view import build_root_view
        self.page.bgcolor = "#1E1E1E"
        self.page.controls.clear()
        self.page.controls.append(build_root_view(self.page))
        self.page.update()

    # ------------------------------------------------------------------
    # Callbacks
    # ------------------------------------------------------------------
    def _on_take(self, e):
        """Handle Take button press – extract all faces from the current frame."""
        self.face_detector.force_extract_faces()

    async def _animate_snapshot(self, frame_b64: str):
        """Animate: pop-in at center → bounce → fly to pending panel."""
        self._snap_image.src = f"data:image/jpeg;base64,{frame_b64}"

        # Show the layer
        self._snap_layer.visible = True
        self._snap_container.visible = True
        self._snap_container.scale = 0
        self._snap_container.offset = ft.Offset(0, 0)
        self._snap_container.opacity = 1
        self._snap_layer.update()
        await asyncio.sleep(0.05)

        # Phase 1: Pop in (scale 0 → 1.15)
        self._snap_container.scale = 1.15
        self._snap_container.update()
        await asyncio.sleep(0.4)

        # Phase 2: Bounce back (1.15 → 0.9)
        self._snap_container.scale = 0.9
        self._snap_container.update()
        await asyncio.sleep(0.2)

        # Phase 3: Settle (0.9 → 1.0)
        self._snap_container.scale = 1.0
        self._snap_container.update()
        await asyncio.sleep(0.3)

        # Phase 4: Fly to pending panel at bottom (shrink + translate down + fade)
        self._snap_container.scale = 0.15
        self._snap_container.offset = ft.Offset(0, 1.3)
        self._snap_container.opacity = 0.3
        self._snap_container.update()
        await asyncio.sleep(0.65)

        # Done – hide the layer so clicks pass through again
        self._snap_container.visible = False
        self._snap_layer.visible = False
        self._snap_container.scale = 0
        self._snap_container.offset = ft.Offset(0, 0)
        self._snap_container.opacity = 0
        self._snap_layer.update()

        # Add snapshot to pending panel
        self._pending.add_snapshot(frame_b64)

    async def _add_snapshot_async(self, face_b64: str):
        self._pending.add_snapshot(face_b64)

    def _on_face_detected(self, face_b64: str):
        """Callback from face detector thread with the face crop."""
        self.page.run_task(self._add_snapshot_async, face_b64)

    def _on_close(self, e):
        self.face_detector.stop()
        self.camera.stop()

    # ------------------------------------------------------------------
    # Run (starts the camera frame loop)
    # ------------------------------------------------------------------
    async def run(self):
        """Start the camera update loop (call with await)."""
        await camera_update_loop(self.camera, self._camera_image)
