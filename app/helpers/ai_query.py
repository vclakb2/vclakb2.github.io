import flet as ft

class AIQueries(ft.UserControl):
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
                ft.Text("AI Insights", size =20),
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
                        ft.FilledButton(
                            "AI Use by Industry", 
                            icon=ft.icons.INSIGHTS, 
                            style = ft.ButtonStyle(
                                bgcolor = "Purple"
                            ),
                            on_click=self.ai_use_diff_for_industries
                        ),
                        ft.FilledButton(
                            "Java Developers using AI", 
                            icon=ft.icons.INSIGHTS, 
                            style = ft.ButtonStyle(
                                bgcolor = "Orange"
                            ),
                            on_click=self.java_dev_using_ai
                        ),
                        ft.FilledButton(
                            "Non-professional Developers trusting AI", 
                            icon=ft.icons.INSIGHTS, 
                            style = ft.ButtonStyle(
                                bgcolor = "Teal"
                            ),
                            on_click=self.non_prof_dev_trust_ai
                        ),
                        ft.FilledButton(
                            "USA Developers distrusting AI", 
                            icon=ft.icons.INSIGHTS, 
                            style = ft.ButtonStyle(
                                bgcolor = "Brown"
                            ),
                            on_click=self.usa_dev_distrust_ai
                        ),
                    ],
                ),
                ft.Divider(height=9, thickness=3),
                ft.Text("Output:"),
                self.tasks,
            ],
        )
    

    # Helper method to build a table from a query output
    def _build_table(self, cols, rows):
        return ft.DataTable(
                border=ft.border.all(2, "white"),
                border_radius=10,
                columns=cols,
                rows= rows
            )


    # Function that specifies subquery behavior
    def select_button_dev(self, e):
        ind = e.data
        if ind == "0":
            self.conditions = None
        elif ind == "1":
            self.conditions = "WHERE countryName = 'testCountry'"
        elif ind == "2":
            self.conditions = "WHERE countryName = 'bruh'"
        else:
            self.conditions = None
        self.get_dev_country(e)


    # Function representing a query tab output
    def get_dev_country(self, e):
        cursor = self.connection.cursor()
        cols_text = ["devID", "countryName", "stance", "company"]        

        query = f"""
        SELECT {', '.join(item for item in cols_text)} FROM Developer
        """
        
        if self.conditions != None:
            query += self.conditions

        self.conditions = None

        cursor.execute(query)
        result = cursor.fetchall()

        cols = [ft.DataColumn(ft.Text(i)) for i in cols_text]
        rows = []
        for i in result:
            cells = [ft.DataCell(ft.Text(j)) for j in i]
            rows.append(ft.DataRow(cells))
        
        self.tasks.controls = [self._build_table(cols, rows)]

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

        self.tasks.controls.append(butt)
        self.update()

    def get_countries(self, e):
        cursor = self.connection.cursor()
        cols_text = ['name', 'population', 'currency', 'status']
        cols = [ft.DataColumn(ft.Text(i)) for i in cols_text]

        query = f"""
        SELECT {', '.join(item for item in cols_text)} FROM Country
        """

        if self.conditions != None:
            query += self.conditions

        self.conditions = None

        cursor.execute(query)
        result = cursor.fetchall()

        rows = []
        for i in result:
            cells = [ft.DataCell(ft.Text(j)) for j in i]
            rows.append(ft.DataRow(cells))

        self.tasks.controls = [self._build_table(cols, rows)]

        def switch(e):
            if e.data == 'true':
                self.conditions = "ORDER BY population ASC"
            else:
                self.conditions = "ORDER BY population DESC"
            self.get_countries(e)

        s = ft.Switch(
            label="Ordered: ASC",
            value=True if e.data == '' or e.data == 'true' else False,
            thumb_color={ft.MaterialState.SELECTED: ft.colors.BLUE},
            track_color=ft.colors.YELLOW,
            focus_color=ft.colors.PURPLE,
            on_change=switch
        )

        self.tasks.controls.append(s)
        self.update()

    def get_comp(self, e):
        cursor = self.connection.cursor()
        cols_text = ['companyName', 'industry', 'marketShare']
        cols = [ft.DataColumn(ft.Text(i)) for i in cols_text]

        query = f"""
        SELECT {', '.join(item for item in cols_text)} FROM Company
        """

        if self.conditions != None:
            query += self.conditions

        self.conditions = None

        cursor.execute(query)
        result = cursor.fetchall()

        rows = []
        for i in result:
            cells = [ft.DataCell(ft.Text(j)) for j in i]
            rows.append(ft.DataRow(cells))

        self.tasks.controls = [self._build_table(cols, rows)]

        def select(e):
            self.conditions = f"WHERE companyName = '{tb1.content.value}'"
            self.get_comp(e)

        tb1 = ft.Container(
            content=ft.TextField(label="Company Name"),
            width=200,
        )

        b = ft.ElevatedButton(text="Submit", on_click=select)

        self.tasks.controls.append(tb1)
        self.tasks.controls.append(b)
        self.update()

    # New queries added below

    def ai_use_diff_for_industries(self, e):
        cursor = self.connection.cursor()
        cols_text = ['industry', 'devID', 'projectPlanning', 'writingCode']
        cols = [ft.DataColumn(ft.Text(i)) for i in cols_text]

        query = """
        SELECT d.industry, a.devID, a.projectPlanning, a.writingCode
        FROM AIDevWorkflowUse AS a
        JOIN Developer AS d ON a.devID = d.devID
        JOIN Company AS c ON d.company = c.companyName
        """

        cursor.execute(query)
        result = cursor.fetchall()

        rows = []
        for i in result:
            cells = [ft.DataCell(ft.Text(j)) for j in i]
            rows.append(ft.DataRow(cells))

        self.tasks.controls = [self._build_table(cols, rows)]
        self.update()

    def java_dev_using_ai(self, e):
        cursor = self.connection.cursor()
        cols_text = ['devID', 'stance', 'commitAndReview']
        cols = [ft.DataColumn(ft.Text(i)) for i in cols_text]

        query = """
        SELECT d.devID, s.stance, w.commitingAndReviewingChange
        FROM Developer AS d
        JOIN AIStance AS s ON d.devID = s.devID
        JOIN AIDevWorkflowUse AS w ON d.devID = w.devID
        WHERE d.devType = 'Java Developer' AND w.commitingAndReviewingChange = 'Strongly'
        """

        cursor.execute(query)
        result = cursor.fetchall()

        rows = []
        for i in result:
            cells = [ft.DataCell(ft.Text(j)) for j in i]
            rows.append(ft.DataRow(cells))

        self.tasks.controls = [self._build_table(cols, rows)]
        self.update()

    def non_prof_dev_trust_ai(self, e):
        cursor = self.connection.cursor()
        cols_text = ['devID', 'stance', 'isProfessional']
        cols = [ft.DataColumn(ft.Text(i)) for i in cols_text]

        query = """
        SELECT d.devID, s.stance, d.isProfessional
        FROM Developer AS d
        JOIN AIStance AS s ON d.devID = s.devID
        WHERE d.isProfessional = 'No' AND s.trustinAccuracyOfAITools = 'Strongly'
        """

        cursor.execute(query)
        result = cursor.fetchall()

        rows = []
        for i in result:
            cells = [ft.DataCell(ft.Text(j)) for j in i]
            rows.append(ft.DataRow(cells))

        self.tasks.controls = [self._build_table(cols, rows)]
        self.update()

    def usa_dev_distrust_ai(self, e):
        cursor = self.connection.cursor()
        cols_text = ['countryName', 'devID', 'stance']
        cols = [ft.DataColumn(ft.Text(i)) for i in cols_text]

        query = """
        SELECT d.countryName, d.devID, s.stance
        FROM Developer AS d
        JOIN AIStance AS s ON d.devID = s.devID
        WHERE d.countryName = 'USA' AND s.trustinAccuracyOfAITools = 'Distrust'
        """

        cursor.execute(query)
        result = cursor.fetchall()

        rows = []
        for i in result:
            cells = [ft.DataCell(ft.Text(j)) for j in i]
            rows.append(ft.DataRow(cells))

        self.tasks.controls = [self._build_table(cols, rows)]
        self.update()
