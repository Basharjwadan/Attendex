import flet as ft
from app import AttendApp

def build_root_view(page: ft.Page):
    """Build the startup dashboard view."""

    async def start_detection(e):
        page.controls.clear()
        page.update()
        
        # Initialize the main app and start it
        app = AttendApp(page)
        await app.run()

    icon = ft.Icon(
        ft.Icons.CAMERA_ALT_ROUNDED,
        size=100,
        color="#4CAF50",
    )

    title = ft.Text(
        "AttendFlet – نظام الحضور",
        size=40,
        weight=ft.FontWeight.BOLD,
        color="#FFFFFF",
    )

    subtitle = ft.Text(
        "مرحباً بك في نظام تسجيل الحضور الآلي",
        size=20,
        color="#B0B0B0",
    )

    start_btn = ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(ft.Icons.PLAY_ARROW_ROUNDED, color="#FFFFFF", size=24),
                ft.Text(
                    "بدء التسجيل  ▶  Start Detection",
                    color="#FFFFFF",
                    size=18,
                    weight=ft.FontWeight.W_600,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        ),
        bgcolor="#4CAF50",
        border_radius=12,
        padding=ft.Padding(32, 16, 32, 16),
        on_click=start_detection,
        ink=True,
        width=340,
    )

    return ft.Container(
        content=ft.Column(
            controls=[
                icon,
                ft.Container(height=8),
                title,
                subtitle,
                ft.Container(height=40),
                start_btn,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        ),
        alignment=ft.Alignment(0, 0),
        expand=True,
        bgcolor="#1E1E1E",
    )
