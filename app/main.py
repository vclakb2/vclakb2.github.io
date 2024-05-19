import flet as ft
from flet import View, RouteChangeEvent
import mysql.connector
from app import DevAI

myConnection = mysql.connector.connect(user = 'avnadmin',
        password = 'AVNS_978XTtRvLUWrowzEW-D',
        host = 'mysql-3b07a8e5-db-developer.f.aivencloud.com',
        port = 13447,
        database = 'DevAI'
    )

def main(page: ft.Page):
    page.title = "DevAI"
    page.scroll = 'auto'
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_width = 1300      
    page.window_height = 800       
    page.window_resizable = True 
    page.theme = ft.theme.Theme(
        font_family="Verdana")
    page.theme.page_transitions.windows = "cupertino"
    page.fonts = {
        "Pacifico": "/Pacifico-Regular.ttf"
    }
    page.bgcolor = ft.colors.BLUE_GREY_200
    page.update()
    app = DevAI(page, myConnection)


ft.app(target=main)

