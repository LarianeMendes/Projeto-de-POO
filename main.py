import flet as ft
from app import BliBankApp

def main(page: ft.Page):
    app = BliBankApp()
    app.inicial(page)

ft.app(target=main)
