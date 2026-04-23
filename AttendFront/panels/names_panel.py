"""
names_panel.py – Student attendance names panel (RTL Arabic).
"""

import flet as ft

# Hardcoded Arabic student names for now
_DEFAULT_NAMES = [
    "أحمد محمد",
    "فاطمة علي",
    "عمر حسين",
    "مريم خالد",
    "يوسف إبراهيم",
    "نور الدين",
    "سارة عبد الله",
    "حسن أبو بكر",
    "ليلى عثمان",
    "خالد الرحمن",
]


def _name_tile(name: str, index: int) -> ft.Container:
    """Build a single name row with an index badge."""
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Text(
                    name,
                    size=16,
                    weight=ft.FontWeight.W_500,
                    color="#EEEEEE",
                    text_align=ft.TextAlign.RIGHT,
                    expand=True,
                    rtl=True,
                ),
                ft.Container(
                    content=ft.Text(
                        str(index + 1),
                        size=12,
                        color="#9E9E9E",
                        text_align=ft.TextAlign.CENTER,
                    ),
                    width=28,
                    height=28,
                    border_radius=14,
                    bgcolor="#333333",
                    alignment=ft.Alignment(0, 0),
                ),
            ],
            alignment=ft.MainAxisAlignment.END,
            spacing=10,
        ),
        padding=ft.padding.symmetric(horizontal=12, vertical=8),
        border_radius=8,
        bgcolor="#2A2A2A",
    )


def build_names_panel(names: list[str] | None = None) -> ft.Container:
    """Build the student names panel."""
    names = names or _DEFAULT_NAMES

    header = ft.Text(
        "قائمة الحضور",
        size=20,
        weight=ft.FontWeight.BOLD,
        color="#FFFFFF",
        text_align=ft.TextAlign.RIGHT,
        rtl=True,
    )

    name_tiles = [_name_tile(n, i) for i, n in enumerate(names)]

    list_view = ft.ListView(
        controls=name_tiles,
        expand=True,
        spacing=6,
        padding=ft.padding.only(top=10),
    )

    return ft.Container(
        content=ft.Column(
            controls=[header, list_view],
            spacing=12,
            expand=True,
        ),
        expand=1,
        bgcolor="#1E1E1E",
        border_radius=12,
        padding=16,
    )
