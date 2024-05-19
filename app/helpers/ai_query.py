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
        lv = ft.ListView(expand=0, spacing=20, padding=20, auto_scroll=False,  height=600)
        lv.controls.append(ft.Column(
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
                            "AI Stance of Java Developers who use AI to\n commit and Review changes", 
                            icon=ft.icons.INSIGHTS, 
                            style = ft.ButtonStyle(
                                bgcolor = "Orange",
                                color="White"
                            ),
                            on_click=self.java_dev_using_ai
                        ),
                        ft.FilledButton(
                            "AI Stance of \nNon-professional Developers who \n'Highly Trust' in AI accuracy", 
                            icon=ft.icons.INSIGHTS, 
                            style = ft.ButtonStyle(
                                bgcolor = "Teal",
                                color="White"
                            ),
                            on_click=self.non_prof_dev_trust_ai
                        ),
                        ft.FilledButton(
                            "AI stance of American\n Developers who distrust or \nHighly distrust accuracy of AI tools", 
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
        ))
        return lv
    

    def _build_table_static(self, cols, rows, attr):
       return ft.Column(
           controls= [
                ft.Divider(thickness=1),
                ft.Text(attr, size ="20"),
                ft.DataTable(
                    border=ft.border.all(2, "white"),
                    border_radius=10,
                    columns=cols,
                    rows= rows
                )
           ]
       )
       

    # Helper method to build a table from a query output
    def _build_table(self, cols, rows):
        lv = ft.ListView(expand=0, spacing=20, padding=20, auto_scroll=False,  height=400)
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

        attributes = [
            'projectPlanning',
            'learnAboutCodeBase',
            'documentingCode',
            'writingCode',
            'debuggingAndGettingHelp',
            'testingCode',
            'commitingAndReviewingChange',
            'deploymentAndMonitoring',
            'collaboratingWithTeammates'
        ]

        tables = []

        for attribute in attributes:
            query = f"""
            SELECT
                ind.industry,
                SUM(CASE WHEN wf.{attribute} = 'NOT USING' THEN 1 ELSE 0 END) AS {attribute}_NOT_USING,
                SUM(CASE WHEN wf.{attribute} = 'INTERESTED' THEN 1 ELSE 0 END) AS {attribute}_INTERESTED,
                SUM(CASE WHEN wf.{attribute} = 'USING' THEN 1 ELSE 0 END) AS {attribute}_USING,
                SUM(CASE WHEN wf.{attribute} IS NULL THEN 1 ELSE 0 END) AS {attribute}_NULL
            FROM
                Developer AS dev
            JOIN
                AIDevWorkflowUse AS wf ON dev.devID = wf.devID
            JOIN
                Industry AS ind ON dev.industry = ind.industry
            GROUP BY
                ind.industry;
            """

            cursor.execute(query)
            result = cursor.fetchall()

            cols_text = [
                'industry',
                f'NOT USING (%)',
                f'INTERESTED (%)',
                f'USING (%)',
                f'NULL (%)',
            ]
            cols = [ft.DataColumn(ft.Text(i)) for i in cols_text]

            rows = []
            for row in result:
                # print(row)
                industry = row[0]
                not_using = row[1]
                interested = row[2]
                using = row[3]
                null = row[4]
                total = not_using + interested + using + null
                
                not_using_percent = (not_using / total) * 100 if total > 0 else 0
                interested_percent = (interested / total) * 100 if total > 0 else 0
                using_percent = (using / total) * 100 if total > 0 else 0
                null_percent = (null / total) * 100 if total > 0 else 0

                cells = [
                ft.DataCell(ft.Text(industry)),
                ft.DataCell(
                    ft.Row([
                        ft.Text(f"{not_using} ", color="red"),
                        ft.Text(f"({not_using_percent:.2f}%)", color=ft.colors.RED_100)
                    ])
                ),
                ft.DataCell(
                    ft.Row([
                        ft.Text(f"{interested} ", color="blue"),
                        ft.Text(f"({interested_percent:.2f}%)", color=ft.colors.LIGHT_BLUE_300)
                    ])
                ),
                ft.DataCell(
                    ft.Row([
                        ft.Text(f"{using} ", color="green"),
                        ft.Text(f"({using_percent:.2f}%)", color=ft.colors.LIGHT_GREEN_300)
                    ])
                ),
                ft.DataCell(
                    ft.Row([
                        ft.Text(f"{null} ", color="grey"),
                        ft.Text(f"({null_percent:.2f}%)", color=ft.colors.ORANGE_300)
                    ])
                )
            ]
                rows.append(ft.DataRow(cells))

            tables.append(self._build_table_static(cols, rows, attribute))
    
        self.tasks.controls = tables
        self.update()


    def java_dev_using_ai(self, e):
        cursor = self.connection.cursor()
        cols_text = ['stance', 'count']
        cols = [ft.DataColumn(ft.Text(i)) for i in cols_text]

        query = """
        SELECT s.stance, COUNT(d.devID) as count
        FROM Developer AS d
        JOIN AIStance AS s ON d.devID = s.devID
        JOIN AIDevWorkflowUse AS w ON d.devID = w.devID
        JOIN Uses as u ON d.devId = u.devId
        WHERE u.technologyName = 'Java'
        AND w.commitingAndReviewingChange = 'USING'
        AND s.stance IN ('Very favorable', 'Favorable', 'Indifferent', 'Unfavorable', 'Unsure', 'NA')
        GROUP BY s.stance
        UNION ALL
        SELECT 'Total', COUNT(d.devID) as count
        FROM Developer AS d
        JOIN AIStance AS s ON d.devID = s.devID
        JOIN AIDevWorkflowUse AS w ON d.devID = w.devID
        JOIN Uses as u ON d.devId = u.devId
        WHERE u.technologyName = 'Java'
        AND w.commitingAndReviewingChange = 'USING';
        """

        cursor.execute(query)
        result = cursor.fetchall()

        rows = []
        for i in result:
            cells = [ft.DataCell(ft.Text(str(j))) for j in i]
            rows.append(ft.DataRow(cells))

        self.tasks.controls = [self._build_table(cols, rows)]
        self.update()



    def non_prof_dev_trust_ai(self, e):
        cursor = self.connection.cursor()
        cols_text = ['stance', 'count']
        cols = [ft.DataColumn(ft.Text(i)) for i in cols_text]

        query = """
        SELECT s.stance, COUNT(d.devID) as count
        FROM Developer AS d
        JOIN AIStance AS s ON d.devID = s.devID
        WHERE d.isDeveloper = True 
        AND s.trustinAccuracyOfAITools = 'Highly trust'
        GROUP BY s.stance
        UNION ALL
        SELECT 'Total', COUNT(d.devID) as count
        FROM Developer AS d
        JOIN AIStance AS s ON d.devID = s.devID
        WHERE d.isDeveloper = True 
        AND s.trustinAccuracyOfAITools = 'Highly trust';
        """

        cursor.execute(query)
        result = cursor.fetchall()

        rows = []
        for i in result:
            cells = [ft.DataCell(ft.Text(str(j))) for j in i]
            rows.append(ft.DataRow(cells))

        self.tasks.controls = [self._build_table(cols, rows)]
        self.update()

    def usa_dev_distrust_ai(self, e):
        cursor = self.connection.cursor()
        cols_text = ['stance', 'count']
        cols = [ft.DataColumn(ft.Text(i)) for i in cols_text]

        query = """
        SELECT s.stance, COUNT(d.devID) as count
        FROM Developer AS d
        JOIN AIStance AS s ON d.devID = s.devID
        WHERE d.countryName = 'United States of America' 
        AND (s.trustinAccuracyOfAITools = 'Somewhat distrust' OR s.trustinAccuracyOfAITools = 'Highly distrust')
        GROUP BY s.stance
        UNION ALL
        SELECT 'Total', COUNT(d.devID) as count
        FROM Developer AS d
        JOIN AIStance AS s ON d.devID = s.devID
        WHERE d.countryName = 'United States of America' 
        AND (s.trustinAccuracyOfAITools = 'Somewhat distrust' OR s.trustinAccuracyOfAITools = 'Highly distrust');
        """

        cursor.execute(query)
        result = cursor.fetchall()

        rows = []
        for i in result:
            cells = [ft.DataCell(ft.Text(str(j))) for j in i]
            rows.append(ft.DataRow(cells))

        self.tasks.controls = [self._build_table(cols, rows)]
        self.update()
