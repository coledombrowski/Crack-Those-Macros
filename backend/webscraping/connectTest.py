import pyodbc
import pandas as pd

server = 'crackthosemacros.database.windows.net'
database = 'crackthosemacros'
username = 'viewonly'
password = 'CrackThoseMacros!2024'
driver = '{SQL Server}'  # Adjust driver as needed

conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
connection = pyodbc.connect(conn_str)

query = "SELECT * FROM [dbo].[v_All_Food]"
df = pd.read_sql_query(query, connection)

print(df)
