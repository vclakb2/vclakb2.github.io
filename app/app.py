from flet import View, RouteChangeEvent, Image
from helpers.nav import Navbar
from helpers.dev_query import DevQueries
from helpers.misc_query import MiscQueries
from helpers.ai_query import AIQueries
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
                            ft.Image(src="/Users/akhilvaid/Desktop/Uchicago 2023/databases/vclakb2.github.io/app/resources/dallehomepage.jpg", width=500, height=500),
                            
                        ]
                    )
                ],
            )
        )
        if self.page.route == '/dev':
            self.page.views.append(
                View(
                    drawer = self.navbar,
                    route='/dev',
                    controls = [ft.AppBar(),DevQueries(self.connection)],
                )
            )

        if self.page.route == '/ai':
            self.page.views.append(
                View(
                    drawer = self.navbar,
                    route='/ai',
                    controls = [ft.AppBar(),AIQueries(self.connection)],
                )
            )
        if self.page.route == '/misc':
            self.page.views.append(
                View(
                    drawer = self.navbar,
                    route='/misc',
                    controls = [ft.AppBar(),MiscQueries(self.connection)],
                )
            )

        self.page.update()

    def view_pop(self, e: ft.ViewPopEvent):
        self.page.views.pop()
        top_view : View = self.page.views[-1]
        self.page.go(top_view.route)