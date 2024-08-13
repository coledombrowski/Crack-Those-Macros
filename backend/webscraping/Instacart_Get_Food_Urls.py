from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import time
import re
from selenium.webdriver.common.keys import Keys
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)


Instacart_Stores = {'Food Lion':[   'https://www.instacart.com/store/food-lion-now-convenience/collections/2703-frozen-entrees',
                                    'https://www.instacart.com/store/food-lion-now-convenience/collections/2707-frozen-breakfast',
                                    'https://www.instacart.com/store/food-lion-now-convenience/collections/2706-frozen-meat',
                                    'https://www.instacart.com/store/food-lion-now-convenience/collections/2704-frozen-snacks',
                                    'https://www.instacart.com/store/food-lion-now-convenience/collections/2705-frozen-vegetables',
                                    'https://www.instacart.com/store/food-lion-now-convenience/collections/2708-frozen-fruit',
                                    'https://www.instacart.com/store/food-lion-now-convenience/collections/2822-meats',
                                    'https://www.instacart.com/store/food-lion-now-convenience/collections/2819-salads',
                                    'https://www.instacart.com/store/food-lion-now-convenience/collections/2823-sides',
                                    'https://www.instacart.com/store/food-lion-now-convenience/collections/2818-sandwiches'],
                    'Publix':[   'https://www.instacart.com/store/publix/collections/beef',
                                    'https://www.instacart.com/store/publix/collections/pork',
                                    'https://www.instacart.com/store/publix/collections/603-chicken',
                                    'https://www.instacart.com/store/publix/collections/fish',
                                    'https://www.instacart.com/store/publix/collections/shellfish',
                                    'https://www.instacart.com/store/publix/collections/hot-dogs-sausages',
                                    'https://www.instacart.com/store/publix/collections/968-lamb',
                                    'https://www.instacart.com/store/publix/collections/604-turkey',
                                    'https://www.instacart.com/store/publix/collections/668-meat-alternatives',
                                    'https://www.instacart.com/store/publix/collections/fresh-vegetables',
                                    'https://www.instacart.com/store/publix/collections/fresh-fruits',
                                 'https://www.instacart.com/store/publix/collections/ice-cream',
                                 'https://www.instacart.com/store/publix/collections/apps-snacks',
                                 'https://www.instacart.com/store/publix/collections/pizza-meals',
                                 'https://www.instacart.com/store/publix/collections/frozen-breakfast',
                                 'https://www.instacart.com/store/publix/collections/meat-seafood',
                                 'https://www.instacart.com/store/publix/collections/vegetables',
                                 'https://www.instacart.com/store/publix/collections/frozen-fruits',
                                 'https://www.instacart.com/store/publix/collections/desserts',
                                 'https://www.instacart.com/store/publix/collections/breads-doughs',
                                 'https://www.instacart.com/store/publix/collections/cookies-brownies',
                                 'https://www.instacart.com/store/publix/collections/buns-rolls',
                                 'https://www.instacart.com/store/publix/collections/cakes-pies',
                                 'https://www.instacart.com/store/publix/collections/breakfast-pastries',
                                 'https://www.instacart.com/store/publix/collections/bread',
                                 'https://www.instacart.com/store/publix/collections/specialty-desserts',
                                 'https://www.instacart.com/store/publix/collections/bagels-english-muffins',
                                 'https://www.instacart.com/store/publix/collections/frozen-baked-goods',
                                 'https://www.instacart.com/store/publix/collections/tortillas-flatbreads',
                                 'https://www.instacart.com/store/publix/collections/9798-cookies-sweet-treats',
                                 'https://www.instacart.com/store/publix/collections/chips',
                                 'https://www.instacart.com/store/publix/collections/chocolate-candy',
                                 'https://www.instacart.com/store/publix/collections/9797-crackers',
                                 'https://www.instacart.com/store/publix/collections/popcorn',
                                 'https://www.instacart.com/store/publix/collections/popcorn',
                                 'https://www.instacart.com/store/publix/collections/snack-bars',
                                 'https://www.instacart.com/store/publix/collections/9796-dried-fruit-fruit-snacks',
                                 'https://www.instacart.com/store/publix/collections/jerky',
                                 'https://www.instacart.com/store/publix/collections/873-more-snacks',
                                 'https://www.instacart.com/store/publix/collections/9804-fruit-cups-applesauce',
                                 'https://www.instacart.com/store/publix/collections/9805-pudding-gelatin',
                                 'https://www.instacart.com/store/publix/collections/962-boxed-meals',
                                 'https://www.instacart.com/store/publix/collections/pasta',
                                 'https://www.instacart.com/store/publix/collections/rices-grains',
                                 'https://www.instacart.com/store/publix/collections/noodles',
                                 'https://www.instacart.com/store/publix/collections/dried-beans',
                                 'https://www.instacart.com/store/publix/collections/seeds',
                                 'https://www.instacart.com/store/publix/collections/eggs',
                                 'https://www.instacart.com/store/publix/collections/cheese',
                                 'https://www.instacart.com/store/publix/collections/yogurt',
                                 'https://www.instacart.com/store/publix/collections/3102-chicken',
                                 'https://www.instacart.com/store/publix/collections/3096-sandwiches-wraps',
                                 'https://www.instacart.com/store/publix/collections/3101-salads',
                                 'https://www.instacart.com/store/publix/collections/3105-meal-kits',
                                 'https://www.instacart.com/store/publix/collections/3097-pizza-meals',
                                 'https://www.instacart.com/store/publix/collections/3098-sushi',
                                 'https://www.instacart.com/store/publix/collections/3100-soups',
                                 'https://www.instacart.com/store/publix/collections/3103-other-prepared-meats',
                                 'https://www.instacart.com/store/publix/collections/3099-party-platters',
                                 'https://www.instacart.com/store/publix/collections/3104-snack-packs',
                                 'https://www.instacart.com/store/publix/collections/soups',
                                 'https://www.instacart.com/store/publix/collections/canned-beans',
                                 'https://www.instacart.com/store/publix/collections/canned-fruits',
                                 'https://www.instacart.com/store/publix/collections/canned-fish',
                                 'https://www.instacart.com/store/publix/collections/canned-meals',
                                 'https://www.instacart.com/store/publix/collections/canned-meat',
                                 'https://www.instacart.com/store/publix/collections/634-cereal',
                                 'https://www.instacart.com/store/publix/collections/oatmeal',
                                 'https://www.instacart.com/store/publix/collections/granola',
                                 'https://www.instacart.com/store/publix/collections/nut-butters',
                                 'https://www.instacart.com/store/publix/collections/toaster-pastries',
                                 'https://www.instacart.com/store/publix/collections/breakfast-bars',
                                'https://www.instacart.com/store/publix/collections/pancake-waffle',
                                 'https://www.instacart.com/store/publix/collections/3090-deli-meats',
                                 'https://www.instacart.com/store/publix/collections/34807-meat-cheese-combos',
                                 'https://www.instacart.com/store/publix/collections/3091-cheese',
                                 'https://www.instacart.com/store/publix/collections/rc-ready_to_cook_meals_for_one',
                                 'https://www.instacart.com/store/publix/collections/rc-ready_to_cook_meal_kits',
                                 'https://www.instacart.com/store/publix/collections/rc-ready_to_cook_ready_to_cook'


                                 ],
                    'Kroger':[   'https://www.instacart.com/store/kroger-delivery-now/collections/2703-frozen-entrees',
                                    'https://www.instacart.com/store/kroger-delivery-now/collections/2706-frozen-meat',
                                    'https://www.instacart.com/store/kroger-delivery-now/collections/2707-frozen-breakfast',
                                    'https://www.instacart.com/store/kroger-delivery-now/collections/2704-frozen-snacks',
                                    'https://www.instacart.com/store/kroger-delivery-now/collections/2705-frozen-vegetables',
                                    'https://www.instacart.com/store/kroger-delivery-now/collections/2708-frozen-fruit',
                                    'https://www.instacart.com/store/kroger-delivery-now/collections/2822-meats',
                                    'https://www.instacart.com/store/kroger-delivery-now/collections/2819-salads',
                                    'https://www.instacart.com/store/kroger-delivery-now/collections/2821-sushi',
                                    'https://www.instacart.com/store/kroger-delivery-now/collections/2818-sandwiches',
                                 'https://www.instacart.com/store/kroger-delivery-now/collections/2820-soups',
                                 'https://www.instacart.com/store/kroger-delivery-now/collections/2823-sides'],
                    'Aldi':['https://www.instacart.com/store/aldi-express/collections/2706-frozen-meat',
                            'https://www.instacart.com/store/aldi-express/collections/2703-frozen-entrees',
                            'https://www.instacart.com/store/aldi-express/collections/2707-frozen-breakfast',
                            'https://www.instacart.com/store/aldi-express/collections/2704-frozen-snacks',
                            'https://www.instacart.com/store/aldi-express/collections/2708-frozen-fruit',
                            'https://www.instacart.com/store/aldi-express/collections/2705-frozen-vegetables',
                            'https://www.instacart.com/store/aldi-express/collections/2669-breakfast-pastries',
                            'https://www.instacart.com/store/aldi-express/collections/2668-bread',
                            'https://www.instacart.com/store/aldi-express/collections/2670-cookies-treats',
                            'https://www.instacart.com/store/aldi-express/collections/2671-buns-rolls',
                            'https://www.instacart.com/store/aldi-express/collections/2672-tortillas'
                            ],
                    'The Fresh Market':[
                        'https://www.instacart.com/store/the-fresh-market-express/collections/2705-frozen-vegetables',
                        'https://www.instacart.com/store/the-fresh-market-express/collections/2704-frozen-snacks',
                        'https://www.instacart.com/store/the-fresh-market-express/collections/2703-frozen-entrees',
                        'https://www.instacart.com/store/the-fresh-market-express/collections/2706-frozen-meat',
                        'https://www.instacart.com/store/the-fresh-market-express/collections/2707-frozen-breakfast',
                        'https://www.instacart.com/store/the-fresh-market-express/collections/2708-frozen-fruit',
                        'https://www.instacart.com/store/the-fresh-market-express/collections/2666-more-cheese',
                        'https://www.instacart.com/store/the-fresh-market-express/collections/2656-cheddar',
                        'https://www.instacart.com/store/the-fresh-market-express/collections/2658-mozzarella',
                        'https://www.instacart.com/store/the-fresh-market-express/collections/2657-shredded-cheese',
                        'https://www.instacart.com/store/the-fresh-market-express/collections/2661-swiss',
                        'https://www.instacart.com/store/the-fresh-market-express/collections/2662-pepperjack',
                        'https://www.instacart.com/store/the-fresh-market-express/collections/2659-american'
                    ],
                    'Target':[
                        'https://www.instacart.com/store/target-fast-delivery/collections/2703-frozen-entrees',
                        'https://www.instacart.com/store/target-fast-delivery/collections/2706-frozen-meat',
                        'https://www.instacart.com/store/target-fast-delivery/collections/2704-frozen-snacks',
                        'https://www.instacart.com/store/target-fast-delivery/collections/2707-frozen-breakfast',
                        'https://www.instacart.com/store/target-fast-delivery/collections/2708-frozen-fruit',
                        'https://www.instacart.com/store/target-fast-delivery/collections/2705-frozen-vegetables',
                        'https://www.instacart.com/store/target-fast-delivery/collections/2682-chocolate',
                        'https://www.instacart.com/store/target-fast-delivery/collections/2680-chips',
                        'https://www.instacart.com/store/target-fast-delivery/collections/2681-candy',
                        'https://www.instacart.com/store/target-fast-delivery/collections/2687-granola-bars',
                        'https://www.instacart.com/store/target-fast-delivery/collections/2683-crackers',
                        'https://www.instacart.com/store/target-fast-delivery/collections/2685-popcorn',
                        'https://www.instacart.com/store/target-fast-delivery/collections/2689-fruit-snacks',
                        'https://www.instacart.com/store/target-fast-delivery/collections/2688-pudding',
                        'https://www.instacart.com/store/target-fast-delivery/collections/2686-pretzels',
                        'https://www.instacart.com/store/target-fast-delivery/collections/2684-cookies'
                    ],
                    'CVS': [
                        'https://www.instacart.com/store/cvs/collections/938-ice-cream-desserts',
                        'https://www.instacart.com/store/cvs/collections/940-meals',
                        'https://www.instacart.com/store/cvs/collections/939-snacks',
                        'https://www.instacart.com/store/cvs/collections/950-candy-chocolate',
                        'https://www.instacart.com/store/cvs/collections/948-chips',
                        'https://www.instacart.com/store/cvs/collections/949-cookies-baked-treats',
                        'https://www.instacart.com/store/cvs/collections/953-nuts-dried-fruits',
                        'https://www.instacart.com/store/cvs/collections/952-jerky-popcorn',
                        'https://www.instacart.com/store/cvs/collections/955-snack-bars',
                        'https://www.instacart.com/store/cvs/collections/956-crackers',
                        'https://www.instacart.com/store/cvs/collections/954-snack-mixes',
                        'https://www.instacart.com/store/cvs/collections/959-more-snacks'

                    ],
                    'Walgreens': [
                        'https://www.instacart.com/store/walgreens/collections/938-ice-cream-desserts',
                        'https://www.instacart.com/store/walgreens/collections/940-meals',
                        'https://www.instacart.com/store/walgreens/collections/939-snacks',
                        'https://www.instacart.com/store/walgreens/collections/942-more-frozen',
                        'https://www.instacart.com/store/walgreens/collections/950-candy-chocolate',
                        'https://www.instacart.com/store/walgreens/collections/948-chips',
                        'https://www.instacart.com/store/walgreens/collections/949-cookies-baked-treats',
                        'https://www.instacart.com/store/walgreens/collections/952-jerky-popcorn',
                        'https://www.instacart.com/store/walgreens/collections/953-nuts-dried-fruits',
                        'https://www.instacart.com/store/walgreens/collections/956-crackers',
                        'https://www.instacart.com/store/walgreens/collections/955-snack-bars',
                        'https://www.instacart.com/store/walgreens/collections/954-snack-mixes',
                        'https://www.instacart.com/store/walgreens/collections/959-more-snacks'
                    ]
}


def getItems(IC_URL):

    options = Options()
    options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'

    service = Service(executable_path=r'C:\Users\2cona\OneDrive\Advanced Software Engineering\Local Dev\geckodriver.exe')
    driver = webdriver.Firefox(service=service, options=options)
    driver.get(IC_URL)
    driver.implicitly_wait(10)
    try:
        # Wait for the element to be present
        time.sleep(1.5)
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[6]/div"))
        )
        # Execute JavaScript to remove the element
        driver.execute_script("arguments[0].parentNode.removeChild(arguments[0]);", element)
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[7]/div"))
        )
        # Execute JavaScript to remove the element
        driver.execute_script("arguments[0].parentNode.removeChild(arguments[0]);", element)
    except Exception as e:
        print(e)
    # driver.execute_script("document.body.style.zoom='30%'")
    # Create a var of the window
    # Set the focus to the browser rather than the web content
    driver.set_context("chrome")
    # Create a var of the window
    win = driver.find_element(by=By.TAG_NAME, value="html")
    win.send_keys(Keys.CONTROL + "-")
    win.send_keys(Keys.CONTROL + "-")
    win.send_keys(Keys.CONTROL + "-")
    win.send_keys(Keys.CONTROL + "-")
    win.send_keys(Keys.CONTROL + "-")
    # Set the focus back to content to re-engage with page elements
    driver.set_context("content")
    time.sleep(7.5)

    elements = driver.find_elements(By.TAG_NAME, 'a')

    # List to store extracted values
    product_ids = []

    # Regex pattern to extract the product ID
    pattern = re.compile(r'\/products\/(\d+)-')

    # Loop through found <a> elements and extract IDs
    for element in elements:
        href = element.get_attribute('href')
        if href:
            match = pattern.search(href)
            if match:
                product_ids.append(match.group(1))

    # Print all product IDs
    driver.close()
    print(product_ids)
    return product_ids

def getItemURLs(Store_Name):
    df = pd.DataFrame(columns=['Store', 'URLs'])

    URL_List = Instacart_Stores[Store_Name]
    Base = 'https://www.instacart.com/products/'
    for URL in URL_List:
        product_list = getItems(URL)
        product_urls = [Base + s for s in product_list]
        unique_urls = list(set(product_urls))  # Removing duplicates
        # Append new rows to the DataFrame for each unique URL
        for url in unique_urls:
            df = df.append({'Store': Store_Name, 'URLs': url}, ignore_index=True)
    return df





combined_df = pd.DataFrame()

for key in Instacart_Stores:
    df = getItemURLs(key)
    csv_file_path = f"{key}_product_URLs.csv"
    df.to_csv(csv_file_path, index=False)
    print(f'{key} complete!')
    time.sleep(.5)
