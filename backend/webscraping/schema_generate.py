import pyodbc
import pandas as pd

server = 'crackthosemacros.database.windows.net'
database = 'crackthosemacros'
username = 'admin_p'
password = input()
driver = '{SQL Server}'  # Adjust driver as needed

conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
connection = pyodbc.connect(conn_str)

# Function to fetch tables and columns
def fetch_schema(connection):
    query = """
    SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE 
    FROM INFORMATION_SCHEMA.COLUMNS 
    WHERE TABLE_CATALOG = ? 
    ORDER BY TABLE_NAME, ORDINAL_POSITION
    """
    return pd.read_sql(query, connection, params=[database])

# Function to write schema to a text file
def write_schema_to_file(schema, filename="database_schema.txt"):
    with open(filename, 'w') as f:
        current_table = ''
        for index, row in schema.iterrows():
            if current_table != row['TABLE_NAME']:
                current_table = row['TABLE_NAME']
                f.write(f"\nTable: {current_table}\n")
                f.write("Columns:\n")
            f.write(f"  {row['COLUMN_NAME']} ({row['DATA_TYPE']})\n")

# Fetch the schema and write to file
schema = fetch_schema(connection)
write_schema_to_file(schema)
