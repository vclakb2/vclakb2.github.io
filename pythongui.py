import tkinter as tk
from tkinter import ttk
import mysql.connector

def display_mysql_table(host, port, user, password, database, query):
    # Connect to MySQL database
    conn = mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database
    )

    # Create cursor
    cursor = conn.cursor()

    # Execute SQL query to fetch data
    cursor.execute(query)

    # Fetch all rows
    rows = cursor.fetchall()

    # Create new window for displaying table
    table_window = tk.Toplevel()
    table_window.title("MySQL Table Viewer")

    tree = ttk.Treeview(table_window)

    # Add columns
    columns = [i[0] for i in cursor.description]
    tree["columns"] = columns
    tree.heading("#0", text="Index")
    for col in columns:
        tree.heading(col, text=col)

    # Add rows
    for i, row in enumerate(rows, 1):
        tree.insert("", "end", text=i, values=row)

    tree.pack(expand=True, fill="both")

def main():
    def on_select(event=None):
        chosen_query = query_variable.get()
        if chosen_query:
            if chosen_query == "Developer":
                query = "SELECT * FROM Developer"
            elif chosen_query == "AIWorkflowChangein1Year":
                query = "SELECT * FROM AIWorkflowChangein1Year"
            elif chosen_query == "AIStance":
                query = "SELECT * FROM AIStance"
            display_mysql_table(
                host="mysql-3b07a8e5-db-developer.f.aivencloud.com",
                port="13447",
                user="avnadmin",
                password="AVNS_978XTtRvLUWrowzEW-D",
                database="DevAI",
                query=query
            )

    root = tk.Tk()
    root.title("Main Menu")

    query_options = ["Developer", "AIWorkflowChangein1Year", "AIStance"]
    query_variable = tk.StringVar(root)
    query_variable.set(query_options[0])  # Default selection
    query_menu = tk.OptionMenu(root, query_variable, *query_options, command=on_select)
    query_menu.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()