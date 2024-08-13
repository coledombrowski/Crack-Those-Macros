from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time
import re
import random
import pandas as pd

options = Options()
options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
service = Service(executable_path=r'C:\Users\2cona\OneDrive\Advanced Software Engineering\Local Dev\geckodriver.exe')
options.add_argument("--headless")

# Initialize the WebDriver
driver = webdriver.Firefox(service=service, options=options)

# Base URL
urls = ['https://www.nutritionix.com/brand/mcdonalds/products/513fbc1283aa2dc80c000053',
             'https://www.nutritionix.com/brand/burger-king/products/513fbc1283aa2dc80c00000a',
             'https://www.nutritionix.com/brand/cracker-barrel/products/58ef9673ec6894767f874f4a',
        'https://www.nutritionix.com/brand/wendys/products/513fbc1283aa2dc80c00000f',
        'https://www.nutritionix.com/brand/cook-out/products/57ab8ba0a028b5e1529f4d3e',
        'https://www.nutritionix.com/brand/subway/products/513fbc1283aa2dc80c000005',
        'https://www.nutritionix.com/brand/dominos/products/513fbc1283aa2dc80c000003',
        'https://www.nutritionix.com/brand/taco-bell/products/513fbc1283aa2dc80c000020',
        'https://www.nutritionix.com/brand/buffalo-wild-wings/products/521b95464a56d006cae29dac',
        'https://www.nutritionix.com/brand/waffle-house/products/55ded06e27fbbf82551a8491',
        'https://www.nutritionix.com/brand/applebees/products/513fbc1283aa2dc80c000015',
        'https://www.nutritionix.com/brand/olive-garden/products/513fbc1283aa2dc80c000024',
        'https://www.nutritionix.com/brand/chilis/products/513fbc1283aa2dc80c000022',
        'https://www.nutritionix.com/brand/texas-roadhouse/products/d3ea0422d63a633f2c3eb6f4',
        'https://www.nutritionix.com/brand/chick-fil-a/products/513fbc1283aa2dc80c000025',
        'https://www.nutritionix.com/brand/scooters-coffee/products/513fbc1283aa2dc80c00061d'
             ]
base_urls = [url + "?page=" for url in urls]

def get_item_ids(soup):
    item_ids = []
    for item in soup.find_all('tr', class_='item-row item-hover ng-scope'):
        href = item.get('href')
        if href:
            item_ids.append(href)
    item_ids = [id.split('/')[-1] for id in item_ids]
    return item_ids

def get_current_page_from_title(soup):
    title = soup.find('title').text
    match = re.search(r'Page (\d+)', title)
    if match:
        return int(match.group(1))
    return None

def main(base_url):
    # Start from page 1
    page = 1
    all_item_ids = []

    while True:
        # Modify the URL to load the appropriate page
        url = f'{base_url}{page}'

        # Load the page
        driver.get(url)

        sleep_time_int = random.uniform(2, 6)
        sleep_time_dec = random.uniform(1, 100)
        sleep_time = sleep_time_int + (sleep_time_dec/100)
        time.sleep(sleep_time)

        # Wait for JavaScript to load
        driver.implicitly_wait(sleep_time)

        # Get the page source after JavaScript execution
        html = driver.page_source

        # Parse with BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        current_page_number = get_current_page_from_title(soup)


        if current_page_number is None or current_page_number != page:
            break

        current_page_ids = get_item_ids(soup)
        # Add current page items to all items list
        all_item_ids.extend(current_page_ids)
        print(f'complete page {page}')

        # Move to the next page
        page += 1
    return all_item_ids

# Initialize an empty DataFrame to store the item IDs
df = pd.DataFrame(columns=['Brand', 'Item_ID'])

# Main loop to process each base URL
for base_url in base_urls:
    # Extract the brand name from the URL for labeling purposes in the DataFrame
    brand_name = base_url.split('/')[4]  # Adjust according to the actual URL format

    # Use the main function to get all item IDs for this brand
    item_ids = main(base_url)

    # Create a DataFrame from the current brand's item IDs
    temp_df = pd.DataFrame(item_ids, columns=['Item_ID'])
    temp_df['Brand'] = brand_name  # Add a column for the brand name

    # Append the current brand's DataFrame to the main DataFrame
    df = pd.concat([df, temp_df], ignore_index=True)

# Close the browser after processing all URLs
driver.quit()

# Export the DataFrame to a CSV file
csv_filename = 'item_ids.csv'
df.to_csv(csv_filename, index=False)

# Print a message to confirm export
print(f"Data successfully exported to {csv_filename}")