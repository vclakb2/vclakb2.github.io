from flet import View, RouteChangeEvent
from helpers.nav import Navbar
from helpers.query import Queries
import flet as ft
class DevAI:
    def __init__(self, page, connection):
        self.page = page
        self.connection = connection
        self.navbar = Navbar(self.page).build()

        self.page.on_route_change = self.route_change
        self.page.on_view_pop = self.view_pop
        self.page.go(self.page.route)

    def route_change(self, e: RouteChangeEvent) -> None:
        self.page.views.clear()
        self.page.views.append(
            View(
                horizontal_alignment= ft.CrossAxisAlignment.CENTER,
                vertical_alignment= ft.CrossAxisAlignment.CENTER,
                drawer = self.navbar,
                route='/',
                controls = [
                    ft.AppBar(),
                    ft.Column (
                        horizontal_alignment= ft.CrossAxisAlignment.CENTER,
                        controls = [
                            ft.Text(value="Welcome to DevAI", size = 30),
                            ft.Text(value="Get the best insights about modern developers and AI!", size=20),
                            ft.Text(value="Click the hamburger to see what insights we have available", size=15),
                        ]
                    )
                ],
            )
        )

        if self.page.route == '/store':
            self.page.views.append(
                View(
                    drawer = self.navbar,
                    route='/store',
                    controls = [ft.AppBar(),Queries(self.connection)],
                )
            )

        self.page.update()

    def view_pop(self, e: ft.ViewPopEvent):
        self.page.views.pop()
        top_view : View = self.page.views[-1]
        self.page.go(top_view.route)