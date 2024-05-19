import flet as ft
import os

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
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        base_dir = os.path.dirname(os.path.abspath(__file__))        
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
                            "Dev Years of Experience by Technology", 
                            icon=ft.icons.PERSON_3, 
                            style =  ft.ButtonStyle(
                                bgcolor = ft.colors.BLUE_700,
                                color='White'
                            ), 
                            on_click=self.get_yoe
                        ),
                        ft.FilledButton(
                            "Popular Developer Technologies", 
                            icon=ft.icons.PERSON_3, 
                            style =  ft.ButtonStyle(
                                bgcolor = ft.colors.YELLOW_900,
                                color='White'
                            ), 
                            on_click=self.get_tech
                        ),
                        ft.FilledButton(
                            "Popular Developer Industries", 
                            icon=ft.icons.PERSON_3, 
                            style =  ft.ButtonStyle(
                                bgcolor = "Red",
                                color='White'
                            ),
                            on_click=self.get_ind
                        ),
                    ],
                ),
                ft.Divider(height=9, thickness=3),
                ft.Text("Output:"),
                self.tasks,
            ],
        )
    

    # Heler method to build a table from a query output
    def _build_table(self, cols, rows, height = 300):
        lv = ft.ListView(expand=0, spacing=10, padding=20, auto_scroll=False,  height=height)
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
    def get_yoe(self, e):
        cursor = self.connection.cursor()
        # Define columns to retrieve 
        cols_text = ["Tech", "Years in Industry"]        

        # Query based on column names defined
        query = f"""
        SELECT t.technologyName , ROUND(AVG(d.devExperience), 2) AS Experience FROM Technology as t
        JOIN Uses as u on t.technologyName = u.technologyName
        JOIN Developer as d on d.devID = u.devID
        GROUP BY t.technologyName
        ORDER BY Experience DESC
        """
        
        # If a condition exists then add it to the query
        if self.conditions != None:
            query = f"""
            SELECT t.technologyName , ROUND(AVG(d.devExperience), 2) AS Experience FROM Technology as t
            JOIN Uses as u on t.technologyName = u.technologyName
            JOIN Developer as d on d.devID = u.devID
            {self.conditions}
            GROUP BY t.technologyName
            ORDER BY Experience DESC
            """

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
        self.tasks.controls = [self._build_table(cols, rows, 400)]

        # Create subquery button
        def select(e):
            self.conditions = f"WHERE t.technologyName = '{tb1.content.value}'"
            self.get_yoe(e)

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

    def get_tech(self, e):
        cursor = self.connection.cursor()
        # Define columns to retrieve 
        cols_text = ['Tech', 'Number of Users']
        # Format columns to flet datatype
        cols = [ft.DataColumn(ft.Text(i)) for i in cols_text]

        # Query based on column names defined
        query = f"""
        SELECT t.technologyName , COUNT(*) AS cnt FROM Technology as t
        JOIN Uses as u on t.technologyName = u.technologyName
        JOIN Developer as d on d.devID = u.devID
        GROUP BY t.technologyName
        ORDER BY cnt DESC
        """

        if self.conditions != None:
            query = f"""
            SELECT t.technologyName , COUNT(*) AS cnt FROM Technology as t
            JOIN Uses as u on t.technologyName = u.technologyName
            JOIN Developer as d on d.devID = u.devID
            GROUP BY t.technologyName
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
        self.tasks.controls = [self._build_table(cols, rows, 400)]


        # Switch function that called when the switch is changed
        def switch(e):
            if e.data == 'true':
                e.data = True
                self.conditions = "ORDER BY cnt DESC"
            else:
                e.data = False
                self.conditions = "ORDER BY cnt ASC"
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


    def get_ind(self, e):
        cursor = self.connection.cursor()
        # Define columns to retrieve 
        cols_text = ['Industry', "Count"]
        # Format columns to flet datatype
        cols = [ft.DataColumn(ft.Text(i)) for i in cols_text]

        # Query based on column names defined
        query = f"""
        SELECT i.industry, COUNT(*) FROM Industry as i
        JOIN Developer as d on d.industry = i.industry
        GROUP BY i.industry
        ORDER BY COUNT(*) DESC
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
        self.tasks.controls = [self._build_table(cols, rows, 500)]
        self.update()
