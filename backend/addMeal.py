import pyodbc
import pandas as pd
import numpy as np
from datetime import datetime



def accept_meal_entry(pandas_row):
    server = 'crackthosemacros.database.windows.net'
    database = 'crackthosemacros'
    username = 'Admin_Shared'
    password = 'ZeroCalories!0'
    driver = '{SQL Server}'  # Adjust driver as needed

    # Connection string
    conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    connection = pyodbc.connect(conn_str)
    cursor = connection.cursor()

    response = input('Accept Meal Entry (yes/no)? ')
    if response.lower() == 'yes':
        # Prompt for username
        user_name = input('Enter username (no spaces): ')
        food_id = pandas_row['food_id']
        current_datetime = datetime.now()

        # SQL command to insert data
        insert_query = '''
        INSERT INTO UserLog (Username, food_id, insert_datetime) 
        VALUES (?, ?, ?)
        '''
        # Execute the insert command
        cursor.execute(insert_query, (user_name, food_id, current_datetime))
        cursor.commit()  # Commit the transaction
        print('Meal entry accepted and logged.')

    cursor.close()
    connection.close()

def upsert_questionnaire_results(username, meal, goal_number, units, connection_string):
    try:
        # Establish a connection to the database
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        # Define the SQL MERGE statement
        sql = """
        MERGE Questionnaire_Results AS target
        USING (SELECT ? AS Username, ? AS Meal, ? AS Goal_Number, ? AS units) AS source
        ON target.Username = source.Username and target.Meal = source.Meal
        WHEN MATCHED THEN 
            UPDATE SET 
                Meal = source.Meal,
                Goal_Number = source.Goal_Number,
                units = source.units
        WHEN NOT MATCHED BY TARGET THEN
            INSERT (Username, Meal, Goal_Number, units)
            VALUES (source.Username, source.Meal, source.Goal_Number, source.units);
        """

        # Execute the SQL statement
        cursor.execute(sql, username, meal, goal_number, units)
        conn.commit()

        print("Upsert operation completed successfully.")

    except pyodbc.Error as e:
        print(f"Error occurred: {e}")

    finally:
        # Close the database connection
        cursor.close()
        conn.close()
