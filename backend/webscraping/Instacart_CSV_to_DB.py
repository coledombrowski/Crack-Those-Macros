import re
import pyodbc
import pandas as pd
import numpy as np

# Define the path to the CSV file
file_path = r'C:\Users\2cona\OneDrive\Advanced Software Engineering\Local Dev\RawNutritionFacts.csv'

# Load the CSV file into a DataFrame
df = pd.read_csv(file_path)

# Convert all text in 'NF_Raw' to uppercase
df['NF_Raw'] = df['NF_Raw'].str.upper()

# Split the 'NF_Raw' column by '\n' into a list of strings
df['split'] = df['NF_Raw'].str.split('\n')

#Define a function to process each list and return a dictionary
def process_list(lst):
    result = {}
    for item in lst:
        #  Regex to handle numbers and ranges, and to filter out invalid entries
        match = re.search(r'^(.*?)\s*([-\d\.]+)\s*(.*?)$', item)
        if match:
            key = match.group(1).strip() + ' ' + match.group(3).strip()
            value = match.group(2).strip()
            # Check and process the value if it's a range or a valid number
            if '-' in value:
                try:
                    numbers = [float(num) for num in value.split('-') if re.match(r'^\d+\.?\d*$', num)]
                    if numbers:
                        average_value = sum(numbers) / len(numbers)
                        result[key] = average_value
                except ValueError:
                    continue  # Skip if conversion fails
            else:
                try:
                    if re.match(r'^\d+\.?\d*$', value):  # Check if value is a valid float
                        result[key] = float(value)
                except ValueError:
                    continue  # Skip if conversion fails
    return result

# Apply transformations
df_expanded = pd.json_normalize(df['split'].apply(process_list))
df['Price'] = df['Price'].str.replace('$', '').astype(float)

#Concatenate the new columns to the original DataFrame
df = pd.concat([df, df_expanded], axis=1)

# Drop columns not needed
df.drop(columns=['split',' %','PERCENT DAILY VALUES ARE BASED ON A ,000 CALORIE DIET.'], inplace=True)

# Replace invalid characters in DataFrame column names with underscores
df.columns = [col.strip().replace(' ', '_') for col in df.columns]
df.columns = [col.strip().replace('.', '_') for col in df.columns]
df.columns = [col.strip().replace('(', '_') for col in df.columns]
df.columns = [col.strip().replace(')', '_') for col in df.columns]
df.columns = [col.strip().replace('/', '_') for col in df.columns]
df.columns = [col.strip().replace(',', '_') for col in df.columns]
df.columns = [col.strip().replace(':', '_') for col in df.columns]

# Replace all np.nan with None and convert NumPy types to Python types for SQL compatibility
df = df.where(pd.notna(df), None)
df = df.applymap(lambda x: float(x) if isinstance(x, (int, float, np.float64, np.int64)) else x)


def Pivot_Servings(df):
    # Filter columns that include any form of "serving" or "servings"
    serving_cols = [col for col in df.columns if 'serving' in col.lower() and 'size' not in col.lower()]

    # Melt the dataframe so each serving column becomes a row
    df_melted = df.melt(id_vars=[col for col in df.columns if col not in serving_cols],
                        value_vars=serving_cols,
                        var_name='Serving_Per_Type',
                        value_name='Serving_Per_Value')

    df_melted['Serving_Per_Value'] = pd.to_numeric(df_melted['Serving_Per_Value'], errors='coerce')

    # Remove rows where 'Serving_Value' is NaN or less than or equal to zero
    df_melted = df_melted[df_melted['Serving_Per_Value'] > 0]

    return df_melted

def Pivot_Serving_Size(df):
    # Filter columns that include any form of "serving" or "servings"
    serving_cols = [col for col in df.columns if 'serving' in col.lower() and 'per' not in col.lower()]

    # Melt the dataframe so each serving column becomes a row
    df_melted = df.melt(id_vars=[col for col in df.columns if col not in serving_cols],
                        value_vars=serving_cols,
                        var_name='Serving_Size_Type',
                        value_name='Serving_Size_Value')

    # Convert 'Serving_Value' to numeric, setting errors='coerce' to handle non-numeric values
    df_melted['Serving_Size_Value'] = pd.to_numeric(df_melted['Serving_Size_Value'], errors='coerce')

    # Remove rows where 'Serving_Value' is NaN or less than or equal to zero
    df_melted = df_melted[df_melted['Serving_Size_Value'] > 0]

    return df_melted

df = Pivot_Servings(df)
df = Pivot_Serving_Size(df)

df['Item_ID'] = 'NONE'
df['IRON_MG'] = 0.00
df['CALCIUM_MG'] =0.00
df['CALORIES_FROM_FAT'] = 0.00
df['POTASSIUM_MG'] = 0.00
df['VITAMIN_D_MCG'] = 0.00


csv_file_path = r"C:\Users\2cona\OneDrive\Advanced Software Engineering\Local Dev\TestDev\NutritionFacts_Test2.csv"
df.to_csv(csv_file_path, index=False)

# Database connection setup
server = 'crackthosemacros.database.windows.net'
database = 'crackthosemacros'
username = 'admin_p'
password = input()  # Ensure password is securely handled in actual use
driver = '{SQL Server}'

conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
connection = pyodbc.connect(conn_str)
cursor = connection.cursor()

# Retrieve existing column names from the table
table_name = 'G_Products'
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