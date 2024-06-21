import flet as ft
from app import BliBankApp

def main(page: ft.Page):
    '''
    Função principal que inicializa o aplicativo BliBank.
    '''

    app = BliBankApp()
    app.inicial(page)

ft.app(target=main)
