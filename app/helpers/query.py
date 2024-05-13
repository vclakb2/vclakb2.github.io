import flet as ft

class Queries(ft.UserControl):
    def __init__(self, connection):
        super().__init__()
        self.connection = connection

    def build(self):
        self.tasks = ft.Column()

        return ft.Column(
            width=1200,
            #horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Row(
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
                        ft.FilledButton(
                            "Get Technology", 
                            icon=ft.icons.ADD, 
                            style =  ft.ButtonStyle(
                                bgcolor = "Purple"
                            ),
                            on_click=self.get_tech
                        ),
                    ],
                ),
                ft.Divider(height=9, thickness=3),
                ft.Text("Output:"),
                self.tasks,
            ],
        )
    def _build_table(self, cols, rows):
        return ft.DataTable(
                border=ft.border.all(2, "white"),
                border_radius=10,
                columns=cols,
                rows= rows
            )

    def get_cols(self, cursor, name):
        query = f"""select *
            from INFORMATION_SCHEMA.COLUMNS
            where TABLE_NAME={name}"""
        cursor.execute(query)
        return cursor.fetchone()

    def get_dev_country(self, e):
        cursor = self.connection.cursor()
        # Define columns to retrieve 
        cols_text = ["devID", "countryName", "stance", "company"]
        # Format columns to flet datatype
        cols = [ft.DataColumn(ft.Text(i)) for i in cols_text]

        # Query based on column names defined
        query = f"""
        SELECT {', '.join(item for item in cols_text)} FROM Developer;
        """
        cursor.execute(query)
        result = cursor.fetchall()

        # Format results into flet rows
        rows = []
        for i in result:
            cells = []
            for j in i:
                cells.append(ft.DataCell(ft.Text(j)))
            rows.append(ft.DataRow(cells))

        self.tasks.controls = [self._build_table(cols, rows)]
        
        self.update()

    def get_countries(self, e):
        cursor = self.connection.cursor()
        # Define columns to retrieve 
        cols_text = ['name', 'population', 'currency', 'status']
        # Format columns to flet datatype
        cols = [ft.DataColumn(ft.Text(i)) for i in cols_text]

        # Query based on column names defined
        query = f"""
        SELECT {', '.join(item for item in cols_text)} FROM Country;
        """
        cursor.execute(query)
        result = cursor.fetchall()

        # Format results into flet rows
        rows = []
        for i in result:
            cells = []
            for j in i:
                cells.append(ft.DataCell(ft.Text(j)))
            rows.append(ft.DataRow(cells))

        self.tasks.controls = [self._build_table(cols, rows)]
        self.update()
    
    def get_tech(self, e):
        cursor = self.connection.cursor()
        # Define columns to retrieve 
        cols_text = ['technologyName', 'dateOfPublication', 'technologyType']
        # Format columns to flet datatype
        cols = [ft.DataColumn(ft.Text(i)) for i in cols_text]

        # Query based on column names defined
        query = f"""
        SELECT {', '.join(item for item in cols_text)} FROM Technology;
        """
        cursor.execute(query)
        result = cursor.fetchall()

        # Format results into flet rows
        rows = []
        for i in result:
            cells = []
            for j in i:
                cells.append(ft.DataCell(ft.Text(j)))
            rows.append(ft.DataRow(cells))

        self.tasks.controls = [self._build_table(cols, rows)]
        self.update()

    def get_comp(self, e):
        cursor = self.connection.cursor()
        # Define columns to retrieve 
        cols_text = ['companyName', 'industry', 'marketShare']
        # Format columns to flet datatype
        cols = [ft.DataColumn(ft.Text(i)) for i in cols_text]

        # Query based on column names defined
        query = f"""
        SELECT {', '.join(item for item in cols_text)} FROM Company;
        """
        cursor.execute(query)
        result = cursor.fetchall()

        # Format results into flet rows
        rows = []
        for i in result:
            cells = []
            for j in i:
                cells.append(ft.DataCell(ft.Text(j)))
            rows.append(ft.DataRow(cells))

        self.tasks.controls = [self._build_table(cols, rows)]
        self.update()
