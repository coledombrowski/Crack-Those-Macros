import os
import re
import pyodbc
import pandas as pd
import numpy as np

def import_pickled_dfs(folder_path):
    # List to hold all DataFrames
    df_list = []

    # Iterate over all files in the given folder path
    for filename in os.listdir(folder_path):
        # Check if the file is a pickle file
        if filename.endswith('.pkl'):
            # Construct full file path
            file_path = os.path.join(folder_path, filename)
            # Load the pickled pandas DataFrame
            df = pd.read_pickle(file_path)
            # Append the DataFrame to the list
            df_list.append(df)

    # Concatenate all DataFrames in the list into one DataFrame
    combined_df = pd.concat(df_list, ignore_index=True)

    return combined_df

folder_path = r'C:\Users\2cona\OneDrive\Advanced Software Engineering\Local Dev\Pickled Files'
df = import_pickled_dfs(folder_path)

df.rename(columns={'Brand': 'Store'}, inplace=True)
df.rename(columns={'NF': 'NF_RAW'}, inplace=True)


df = df[df['NF_RAW'] != 'No Nutrition Facts'].reset_index(drop=True)

# Convert all text in 'NF' to uppercase
df['NF_RAW'] = df['NF_RAW'].str.upper()

# Split the 'NF_RAW' column by '\n' into a list of strings
df['split'] = df['NF_RAW'].str.split('\n')



#Define a function to process each list and return a dictionary
def process_list(lst):
    temp_var = 0
    result = {}
    for item in lst:
        #  Regex to handle numbers and ranges, and to filter out invalid entries
        match = re.search(r'^(.*?)\s*([-\d\.]+)\s*(.*?)$', item)
        if item == "CALORIES":
            temp_var = 1

        if match:
            if temp_var == 1:
                key = "CALORIES"
            else:
                key = match.group(1).strip() + ' ' + match.group(3).strip()
            value = match.group(2).strip()
            temp_var = 0

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

#Concatenate the new columns to the original DataFrame
df = pd.concat([df, df_expanded], axis=1)



# Replace invalid characters in DataFrame column names with underscores
df.columns = [col.strip().replace(' ', '_') for col in df.columns]
df.columns = [col.strip().replace('.', '_') for col in df.columns]
df.columns = [col.strip().replace('(', '_') for col in df.columns]
df.columns = [col.strip().replace(')', '_') for col in df.columns]
df.columns = [col.strip().replace('/', '_') for col in df.columns]
df.columns = [col.strip().replace(',', '_') for col in df.columns]
df.columns = [col.strip().replace(':', '_') for col in df.columns]
df.columns = [col.strip().replace('"', '_') for col in df.columns]

# Replace all np.nan with None and convert NumPy types to Python types for SQL compatibility
df = df.where(pd.notna(df), None)
df = df.applymap(lambda x: float(x) if isinstance(x, (int, float, np.float64, np.int64)) else x)

df.drop(columns=['%','split','*_PERCENT_DAILY_VALUES_ARE_BASED_ON_A_CALORIE_DIET_'], inplace=True)
df = df.drop(df.filter(regex='^INGREDIENTS__').columns, axis=1)

# Handle duplicate columns
df = df.groupby(level=0, axis=1).sum()


def Pivot_Servings_Modified(df):
    # List of custom serving columns that include measurements in grams or specific types
    custom_serving_cols = [
        'BOWL___G', 'BREAD_BOWL___G', 'BROWNIE_HALF___G', 'BROWNIE___G', 'CAKE___G',
        'CAN___G', 'CHICKEN_STRIP___G', 'CM_CUBE__30G', 'CONTAINER___G', 'COOKIE___G',
        'COUNT___G', 'CRISPS___G', 'CUP___G', 'DISH___G', 'EACH___G', 'FLUID_OUNCE___G',
        'GALLON___G', 'GRAMS___G', 'INCLUDES_G','TRAY___G','TSP___G','TACO_SHELLS___G','TBSP___G',
        'SCOOPS___G','SCOOP___G','SLICES___G','SLICE___G','OZ___G','PACKAGE___G','PACKET___G','PIECES___G','PIECE___G','PIZZA_PORTION___G','PIZZA___G','PORTION___G',
        'LOADED_TOTS___G','NUGGET___G','ROLL___G','SANDWICH___G','STICK___G','WRAP___G','__CUBE___G'
    ]

    # Combine with the generic filter for any column names containing "serving"
    serving_cols = [col for col in df.columns if 'serving' in col.lower()] + custom_serving_cols

    # Melt the dataframe so each serving column becomes a row
    df_melted = df.melt(id_vars=[col for col in df.columns if col not in serving_cols],
                        value_vars=serving_cols,
                        var_name='Serving_Size_Type',
                        value_name='Serving_Size_Value')

    # Convert 'Serving_Value' to numeric, setting errors='coerce' to handle non-numeric values
    df_melted['Serving_Size_Value'] = pd.to_numeric(df_melted['Serving_Size_Value'], errors='coerce')

    # Replace non-positive values with 1 and corresponding 'Serving_Type' to 'MEAL'
    mask = df_melted['Serving_Size_Value'] <= 0
    df_melted.loc[mask, 'Serving_Size_Value'] = 1
    df_melted.loc[mask, 'Serving_Size_Type'] = 'MEAL'

    # Remove duplicate rows
    df_melted = df_melted.drop_duplicates()

    return df_melted


df = Pivot_Servings_Modified(df)
df.rename(columns={'TOTAL_CARBOHYDRATES_G': 'TOTAL_CARBOHYDRATE_G'}, inplace=True)

df['Price'] = 0.00
df['POLYUNSATURATED_FAT_G'] = 0.00
df['MONOUNSATURATED_FAT_G'] =0.00
df['Serving_Per_Type'] = 'MEAL'
df['Serving_Per_Value'] = 1.00

filepath= r'C:\Users\2cona\OneDrive\Advanced Software Engineering\Local Dev\Pickled Files\Restaurants_test2.csv'
df.to_csv(filepath, index=False)

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
table_name = 'R_MEALS'
query = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}'"
existing_columns = [row[0] for row in cursor.execute(query).fetchall()]
print(existing_columns)
print([col for col in df.columns])


# Check for any new columns in the DataFrame not in the SQL table
new_columns = [col for col in df.columns if col not in existing_columns]

# SQL to add new columns to the table, defaulting to a generous VARCHAR type
for col in new_columns:
    try:
        alter_query = f"ALTER TABLE {table_name} ADD {col} VARCHAR(MAX)"
        print(alter_query)
        cursor.execute(alter_query)
    except Exception as e:
        print('failed')

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