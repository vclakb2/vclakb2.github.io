import mysql.connector
import csv


filepath = "survey_results_public.csv"

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

ONLINE = ['Formal documentation provided by the owner of the tech', 
            'Blogs with tips and tricks', 
            'Books', 
            'Recorded coding sessions', 
            'How-to videos', 
            'Video-based Online Courses', 
            'Written-based Online Courses', 
            'Auditory material (e.g., podcasts)', 
            'Online challenges (e.g., daily or weekly coding challenges)', 
            'Written Tutorials', 
            'Click to write Choice 20', 
            'Stack Overflow', 
            'Interactive tutorial', 
            'Programming Games']

OFFLINE = ['Books / Physical media',
            'Coding Bootcamp',
            'Colleague', 
            'Friend or family member', 
            'Hackathons (virtual or in-person)', 
            'Online Courses or Certification', 
            'On the job training', 
            'Other online resources (e.g., videos, blogs, forum)', 
            'School (i.e., University, College, etc)']

LANGUAGES = ["Ada",
            "Apex",
            "APL",
            "Assembly",
            "Bash/Shell (all shells)",
            "C",
            "C#",
            "C++",
            "Clojure",
            "Cobol",
            "Crystal",
            "Dart",
            "Delphi",
            "Elixir",
            "Erlang",
            "F#",
            "Flow",
            "Fortran",
            "GDScript",
            "Go",
            "Groovy",
            "Haskell",
            "HTML/CSS",
            "Java",
            "JavaScript",
            "Julia",
            "Kotlin",
            "Lisp",
            "Lua",
            "MATLAB",
            "Nim",
            "Objective-C",
            "OCaml",
            "Perl",
            "PHP",
            "PowerShell",
            "Prolog",
            "Python",
            "R",
            "Raku",
            "Ruby",
            "Rust",
            "SAS",
            "Scala",
            "Solidity",
            "SQL",
            "Swift",
            "TypeScript",
            "VBA",
            "Visual Basic (.Net)",
            "Zig"]

OS = ["AIX",
    "Android",
    "Arch",
    "BSD",
    "ChromeOS",
    "Cygwin",
    "Debian",
    "Fedora",
    "Haiku",
    "iOS",
    "iPadOS",
    "MacOS",
    "Other Linux-based",
    "Red Hat",
    "Solaris",
    "Ubuntu",
    "Windows",
    "Windows Subsystem for Linux (WSL)"]

LIBS = [".NET (5+)",
        ".NET Framework (1.0 - 4.8)",
        ".NET MAUI",
        "Apache Kafka",
        "Apache Spark",
        "Capacitor",
        "Cordova",
        "CUDA",
        "Electron",
        "Flutter",
        "GTK",
        "Hadoop",
        "Hugging Face Transformers",
        "Ionic",
        "JAX",
        "Keras",
        "Ktor",
        "MFC",
        "Micronaut",
        "Numpy",
        "Opencv",
        "OpenGL",
        "Pandas",
        "Qt",
        "Quarkus",
        "RabbitMQ",
        "React Native",
        "Scikit-Learn",
        "Spring Framework",
        "SwiftUI",
        "Tauri",
        "TensorFlow",
        "Tidyverse",
        "Torch/PyTorch",
        "Uno Platform",
        "Xamarin"]

def parse(connection: mysql.connector.connection_cext.CMySQLConnection, filepath):
    cursor = connection.cursor()
    # # EducationSource
    # for entry in ONLINE:
    #     query = "INSERT INTO EducationSource VALUES (%s, %s)"
    #     values = (entry, True)
    #     cursor.execute(query, values)
    #     connection.commit()
    # for entry in OFFLINE:
    #     query = "INSERT INTO EducationSource VALUES (%s, %s)"
    #     values = (entry, False)
    #     cursor.execute(query, values)
    #     connection.commit()

    # # Technology
    # query = "INSERT INTO Technology VALUES (%s, %s, %s)"

    # for entry in LANGUAGES:
    #     values = (entry, None, 'LANGUAGE')
    #     cursor.execute(query, values)
    #     connection.commit()
    # for entry in OS:
    #     values = (entry, None, 'OPERATING SYSTEM')
    #     cursor.execute(query, values)
    #     connection.commit()
    # for entry in LIBS:
    #     values = (entry, None, 'LIBRARIES')
    #     cursor.execute(query, values)
    #     connection.commit()
    
    with open(filepath, newline='', errors='ignore') as datafile:
        reader = csv.DictReader(datafile)
        count = 0
        for row in reader:
            if count == 2000:
                break
            count += 1
            id = row['ResponseId']

            # Developer          
            query = "INSERT INTO Developer VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (id, 
                      row['Country'] if row['MainBranch'] != 'NA' else None, 
                      row['Industry'] if row['Industry'] != 'NA' else None, 
                      row['YearsCode'] if row['YearsCode'] != 'NA' else None, 
                      row['OrgSize'] if row['OrgSize'] != 'NA' else None, 
                      row['WorkExp'] if row['WorkExp'] != 'NA' else None,
                      row['YearsCodePro'] if row['YearsCodePro'] != 'NA' else None,
                      bool(row['Employment']) if row['Employment'] != 'NA' else None,
                      row['Age'] if row['Age'] != 'NA' else None,
                      bool(row['MainBranch']) if row['MainBranch'] != 'NA' else None,
                      row['DevType'] if row['DevType'] != 'NA' else None,
                      row['PurchaseInfluence'] if row['PurchaseInfluence'] != 'NA' else None,
                      row['CodingActivities'][:150] if row['CodingActivities'] != 'NA' else None,
                      row['RemoteWork'] if row['RemoteWork'] != 'NA' else None,
                      row['EdLevel'] if row['EdLevel'] != 'NA' else None,
                      row['ConvertedCompYearly'] if row['ConvertedCompYearly'] != 'NA' else None)
            cursor.execute(query, values)
            
            # AIStance
            query = "INSERT INTO AIStance VALUES (%s, %s, %s)"
            values = (id, row['AISent'], row['AIBen'])
            cursor.execute(query, values)

            # AIDevWorkflowUse
            workflow_use = [row['AIToolInterested in Using'].split(';'), 
                            row['AIToolCurrently Using'].split(';'), 
                            row['AIToolNot interested in Using'].split(';')]
            keys = [INTERESTED, USING, NOT_USING]

            planning, testing, reviewing, deployment, collaborate, debugging, writing, learning, documenting = (None for _ in range(9))
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

            # AIWorkflowChangein1Year
            workflow_change = [row['AINextVery different'].split(';'), 
                               row['AINextSomewhat different'].split(';'), 
                               row['AINextNeither different nor similar'].split(';'),
                               row['AINextSomewhat similar'].split(';'),
                               row['AINextVery similar'].split(';')]
            keys = [VERY_DIFFERENT, SOMEWHAT_DIFFERENT, NEUTRAL, SOMEWHAT_SIMILAR, VERY_SIMILAR]

            planning, testing, reviewing, deployment, collaborate, debugging, writing, learning, documenting = (None for _ in range(9))
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

            # LearnsFrom
            sources = row['LearnCode'].split(';') + row['LearnCodeOnline'].split(';')
            for source in sources:
                if source in ONLINE or source in OFFLINE:
                    query = "INSERT INTO LearnsFrom VALUES (%s, %s)"
                    values = (id, source)
                    cursor.execute(query, values)

            # Uses
            sources = row['LanguageHaveWorkedWith'].split(';') + row['OpSysProfessional use'].split(';') + row['MiscTechHaveWorkedWith'].split(';')
            for source in sources:
                if source in LANGUAGES or source in OS or source in LIBS:
                    query = "INSERT INTO Uses VALUES (%s, %s)"
                    values = (id, source)
                    cursor.execute(query, values)
            print(count)
        
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

