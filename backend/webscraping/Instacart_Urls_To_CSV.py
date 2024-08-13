from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import pickle
import time
import random
import re
from selenium.webdriver.common.keys import Keys
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
combined_df = pd.concat(dfs, ignore_index=True)

URL_list = combined_df['URLs'].tolist()
URL_list = list(set(URL_list))

options = Options()
options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'

service = Service(executable_path=r'C:\Users\2cona\OneDrive\Advanced Software Engineering\Local Dev\geckodriver.exe')


user_agents = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
]



def getNutritionFacts(URL):
    sleep_time_int = random.uniform(2, 6)
    sleep_time_dec = random.uniform(1, 100)
    sleep_time = sleep_time_int + (sleep_time_dec/100)
    time.sleep(sleep_time)

    attempts = 0
    max_attempts = 3  # Set a maximum number of retries
    while attempts < max_attempts:
        user_agent = random.choice(user_agents)
        # Set the chosen user agent
        options.set_preference("general.useragent.override", user_agent)
        driver = webdriver.Firefox(service=service, options=options)
        driver.get(URL)
        driver.implicitly_wait(10)

        try:
            name_xpath = '/html/body/div[1]/div/main/div[2]/div/div[2]/div[1]/div[1]/h1'
            name_loc = driver.find_element(By.XPATH, name_xpath)
            name_txt = name_loc.text
        except NoSuchElementException as e:
            name_txt = 'Name not found'

        try:
            price_xpath = '//*[@id="regular_price"]'
            price_loc = driver.find_element(By.XPATH, price_xpath)
            price_txt = price_loc.text
        except NoSuchElementException as e:
            try:
                price_xpath = '//*[@id="sale_price"]'
                price_loc = driver.find_element(By.XPATH, price_xpath)
                price_txt = price_loc.text
            except NoSuchElementException as e:
                price_txt = 'Price not found'

        try:
            xpath = '/html/body/div[1]/div/main/div[4]/div/div[2]/div'
            nutrition_facts_table = driver.find_element(By.XPATH, xpath)
            NF = nutrition_facts_table.text
        except NoSuchElementException as e:
            NF = 'No Nutrition Facts'

        driver.close()

        if 'Nutrition Facts' in NF:
            row_tuple = (name_txt, price_txt, NF)
            print(row_tuple)
            return row_tuple
        else:
            attempts += 1
            print("Retrying, attempt", attempts)

    NF = 'Max Attempts Reached'
    row_tuple = (name_txt, price_txt, NF)
    print(row_tuple)
    try:
        return row_tuple
    except:
        return ('', '', 'Max Attempts Reached')


# Define file paths
csv_file = 'RawNutritionFacts.csv'
pkl_file = 'RawNutritionFacts.pkl'


# Function to save data
def save_data(df, csv_file, pkl_file, mode='a'):
    header = not os.path.exists(csv_file) if mode == 'a' else False
    df.to_csv(csv_file, mode=mode, header=header, index=False)
    df.to_pickle(pkl_file)

def main():
    # Check if the CSV and pickle files already exist and load them; otherwise, create a new DataFrame
    if os.path.exists(csv_file) and os.path.exists(pkl_file):
        df = pd.read_pickle(pkl_file)  # Load the DataFrame from pickle for consistency
    else:
        df = pd.DataFrame(columns=['URL', 'Name','Price','NF_Raw'])  # Create a new DataFrame if files do not exist

    # Initialize batch processing
    batch_size = 20
    batch_data = []

    # Process each URL
    for url in URL_list:
        product_info = getNutritionFacts(url)
        if product_info[2] != 'No Nutrition Facts' and product_info[2] != 'Max Attempts Reached':
            new_row = {'URL': url, 'Name': product_info[0],'Price': product_info[1],'NF_Raw': product_info[2]}
            batch_data.append(new_row)

        # Check if the batch is full
        if len(batch_data) >= batch_size:
            # Convert batch data to DataFrame and append to the main DataFrame
            batch_df = pd.DataFrame(batch_data)
            df = df.append(batch_df, ignore_index=True)
            # Save to files
            save_data(batch_df, csv_file, pkl_file)
            # Clear batch data
            batch_data = []

    # Process any remaining data in batch_data after the loop
    if batch_data:
        batch_df = pd.DataFrame(batch_data)
        df = df.append(batch_df, ignore_index=True)
        save_data(batch_df, csv_file, pkl_file)

    # Save the final DataFrame to ensure all data is recorded
    save_data(df, csv_file, pkl_file, mode='w')

main()