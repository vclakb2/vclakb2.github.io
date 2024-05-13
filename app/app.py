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
                drawer = self.navbar,
                route='/',
                controls = [
                ft.AppBar(),
                ft.Text(value="Home", size = 30),
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