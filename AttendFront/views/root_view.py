import flet as ft
from views.detection_view import DetectionView
from views.enrollment_view import EnrollmentView


def build_root_view(page: ft.Page):
    """Build the startup dashboard view."""

    async def start_detection(e):
        page.controls.clear()
        detection_view = DetectionView(page)
        page.controls.append(detection_view.build())
        page.update()
        await detection_view.run()

    async def start_enrollment(e):
        page.controls.clear()
        enrollment_view = EnrollmentView(page)
        page.controls.append(enrollment_view.build())
        page.update()
        await enrollment_view.run()

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

    enroll_btn = ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(ft.Icons.PERSON_ADD_ROUNDED, color="#FFFFFF", size=24),
                ft.Text(
                    "تسجيل طالب  ✦  Register Student",
                    color="#FFFFFF",
                    size=18,
                    weight=ft.FontWeight.W_600,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        ),
        bgcolor="#5C35A0",
        border_radius=12,
        padding=ft.Padding(32, 16, 32, 16),
        on_click=start_enrollment,
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
                ft.Container(height=12),
                enroll_btn,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        ),
        alignment=ft.Alignment(0, 0),
        expand=True,
        bgcolor="#1E1E1E",
    )
