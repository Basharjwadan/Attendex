"""
main.py – Entry point for AttendFlet camera application.
"""

import flet as ft
from views.root_view import build_root_view


async def main(page: ft.Page):
    page.title = "AttendFlet – نظام الحضور"
    page.padding = 0
    page.spacing = 0

    root_view = build_root_view(page)
    page.controls.append(root_view)
    page.update()


ft.run(main)