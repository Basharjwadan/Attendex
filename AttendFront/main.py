"""
main.py – Entry point for AttendFlet.
"""

import flet as ft
from views.root_view import build_root_view


async def main(page: ft.Page):
    page.title = "AttendFlet – نظام الحضور"
    page.padding = 0
    page.spacing = 0
    page.bgcolor = "#1E1E1E"

    root_view = build_root_view(page)
    page.add(root_view)


ft.run(main)