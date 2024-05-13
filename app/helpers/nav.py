import flet as ft

class Navbar(ft.UserControl):
    def __init__(self, page):
        self.page = page

    def navchange(self, e):
        if e.control.selected_index == 1:
            self.page.go('/store')
        else:
            self.page.go('/')
    def build(self):
        return ft.NavigationDrawer(
            on_change=self.navchange,
            controls=[
                ft.Container(height=12),
                ft.NavigationDrawerDestination(
                    label="Item 1",
                    icon=ft.icons.DOOR_BACK_DOOR_OUTLINED,
                    selected_icon_content=ft.Icon(ft.icons.DOOR_BACK_DOOR),
                ),
                ft.Divider(thickness=2),
                ft.NavigationDrawerDestination(
                    icon_content=ft.Icon(ft.icons.MAIL_OUTLINED),
                    label="Item 2",
                    selected_icon=ft.icons.MAIL,
                ),
                ft.Divider(thickness=2),
                ft.NavigationDrawerDestination(
                    icon_content=ft.Icon(ft.icons.PHONE_OUTLINED),
                    label="Item 3",
                    selected_icon=ft.icons.PHONE,
                ),
            ],
        )