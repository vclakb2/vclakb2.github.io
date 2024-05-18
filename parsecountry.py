import pandas as pd
import mysql.connector
from mysql.connector import Error

# Path to your CSV file
csv_file_path = '/Users/akhilvaid/Downloads/stack-overflow-developer-survey-2023/survey_results_public.csv'

# Database connection details
db_config = {
    'host': 'mysql-3b07a8e5-db-developer.f.aivencloud.com',     # e.g., 'localhost' or 'your.server.com'
    'user': 'avnadmin',     # e.g., 'root'
    'port': 13447,
    'password': 'AVNS_978XTtRvLUWrowzEW-D', # e.g., 'password'
    'database': 'DevAI'  # e.g., 'DevAI'
}

def create_connection(db_config):
    """ Create a database connection to the MySQL database specified by db_config """
    connection = None
    try:
        connection = mysql.connector.connect(
            host=db_config['host'],
            user=db_config['user'],
            port=db_config['port'],
            password=db_config['password'],
            database=db_config['database']
        )
        if connection.is_connected():
            print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

def insert_country_data(connection, country, currency):
    """ Insert country data into the Country table """
    cursor = connection.cursor()
    # Escape double quotes
    country = country.replace('"', '\\"')

    # Escape single quotes
    country = country.replace("'", "\\'")
    query ='INSERT INTO Country VALUES (\'' + str(country) + '\', NULL, \'' + str(currency) + '\', NULL);'
    
    # print(query)
    cursor.execute(query)
    connection.commit()

def parse_csv_and_insert_data(csv_file_path, connection):
    """ Parse CSV file and insert data into the database """
    # Read the CSV file
    data = pd.read_csv(csv_file_path)
    data = data.fillna('NA')
    print(data.head())
    # Iterate through the rows and insert data into the Country table
    dict_country = {}
    for index, row in data.iterrows():
        # print(row[0:26])
        country = row['Country']
        
        # print(country)
        currency = row['Currency']
        # print(currency)
        if country == None:
            country = 'NA'
        if currency == None:
            currency = 'NA'
        if country not in dict_country:
            dict_country[country] = [currency]
    
    for country, currency_list in dict_country.items():
        for currency in currency_list:
            insert_country_data(connection, country, currency)

def main():
    # Create a database connection
    connection = create_connection(db_config)
    
    # Parse the CSV and insert data into the database
    
    parse_csv_and_insert_data(csv_file_path, connection)
    connection.close()
    print("Done")

if __name__ == '__main__':
    main()