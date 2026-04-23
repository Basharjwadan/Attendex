"""
pending_panel.py – Pending requests list with snapshot thumbnails and Take button.
"""

from typing import Callable
from datetime import datetime
import flet as ft


def snapshot_tile(frame_b64: str, timestamp: str) -> ft.Container:
    """Build a tile showing a captured snapshot thumbnail with timestamp."""
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    content=ft.Image(
                        src=f"data:image/jpeg;base64,{frame_b64}",
                        fit=ft.BoxFit.COVER,
                        gapless_playback=True,
                    ),
                    height=80,
                    width=120,
                    border_radius=8,
                    clip_behavior=ft.ClipBehavior.HARD_EDGE,
                ),
                ft.Text(
                    timestamp,
                    size=10,
                    color="#9E9E9E",
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
            spacing=4,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=6,
        border_radius=10,
        bgcolor="#2A2A2A",
    )


class PendingPanel:
    """Manages the pending-requests panel with dynamic snapshot additions."""

    def __init__(self, on_take: Callable):
        self._on_take = on_take

        self._header = ft.Text(
            "الصور الملتقطة",
            size=20,
            weight=ft.FontWeight.BOLD,
            color="#FFFFFF",
            text_align=ft.TextAlign.RIGHT,
            rtl=True,
        )

        self._list_view = ft.Row(
            controls=[],
            expand=True,
            spacing=8,
            scroll=ft.ScrollMode.AUTO,
        )

        self._empty_label = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.CAMERA_ALT, size=28, color="#555555"),
                    ft.Text(
                        "قائمة الإنتظار",
                        size=14,
                        color="#777777",
                        text_align=ft.TextAlign.CENTER,
                        rtl=True,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=8,
            ),
            alignment=ft.Alignment(0, 0),
            expand=True,
        )

        # Show empty label initially
        self._content_stack = ft.Stack(
            controls=[self._list_view, self._empty_label],
            expand=True,
        )

        self._take_button = ft.Container(
            content=ft.ElevatedButton(
                content=ft.Text("التقاط", size=16, weight=ft.FontWeight.BOLD),
                icon=ft.Icons.CAMERA_ALT,
                on_click=self._on_take,
                bgcolor="#4CAF50",
                color="#FFFFFF",
                height=56,
            ),
        )

        self.container = ft.Container(
            content=ft.Row(
                controls=[
                    self._header,
                    ft.VerticalDivider(width=1, color="#333333"),
                    self._content_stack,
                    self._take_button,
                ],
                spacing=12,
                expand=True,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            expand=True,
            bgcolor="#1E1E1E",
            border_radius=12,
            padding=ft.Padding(left=16, top=8, right=16, bottom=8),
        )

    def add_snapshot(self, frame_b64: str):
        """Add a snapshot thumbnail to the end of the queue."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        tile = snapshot_tile(frame_b64, timestamp)
        self._list_view.controls.append(tile)

        # Hide the empty label once we have snapshots
        self._empty_label.visible = False

        try:
            self._list_view.update()
            self._empty_label.update()
        except Exception:
            pass
