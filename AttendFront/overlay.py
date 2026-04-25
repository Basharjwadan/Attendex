"""
overlay.py – Full-screen overlay layer (welcome banner, etc.).
"""

import asyncio
import flet as ft


def build_overlay() -> ft.Container:
    """
    Build the overlay container.
    Starts invisible; call show_welcome() to flash it.
    """
    welcome_text = ft.Text(
        "مرحبًا بك!",
        size=64,
        weight=ft.FontWeight.BOLD,
        color="#FFFFFF",
        text_align=ft.TextAlign.CENTER,
        rtl=True,
    )

    subtitle = ft.Text(
        "Welcome",
        size=28,
        color="#B0BEC5",
        text_align=ft.TextAlign.CENTER,
    )

    overlay = ft.Container(
        content=ft.Column(
            controls=[welcome_text, subtitle],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=12,
        ),
        alignment=ft.Alignment(0, 0),
        bgcolor=ft.Colors.with_opacity(0.85, "#000000"),
        border_radius=0,
        expand=True,
        visible=False,
    )

    return overlay


async def show_welcome(overlay: ft.Container, duration: float = 1.0):
    """Show the overlay for the specified duration, then hide it."""
    overlay.visible = True
    try:
        overlay.update()
    except Exception:
        return
    await asyncio.sleep(duration)
    overlay.visible = False
    try:
        overlay.update()
    except Exception:
        pass
