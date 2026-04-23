"""
main.py – Entry point for AttendFlet camera application.
"""

import flet as ft
from app import AttendApp


async def main(page: ft.Page):
    app = AttendApp(page)
    await app.run()


ft.run(main)