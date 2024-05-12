import PySimpleGUI as sg
import mysql.connector
import csv
import re

cursorObject = myConnection.cursor()

def executeAndPrint(query):
    cursorObject.execute(query)
    allResults = cursorObject.fetchall()

    layout = [[sg.Table(allResults, justification='left', key='-TABLE-')],]
    window = sg.Window("Title", layout, finalize=True)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        print(event, values)

    window.close()

def constructVariableQuery():
    variableLayout = [  
                        [sg.Text("What DevID?")],
                        [sg.InputText()],
                        [sg.Button('OK'), sg.Button('Cancel')] 
                     ]

    window = sg.Window('ExampleVariable', variableLayout)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == 'Cancel':
            break

        if event == 'OK':
            executeAndPrint(f'SELECT * FROM Developer WHERE DevID={values[0]}')

    window.close()

query_1 = \
        """
        SELECT * FROM Developer
        """

query_2 = \
        """
        SELECT * FROM Country
        """

layout = [  
            [sg.Button('Query1'), sg.Button('Query2'), sg.Button('Query3')] 
         ]

window = sg.Window('Example', layout)

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    if event == 'Query1':
        executeAndPrint(query_1)
    elif event == 'Query2':
        executeAndPrint(query_2)
    elif event == 'Query3':
        constructVariableQuery()

window.close()
