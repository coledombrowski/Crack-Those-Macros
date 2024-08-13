from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time
import re
import random
import pandas as pd
import numpy as np
import pickle
from concurrent.futures import ThreadPoolExecutor
import string
import os
from threading import Lock
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

lock = Lock()
file_lock = Lock()

# Define the file path
file_path = r'C:\Users\2cona\OneDrive\Advanced Software Engineering\Local Dev\item_ids.csv'

# Import the CSV file into a pandas DataFrame
df = pd.read_csv(file_path)

# Add a new column 'URL' that concatenates the specified format
df['URL'] = df.apply(lambda row: f"https://www.nutritionix.com/i/{row['Brand']}/item/{row['Item_ID']}", axis=1)

# Split DataFrame into parts
dfs = np.array_split(df, 7)

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.48",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 13_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.2 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/92.0.902.67",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.2 Safari/605.1.15",
    "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 12_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0",
    "Mozilla/5.0 (Android 10; Mobile; rv:88.0) Gecko/88.0 Firefox/88.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/93.0.961.38",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (iPad; CPU OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.7 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.7",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0"
]

# Declare the global variable
picked_agents = []

def add_agent(agent):
    global picked_agents
    with lock:
        picked_agents.append(agent)

def remove_agent(agent):
    global picked_agents
    with lock:
        if agent in picked_agents:
            picked_agents.remove(agent)

file_names = []


def pickle_df(df,prefix = ''):
    with file_lock:
        filename = ''
        if len(file_names) >= 14:
            filename = random.choice(file_names)
        while filename == '':
            random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            if random_string not in file_names:
                file_names.append(random_string)
                filename = random_string
                break
        filename = prefix + filename + '.pkl'
        # Resource-safe file handling
        try:
            if os.path.exists(filename):
                with open(filename, 'rb') as f:
                    existing_df = pd.read_pickle(f)
                updated_df = pd.concat([existing_df, df])
                updated_df.to_pickle(filename)
                print(f"successful save over {filename}")
            else:
                filename = filename
                df.to_pickle(filename)
                print(f"successful save {filename}")
        except Exception as e:
            print(f"Error while handling the pickle file: {e}")

def webscrape(data_frame):
    driver = None

    try:

        scraped_data = []
        i = 0

        for row in data_frame.itertuples():
            url = row.URL
            try:
                user_agent = ''
                while user_agent == '':
                    random_agent = random.choice(user_agents)
                    if random_agent not in picked_agents:
                        add_agent(random_agent)
                        user_agent = random_agent
                        break

                # Navigate to the URL
                try:
                    options = Options()
                    options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
                    service = Service(
                        executable_path=r'C:\Users\2cona\OneDrive\Advanced Software Engineering\Local Dev\geckodriver.exe')
                    options.add_argument("--headless")
                    options.set_preference("general.useragent.override", user_agent)
                    driver = webdriver.Firefox(service=service, options=options)
                    driver.get(url)
                except:
                    pickle_df(pd.DataFrame(scraped_data))
                    i = 0
                    scraped_data = []
                    options = Options()
                    options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
                    service = Service(
                        executable_path=r'C:\Users\2cona\OneDrive\Advanced Software Engineering\Local Dev\geckodriver.exe')
                    options.add_argument("--headless")
                    options.set_preference("general.useragent.override", user_agent)
                    driver = webdriver.Firefox(service=service, options=options)
                    driver.get(url)

                time.sleep(random.uniform(2, 6))  # Simplified sleep call


                try:
                    name_xpath = '/html/body/div[2]/div/div[2]/div[1]/div[1]/div[2]/h1'
                    name_loc = driver.find_element(By.XPATH, name_xpath)
                    name_txt = name_loc.text
                except NoSuchElementException as e:
                    name_txt = 'Name not found'

                try:
                    xpath = '//*[@id="nutrition-label"]'
                    nutrition_facts_table = driver.find_element(By.XPATH, xpath)
                    NF = nutrition_facts_table.text
                except NoSuchElementException as e:
                    NF = 'No Nutrition Facts'

                scraped_data.append({
                    'Brand': row.Brand,
                    'Item_ID': row.Item_ID,
                    'URL': url,
                    'Name': str(name_txt),
                    'NF': str(NF)
                })

                i += 1
                if i > 20:
                    pickle_df(pd.DataFrame(scraped_data))
                    i = 0
                    scraped_data = []

                print(f"finish scraping {url}")
            except Exception as e:
                print(f"Failure {e}")
                pickle_df(pd.DataFrame(scraped_data),'error')
                i = 0
                scraped_data = []
            finally:
                remove_agent(user_agent)  # Clean up the used user agent
                if driver:
                    driver.close()

    except Exception as e:
        print(f"Critical Failure {e}")
    finally:
        if scraped_data:  # Save any remaining data
            pickle_df(pd.DataFrame(scraped_data))


# Use ThreadPoolExecutor to run the pickling in parallel
with ThreadPoolExecutor(max_workers=14) as executor:
    # dfs is a list of DataFrame parts
    for df_split in dfs:
        executor.submit(webscrape, df_split)

