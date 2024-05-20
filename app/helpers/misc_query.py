import flet as ft

class MiscQueries(ft.UserControl):
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
                ft.Text("Miscellaneous Insights", size =20),
                ft.Divider(thickness=2),
                ft.Row(
                    # Define the tabs for queries here
                    # The on click must point to the correct function
                    controls=[
                        ft.FilledButton(
                            "Education % by Country", 
                            icon=ft.icons.DATA_THRESHOLDING_ROUNDED, 
                            style =  ft.ButtonStyle(
                                bgcolor = "Red",
                                color = "White"
                            ), 
                            on_click=self.country_edu
                        ),
                        ft.FilledButton(
                            "Avg wage per Country", 
                            icon=ft.icons.DATA_THRESHOLDING_ROUNDED, 
                            style =  ft.ButtonStyle(
                                bgcolor = "Blue",
                                color= "White"
                            ), 
                            on_click=self.country_wage
                        ),
                        ft.FilledButton(
                            "Avg Wage by Technology", 
                            icon=ft.icons.DATA_THRESHOLDING_ROUNDED, 
                            style =  ft.ButtonStyle(
                                bgcolor = "Green",
                                color = "White"
                            ), 
                            on_click=self.tech_wage
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
        lv = ft.ListView(expand=0, spacing=10, padding=20, auto_scroll=False,  height=400)
        lv.controls.append(ft.DataTable(
                border=ft.border.all(2, "white"),
                border_radius=10,
                columns=cols,
                rows= rows
            ))
        return lv


   
    def country_edu(self, e):
        cursor = self.connection.cursor()
        # Define columns to retrieve 
        cols_text = ['Country', '%Primary', '%Secondary', '%Some Col.', '%Assoc.', '%Bach.', '%Mast.', '%PHD+']
        # Format columns to flet datatype
        cols = [ft.DataColumn(ft.Text(i)) for i in cols_text]

        # Query based on column names defined
        text = "Education by Country"
        query = f"""
        SELECT 
            countryName,
            ROUND(COUNT(CASE WHEN educationLevel = \'Primary/Elementary School\' THEN 1 END)/COUNT(*), 2) AS Elementary,
            ROUND(COUNT(CASE WHEN educationLevel  = \'Secondary/High School\' THEN 1 END)/COUNT(*)* 100, 2) AS \'High School\',
            ROUND(COUNT(CASE WHEN educationLevel  = \'Some college/university study without earning a degree\' THEN 1 END) / COUNT(*)* 100, 2) AS \'Some College/No degree\',
            ROUND(COUNT(CASE WHEN educationLevel  = \'Associate degree (A.A., A.S., etc.)\' THEN 1 END) / COUNT(*)* 100, 2) AS \'Associates\',
            ROUND(COUNT(CASE WHEN educationLevel  = \'Bachelor\\\'s degree (B.A., B.S., B.Eng., etc.)\' THEN 1 END) / COUNT(*)* 100, 2) AS \'Bachelors\',
            ROUND(COUNT(CASE WHEN educationLevel  = \'Master\\\'s degree (M.A., M.S., M.Eng., MBA, etc.)\' THEN 1 END) / COUNT(*)* 100, 2) AS \'Masters\',
            ROUND(COUNT(CASE WHEN educationLevel  = \'Professional degree (JD, MD, Ph.D, Ed.D, etc.)\' THEN 1 END) / COUNT(*)* 100, 2) AS \'PHD+\'
        FROM 
            Developer
        GROUP BY 
            countryName
        ORDER BY 
            COUNT(educationLevel) DESC;
        """

        if self.conditions is not None:
            text = "Education for " + self.conditions[len("HAVING countryName = "):]
            query = f"""
            SELECT 
                countryName,
                ROUND(COUNT(CASE WHEN educationLevel = \'Primary/Elementary School\' THEN 1 END)/COUNT(*) * 100, 2) AS Elementary,
                ROUND(COUNT(CASE WHEN educationLevel  = \'Secondary/High School\' THEN 1 END)/COUNT(*)* 100, 2) AS \'High School\',
                ROUND(COUNT(CASE WHEN educationLevel  = \'Some college/university study without earning a degree\' THEN 1 END) / COUNT(*)* 100, 2) AS \'Some College/No degree\',
                ROUND(COUNT(CASE WHEN educationLevel  = \'Associate degree (A.A., A.S., etc.)\' THEN 1 END) / COUNT(*)* 100, 2) AS \'Associates\',
                ROUND(COUNT(CASE WHEN educationLevel  = \'Bachelor\\\'s degree (B.A., B.S., B.Eng., etc.)\' THEN 1 END) / COUNT(*)* 100, 2) AS \'Bachelors\',
                ROUND(COUNT(CASE WHEN educationLevel  = \'Master\\\'s degree (M.A., M.S., M.Eng., MBA, etc.)\' THEN 1 END) / COUNT(*)* 100, 2) AS \'Masters\',
                ROUND(COUNT(CASE WHEN educationLevel  = \'Professional degree (JD, MD, Ph.D, Ed.D, etc.)\' THEN 1 END) / COUNT(*)* 100, 2) AS \'PHD+\'
            FROM 
                Developer
            GROUP BY 
                countryName
            {self.conditions}
            ORDER BY 
                countryName
            """
            print(query)

        self.conditions = None

        cursor.execute(query)
        result = cursor.fetchall()

        # Format results into flet rows with colored text
        rows = []
        for row in result:
            cells = [
                ft.DataCell(ft.Text(row[0])),  # Country
                ft.DataCell(ft.Text(f"{row[1]:.2f}", color="red")),  # Primary
                ft.DataCell(ft.Text(f"{row[2]:.2f}", color="blue")),  # Secondary
                ft.DataCell(ft.Text(f"{row[3]:.2f}", color="green")),  # Some College
                ft.DataCell(ft.Text(f"{row[4]:.2f}", color="purple")),  # Associates
                ft.DataCell(ft.Text(f"{row[5]:.2f}", color="orange")),  # Bachelors
                ft.DataCell(ft.Text(f"{row[6]:.2f}", color="cyan")),  # Masters
                ft.DataCell(ft.Text(f"{row[7]:.2f}", color="magenta"))  # PHD+
            ]
            rows.append(ft.DataRow(cells))

        # Adds table to page
        label = ft.Text(text, size=20)
        self.tasks.controls = [label, self._build_table(cols, rows)]

        def dropdown_changed(e):
            self.conditions = f"HAVING countryName = '{dd.value}'"
            self.country_edu(e)

        t = ft.Text("Pick Country to see")
        cursor.execute("""SELECT DISTINCT name FROM Country ORDER BY name ASC""")
        countrys = cursor.fetchall()
        options = [ft.dropdown.Option(i[0]) for i in countrys]
        #print(options)
        dd = ft.Dropdown(
            on_change=dropdown_changed,
            options= options,
            width=100,
            value = self.conditions if self.conditions else None
        )
        self.conditions = None

        # Adds button and text field to page
        self.tasks.controls.append(t)
        self.tasks.controls.append(dd)
        self.update()

    def country_wage(self, e):
        cursor = self.connection.cursor()
        # Define columns to retrieve 
        cols_text = ['Country', 'Average Salary in USD']
        # Format columns to flet datatype
        cols = [ft.DataColumn(ft.Text(i)) for i in cols_text]

        # Query based on column names defined
        text = "AVG Salary by Country in USD"
        query = f"""
        SELECT
            Country.name, ROUND(AVG(Developer.compensation),2) as  a  From Developer
            JOIN Country on Country.name = Developer.countryName
        GROUP BY Country.name
        HAVING COUNT(*) > 9
        ORDER BY a DESC
        """

        if self.conditions != None:
            query = f"""
                SELECT
                    Country.name, ROUND(AVG(Developer.compensation),2) as  a  From Developer
                    JOIN Country on Country.name = Developer.countryName
                GROUP BY Country.name
                HAVING COUNT(*) > 9
            {self.conditions}
            """

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
        label = ft.Text(text, size=20)
        self.tasks.controls = [label, self._build_table(cols, rows)]


        # Switch function that called when the switch is changed
        def switch(e):
            if e.data == 'true':
                e.data = True
                self.conditions = "ORDER BY a DESC"
            else:
                e.data = False
                self.conditions = "ORDER BY a ASC"
            self.country_wage(e)


        # Switch object for our subquery
        s = ft.Switch(
            label="Ordered: Descending",
            value=True if e.data == '' or e.data == True else False,
            thumb_color={ft.MaterialState.SELECTED: ft.colors.BLUE},
            track_color=ft.colors.YELLOW,
            focus_color=ft.colors.PURPLE,
            on_change = switch
        )

        # Add subquery to page
        self.tasks.controls.append(s)
        self.update()


    def tech_wage(self, e):
        cursor = self.connection.cursor()
        # Define columns to retrieve 
        cols_text = ['Tech Name', 'AVG Salary USD']
        # Format columns to flet datatype
        cols = [ft.DataColumn(ft.Text(i)) for i in cols_text]

        # Query based on column names defined
        text = "AVG Salary by technology"
        query = f"""
        Select t.technologyName, ROUND(AVG(d.compensation),2) as Salary From Technology as t
        JOIN Uses as u on t.technologyName = u.technologyName
        JOIN Developer as d on d.devID = u.devID
        GROUP BY t.technologyName
        HAVING count(*) > 5
        ORDER by Salary DESC;
        """

        if self.conditions != None:
            sub = self.conditions[len("where t.technologynsme = "):]
            text = f"Average salary for {sub}"
            query = f"""
            Select t.technologyName, ROUND(AVG(d.compensation),2) as Salary From Technology as t
            JOIN Uses as u on t.technologyName = u.technologyName
            JOIN Developer as d on d.devID = u.devID
            {self.conditions}
            GROUP BY t.technologyName
            """

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
        label = ft.Text(text, size=20)
        self.tasks.controls = [label, self._build_table(cols, rows)]

        # Sets subquery to text field value
        def select(e):
            self.conditions = f"WHERE t.technologyName = '{tb1.content.value}'"
            self.tech_wage(e)

        # Creates a text input field
        tb1 = ft.Container(
            content = ft.TextField(label="Technology"),
            width = 200,
        )

        # Button that submits text field
        b = ft.ElevatedButton(text="Submit", on_click=select)

        # Adds button and text field to page
        self.tasks.controls.append(tb1)
        self.tasks.controls.append(b)
        self.update()