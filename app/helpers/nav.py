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
                    label="Home",
                    icon=ft.icons.HOME_OUTLINED,
                    selected_icon_content=ft.Icon(ft.icons.HOME),
                ),
                ft.Divider(thickness=2),
                ft.NavigationDrawerDestination(
                    icon_content=ft.Icon(ft.icons.PERSON_2_OUTLINED),
                    label="Developer Insights",
                    selected_icon=ft.icons.PERSON_2_ROUNDED,
                ),
                ft.Divider(thickness=2),
                ft.NavigationDrawerDestination(
                    icon_content=ft.Icon(ft.icons.PHONE_OUTLINED),
                    label="Item 3",
                    selected_icon=ft.icons.PHONE,
                ),
            ],
        )