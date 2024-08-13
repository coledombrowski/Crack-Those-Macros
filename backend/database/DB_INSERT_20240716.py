import pyodbc
import pandas as pd
import numpy as np

server = 'crackthosemacros.database.windows.net'
database = 'crackthosemacros'
username = 'admin_p'
password = input('password:')
driver = '{SQL Server}'  # Adjust driver as needed

conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
connection = pyodbc.connect(conn_str)

# Read data from CSV
df = pd.read_csv('DB_INSERT_202407162.csv')

# Ensure correct data types and handle NaN values
df['Pounds'] = pd.to_numeric(df['Pounds'], errors='coerce')
df['Calories'] = pd.to_numeric(df['Calories'], errors='coerce')
df['Weight Range'] = df['Weight Range'].astype(str)  # Ensuring this is treated as a string

# Replace NaN with None for SQL NULL
df = df.where(pd.notnull(df), None)

# SQL insert statement template
sql_insert = """
INSERT INTO NutritionPlan (Goal, Amount, Pounds, MealTime, WeightRange, Suggestion, Calories)
VALUES (?, ?, ?, ?, ?, ?, ?)
"""

# Cursor for executing SQL commands
cursor = connection.cursor()

# Iterate through DataFrame rows
for row in df.itertuples(index=False):
    data_tuple = tuple(row)
    try:
        # Execute insert statement for each row
        cursor.execute(sql_insert, data_tuple)
        connection.commit()  # Commit each transaction
        print(f"Executed SQL: {sql_insert % data_tuple}")  # Print the SQL statement for debugging
    except Exception as e:
        print(f"An error occurred for row {data_tuple}: {e}")
        connection.rollback()  # Rollback in case of error

# Clean up
cursor.close()
connection.close()