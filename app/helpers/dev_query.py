import flet as ft

class DevQueries(ft.UserControl):
    """
    The class representing the query page of the app
    """
    def __init__(self, connection):
        super().__init__()
        self.connection = connection
        self.conditions = None

    def build(self):
        self.tasks = ft.Column(width=1200,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER)

        return ft.Column(
            width=1200,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text("Developer Insights", size = 20),
                ft.Divider(thickness=2),
                ft.Row(
                    # Define the tabs for queries here
                    # The on click must point to the correct function
                    controls=[
                        ft.FilledButton(
                            "Get Developers", 
                            icon=ft.icons.ADD, 
                            style =  ft.ButtonStyle(
                                bgcolor = "Red"
                            ), 
                            on_click=self.get_dev_country
                        ),
                        ft.FilledButton(
                            "Get Countries", 
                            icon=ft.icons.ADD, 
                            style =  ft.ButtonStyle(
                                bgcolor = "Blue"
                            ), 
                            on_click=self.get_countries
                        ),
                        ft.FilledButton(
                            "Get Company", 
                            icon=ft.icons.ADD, 
                            style =  ft.ButtonStyle(
                                bgcolor = "Green"
                            ),
                            on_click=self.get_comp
                        ),
                    ],
                ),
                ft.Divider(height=9, thickness=3),
                ft.Text("Output:"),
                self.tasks,
            ],
        )
    

    # Heler method to build a table from a query output
    def _build_table(self, cols, rows):
        lv = ft.ListView(expand=0, spacing=10, padding=20, auto_scroll=False,  height=300)
        lv.controls.append(ft.DataTable(
                border=ft.border.all(2, "white"),
                border_radius=10,
                columns=cols,
                rows= rows
            ))
        return lv


    # Function that specifies subquert behavior
    # In this case e.data represents the button index
    # We alter the conditon when we want to provide a subquery
    # Note a condition can also be a order by or group by if necessary
    def select_button_dev(self, e):
        ind = e.data
        if ind == "0":
            self.conditions = None
        elif ind == "1":
            self.conditions = "WHERE countryName = 'testCountry'"
        elif ind == "2":
            print("changing")
            self.conditions = "WHERE countryName = 'bruh'"
        else:
            self.conditions = None
        print(self.conditions)
        self.get_dev_country(e)


    # Function representing a query tab output
    def get_dev_country(self, e):
        cursor = self.connection.cursor()
        # Define columns to retrieve 
        cols_text = ["devID", "countryName", "stance", "company"]        

        # Query based on column names defined
        query = f"""
        SELECT {', '.join(item for item in cols_text)} FROM Developer
        """
        
        # If a condition exists then add it to the query
        if self.conditions != None:
            query += self.conditions

        # Reset a condition after querying
        self.conditions = None


        cursor.execute(query)
        result = cursor.fetchall()

        # Format columns to flet output
        cols = [ft.DataColumn(ft.Text(i)) for i in cols_text] 

        # Format results into flet rows
        rows = []
        for i in result:
            cells = []
            for j in i:
                cells.append(ft.DataCell(ft.Text(j)))
            rows.append(ft.DataRow(cells))
        
        # Add table output to page
        self.tasks.controls = [self._build_table(cols, rows)]

        # Create subquery button
        butt = ft.CupertinoSegmentedButton(
                selected_index=0 if e.data == '' else int(e.data),
                selected_color=ft.colors.BLUE,
                on_change=self.select_button_dev,
                controls=[
                    ft.Text("All"),
                    ft.Container(
                        padding=ft.padding.symmetric(0, 30),
                        content=ft.Text("Country = testCountry"),
                    ),
                    ft.Container(
                        padding=ft.padding.symmetric(0, 10),
                        content=ft.Text("Country = bruh"),
                    ),
                ],
            )

        # Add subquery button to page
        self.tasks.controls.append(butt)
        self.update()

    def get_countries(self, e):
        cursor = self.connection.cursor()
        # Define columns to retrieve 
        cols_text = ['name', 'population', 'currency', 'status']
        # Format columns to flet datatype
        cols = [ft.DataColumn(ft.Text(i)) for i in cols_text]

        # Query based on column names defined
        query = f"""
        SELECT {', '.join(item for item in cols_text)} FROM Country
        """

        if self.conditions != None:
            query += self.conditions

        self.conditions = None

        cursor.execute(query)
        result = cursor.fetchall()

        # Format results into flet rows
        rows = []
        for i in result:
            cells = []
            for j in i:
                cells.append(ft.DataCell(ft.Text(j)))
            rows.append(ft.DataRow(cells))

        # Add table to output
        self.tasks.controls = [self._build_table(cols, rows)]


        # Switch function that called when the switch is changed
        def switch(e):
            if e.data == 'true':
                e.data = True
                self.conditions = "ORDER BY population ASC"
            else:
                e.data = False
                self.conditions = "ORDER BY population DESC"
            self.get_countries(e)


        # Switch object for our subquery
        s = ft.Switch(
            label="Ordered: ASC",
            value=True if e.data == '' or e.data == True else False,
            thumb_color={ft.MaterialState.SELECTED: ft.colors.BLUE},
            track_color=ft.colors.YELLOW,
            focus_color=ft.colors.PURPLE,
            on_change = switch
        )

        # Add subquery to page
        self.tasks.controls.append(s)
        self.update()


    def get_comp(self, e):
        cursor = self.connection.cursor()
        # Define columns to retrieve 
        cols_text = ['companyName', 'industry', 'marketShare']
        # Format columns to flet datatype
        cols = [ft.DataColumn(ft.Text(i)) for i in cols_text]

        # Query based on column names defined
        query = f"""
        SELECT {', '.join(item for item in cols_text)} FROM Company
        """

        if self.conditions != None:
            query += self.conditions

        self.conditions = None

        cursor.execute(query)
        result = cursor.fetchall()

        # Format results into flet rows
        rows = []
        for i in result:
            cells = []
            for j in i:
                cells.append(ft.DataCell(ft.Text(j)))
            rows.append(ft.DataRow(cells))

        # Adds table to page
        self.tasks.controls = [self._build_table(cols, rows)]

        # Sets subquery to text field value
        def select(e):
            self.conditions = f"WHERE companyName = '{tb1.content.value}'"
            self.get_comp(e)

        # Creates a text input field
        tb1 = ft.Container(
            content = ft.TextField(label="Company Name"),
            width = 200,
        )

        # Button that submits text field
        b = ft.ElevatedButton(text="Submit", on_click=select)

        # Adds button and text field to page
        self.tasks.controls.append(tb1)
        self.tasks.controls.append(b)
        self.update()
