import mysql.connector
import pandas as pd


filepath = "~/OneDrive/Documents/db/survey_results_public.csv"

def parse(connection: mysql.connector.connection_cext.CMySQLConnection, filepath):
    pd.read_csv(filepath)
    cursor = connection.cursor()
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