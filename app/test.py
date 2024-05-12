import flet as ft
import mysql.connector

def main(page: ft.Page):
    myConnection = mysql.connector.connect( 
        user = 'avnadmin',
        password = 'AVNS_978XTtRvLUWrowzEW-D',
        host = 'mysql-3b07a8e5-db-developer.f.aivencloud.com',
        post = '13447',
        database = 'DevAI'
    )
    
    def add_clicked(e):
        cursor = myConnection.cursor()
        results = []

        query1 = """
        SELECT * FROM Developer
        """
        cursor.execute(query1)
        results.append(cursor.fetchall())
        page.add(ft.Checkbox(label=new_task.value))
        new_task.value = results[0]
        page.update()

    new_task = ft.TextField(hint_text="What's needs to be done?")

    page.add(ft.FloatingActionButton(icon=ft.icons.ADD, on_click=add_clicked))

ft.app(target=main)
