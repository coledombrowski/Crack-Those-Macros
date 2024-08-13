import re
import pyodbc
import pandas as pd
import numpy as np
import os

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

# Define the directory containing the CSV files
directory = r'C:\Users\2cona\OneDrive\Advanced Software Engineering\Local Dev\Food Urls'

# List to hold individual DataFrames
dfs = []

# Loop through the files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        file_path = os.path.join(directory, filename)
        df = pd.read_csv(file_path)
        dfs.append(df)

# Combine all DataFrames in the list into a single DataFrame
df = pd.concat(dfs, ignore_index=True)

# Replace spaces in DataFrame column names with underscores
df.columns = [col.strip().replace(' ', '_') for col in df.columns]

# Replace all np.nan with None and convert NumPy types to Python types for SQL compatibility
df = df.where(pd.notna(df), None)
df = df.applymap(lambda x: float(x) if isinstance(x, (int, float, np.float64, np.int64)) else x)
def duplicate_to_key(table: pd.DataFrame, column_name: str) -> pd.DataFrame:
    if column_name in table.columns:
        table['join_key'] = table[column_name]
    else:
        raise ValueError(f"The column '{column_name}' does not exist in the DataFrame.")
    return table
df = duplicate_to_key(df,'URLs')

# Database connection setup
server = 'crackthosemacros.database.windows.net'
database = 'crackthosemacros'
username = 'admin_p'
password = 'PurchaseCard!#600'  # Ensure password is securely handled in actual use
driver = '{SQL Server}'

conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
connection = pyodbc.connect(conn_str)
cursor = connection.cursor()

# Retrieve existing column names from the table
table_name = 'Stores'
query = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}'"
existing_columns = [row[0] for row in cursor.execute(query).fetchall()]

# Check for any new columns in the DataFrame not in the SQL table
new_columns = [col for col in df.columns if col not in existing_columns]

# SQL to add new columns to the table, defaulting to a generous VARCHAR type
for col in new_columns:
    alter_query = f"ALTER TABLE {table_name} ADD {col} VARCHAR(MAX)"
    print(alter_query)
    cursor.execute(alter_query)

# Commit changes to add columns
connection.commit()

# Prepare and execute the insert query
insert_query_template = f"INSERT INTO {table_name} ({', '.join(df.columns)}) VALUES "

# Iterate over each record in the dataframe
for record in df.to_records(index=False):
    values_list = []
    for value in record:
        # Check for NaN (specifically for pandas data)
        if pd.isna(value):
            values_list.append('NULL')
        elif isinstance(value, str):
            escaped_value = value.replace("'", "''")
            values_list.append(f"'{escaped_value}'")
        else:
            values_list.append(str(value))
    values_str = ', '.join(values_list)
    full_query = insert_query_template + f"({values_str})"
    try:
        cursor.execute(full_query)
        connection.commit()
    except Exception as e:
        print(full_query)  # Optional: for debugging
        print("An error occurred:", e)

cursor.close()
connection.close()