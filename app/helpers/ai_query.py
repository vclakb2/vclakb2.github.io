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
                            "AI Use by Industry", 
                            icon=ft.icons.INSIGHTS, 
                            style = ft.ButtonStyle(
                                bgcolor = "Purple",
                                color="White"
                            ),
                            on_click=self.ai_use_diff_for_industries
                        ),
                        ft.FilledButton(
                            "Java Developers using AI", 
                            icon=ft.icons.INSIGHTS, 
                            style = ft.ButtonStyle(
                                bgcolor = "Orange",
                                color="White"
                            ),
                            on_click=self.java_dev_using_ai
                        ),
                        ft.FilledButton(
                            "Non-professional Developers trusting AI", 
                            icon=ft.icons.INSIGHTS, 
                            style = ft.ButtonStyle(
                                bgcolor = "Teal",
                                color="White"
                            ),
                            on_click=self.non_prof_dev_trust_ai
                        ),
                        ft.FilledButton(
                            "USA Developers distrusting AI", 
                            icon=ft.icons.INSIGHTS, 
                            style = ft.ButtonStyle(
                                bgcolor = "Brown",
                                color="White"
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
        lv = ft.ListView(expand=0, spacing=10, padding=20, auto_scroll=False,  height=400)
        lv.controls.append(ft.DataTable(
                border=ft.border.all(2, "white"),
                border_radius=10,
                columns=cols,
                rows= rows
            ))
        return lv


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
