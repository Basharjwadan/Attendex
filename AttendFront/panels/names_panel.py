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
    current_names = list(names or _DEFAULT_NAMES)

    header = ft.Text(
        "قائمة الحضور",
        size=20,
        weight=ft.FontWeight.BOLD,
        color="#FFFFFF",
        text_align=ft.TextAlign.RIGHT,
        rtl=True,
    )

    list_view = ft.ListView(
        controls=[_name_tile(n, i) for i, n in enumerate(current_names)],
        expand=True,
        spacing=6,
        padding=ft.padding.only(top=10),
    )

    def add_student(e):
        if name_input.value and name_input.value.strip():
            current_names.insert(0, name_input.value.strip())
            list_view.controls = [_name_tile(n, i) for i, n in enumerate(current_names)]
            list_view.update()
            name_input.value = ""
            name_input.update()

    name_input = ft.TextField(
        hint_text="اسم الطالب...", 
        expand=True, 
        rtl=True, 
        text_align=ft.TextAlign.RIGHT,
        dense=True,
        content_padding=10,
        border_color="#444444",
        focused_border_color="#4CAF50",
    )

    add_btn = ft.IconButton(
        icon=ft.Icons.ADD,
        icon_color="#FFFFFF",
        bgcolor="#4CAF50",
        on_click=add_student,
    )

    input_row = ft.Row(
        controls=[add_btn, name_input],
        spacing=10,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    return ft.Container(
        content=ft.Column(
            controls=[header, list_view, input_row],
            spacing=12,
            expand=True,
        ),
        expand=1,
        bgcolor="#1E1E1E",
        border_radius=12,
        padding=16,
    )
