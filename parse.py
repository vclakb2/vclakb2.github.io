import mysql.connector
import csv


filepath = "~/survey_results_public.csv"

PLANNING = 'Project planning'
TESTING = 'Testing code'
REVIEWING = 'Committing and reviewing code'
DEPLOYMENT = 'Deployment and monitoring'
COLLABORATE = 'Collaborating with teammates'
DEBUGGING = 'Debugging and getting help'
WRITING = 'Writing code'
LEARNING = 'Learning about a codebase'
DOCUMENTING = 'Documenting code'

INTERESTED = 'INTERESTED'
USING = 'USING'
NOT_USING = 'NOT USING'

VERY_DIFFERENT = 'VERY DIFFERENT'
NEUTRAL = 'NEUTRAL'
SOMEWHAT_SIMILAR = 'SOMEWHAT SIMILAR'
VERY_SIMILAR = 'VERY SIMILAR'
SOMEWHAT_DIFFERENT = 'SOMEWHAT DIFFERENT'

def parse(connection: mysql.connector.connection_cext.CMySQLConnection, filepath):
    cursor = connection.cursor()
    
    with open(filepath, newline='') as datafile:
        reader = csv.reader(datafile)
        for row in reader:
            id = row['ResponseId']

            # AIDevWorkflowUse
            workflow_use = [row['AIToolInterested in Using'].split(';'), 
                            row['AIToolCurrently Using'].split(';'), 
                            row['AIToolNot interested in Using'].split(';')]
            keys = [INTERESTED, USING, NOT_USING]

            planning, testing, reviewing, deployment, collaborate, debugging, writing, learning, documenting = ('NULL' for _ in range(9))
            for ind, category in enumerate(workflow_use):
                if PLANNING in category:
                    planning = keys[ind]
                if TESTING in category:
                    testing = keys[ind]
                if REVIEWING in category:
                    reviewing = keys[ind]
                if DEPLOYMENT in category:
                    deployment = keys[ind]
                if COLLABORATE in category:
                    collaborate = keys[ind]
                if DEBUGGING in category:
                    debugging = keys[ind]
                if WRITING in category:
                    writing = keys[ind]
                if LEARNING in category:
                    learning = keys[ind]
                if DOCUMENTING in category:
                    documenting = keys[ind]

            query = "INSERT INTO AIDevWorkflowUse VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (id, planning, learning, documenting, writing, debugging, testing, reviewing, deployment, collaborate)
            cursor.execute(query, values)
            connection.commit()


            # AIWorkflowChangein1Year
            workflow_change = [row['AINextVery different'].split(';'), 
                               row['AINextSomewhat different'].split(';'), 
                               row['AINextNeither different nor similar'].split(';'),
                               row['AINextSomewhat similar'].split(';'),
                               row['AINextVery similar'].split(';')]
            keys = [VERY_DIFFERENT, SOMEWHAT_DIFFERENT, NEUTRAL, SOMEWHAT_SIMILAR, VERY_SIMILAR]

            planning, testing, reviewing, deployment, collaborate, debugging, writing, learning, documenting = ('NULL' for _ in range(9))
            for ind, category in enumerate(workflow_change):
                if PLANNING in category:
                    planning = keys[ind]
                if TESTING in category:
                    testing = keys[ind]
                if REVIEWING in category:
                    reviewing = keys[ind]
                if DEPLOYMENT in category:
                    deployment = keys[ind]
                if COLLABORATE in category:
                    collaborate = keys[ind]
                if DEBUGGING in category:
                    debugging = keys[ind]
                if WRITING in category:
                    writing = keys[ind]
                if LEARNING in category:
                    learning = keys[ind]
                if DOCUMENTING in category:
                    documenting = keys[ind]

            query = "INSERT INTO AIWorkflowChangein1Year VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (id, debugging, testing, deployment, reviewing, documenting, learning, planning, writing, collaborate)
            cursor.execute(query, values)
            connection.commit()

            

    cursor.close()



def main():
    myConnection = mysql.connector.connect(user = 'avnadmin',
        password = 'AVNS_978XTtRvLUWrowzEW-D',
        host = 'mysql-3b07a8e5-db-developer.f.aivencloud.com',
        port = 13447,
        database = 'DevAI'
    )
    parse(myConnection, filepath)
    myConnection.close()

if __name__ == "__main__":
    main()

"""
Reference:
Developer
    isDeveloper - C
    Age - D
    isEmployed - E
    Arrangement Status - F
    codingActivity - G
    Education Level - H
    Compensation - I
    yearsCoding - L
    yearsProCoding - M
    devExperience - BN
    devType - N
    orgSize - O
    purchaseInfluence - P
    Country - S
    Industry - CC
    Compensation - CF
EducationSource
    Source - I
    Online - J
Country
    CountryName - S
    Currency - T
AI Stance(red for strong entity)
    Using AI - AZ
    Stance - BA
    Trust on Accuracy of AI tools - BC
AI Development Workflow use(Relation b/w this and AI, weak entity(green))
Using BD, BE, BF. Cols -> response values, Entries -> excel col names (enum 1, 2, 3)
    Learn about codebase
    Project Planning	
    Writing code	
    Documenting code 
    Debugging and getting help 
    Testing code
    Commiting and reviewing code 
    Deployment and monitoring 
    Collaborating with teammates 
AI Workflow change in 1 year(Relation b/w this and AI, weak entity(green))
Using BG, BH, BI, BJ, BK. Cols -> response values, Entries -> excel col names (enum 1, 2, 3, 4, 5)
    Learn about codebase - AQ
    Project Planning - AQ
    Writing code - AQ
    Documenting code
    Debugging and getting help
    Testing code 
    Committing and reviewing code 
    Deployment and monitoring 
    Collaborating with teammates 
Industry
    Industry name - CC
Technology
    Technology Name
    Technology type (system, framework, language, database)
"""

