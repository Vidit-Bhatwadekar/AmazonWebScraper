# fileName='JSONs/reviews_Video_Games_5.json' # path to the file you want to use to scrape
fileNameList = ['reviews_Beauty_5.json', 'reviews_Clothing_Shoes_and_Jewelry_5.json',  'reviews_Electronics_5.json', 'reviews_Grocery_and_Gourmet_Food_5.json', 'reviews_Health_and_Personal_Care_5.json', 'reviews_Home_and_Kitchen_5.json', 'reviews_Musical_Instruments_5.json', 'reviews_Office_Products_5.json', 'reviews_Sports_and_Outdoors_5.json']
# saveDirectory='scraped/' # path to the folder to save the scraped data into
scrape_limit=3 # not every product can be succesfully scraped so add some extra 500 for items

from selenium import webdriver
import pandas as pd
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotVisibleException
import json
import sys

chromedriverPath = '/Users/vidit/Desktop/RandomProj/Ryan_Data/chromedriver' # Path to the chromium driver

def get_asins(file):
    #input json file in fileNameList
    #Output is array of unique product ASIN numbers
    data = pd.read_json(file, lines=True)
    uniqueproducts = data.asin.unique()
    return uniqueproducts

def parse_about(driver,url):
    driver.get(f'https://www.amazon.com/dp/{url}')
    product=''
    try:
        productDesc = driver.find_element_by_id('productDescription')

        if productDesc:
            allp = productDesc.find_elements_by_tag_name("p")
            description=''

            for p in allp:
                description+=p.text
                description+='\n\n'
            return description
        else:
            ul = driver.find_element_by_css_selector('ul.a-unordered-list.a-vertical.a-spacing-mini')
            allli = ul.find_elements_by_tag_name("li")
            description = ''
            for li in allli:
                description += (li.text+'.')
            return description
    except ElementNotVisibleException:
        print("\tpage not available!")
        return ''
    except Exception:
        print("\tcannot get product description")
        return ''


def get_descriptions(uniqueproducts):
    #Input uniqueproducts ASIN
    #no Returns, but creates CSV of Descriptions
    result = []
    for i,prod in enumerate(uniqueproducts):
        if i==scrape_limit:
            break
        if i%100==0:
            print("program running:",len(result))
        try:
            result.append(parse_about(driver,prod).replace('..','.'))
        except:
            pass

    df = pd.DataFrame()
    df['description'] = result
    df.to_csv(fileName.replace('.json','.csv'))

driver=webdriver.Chrome(chromedriverPath)
for fileName in fileNameList:
    filePath = 'JSONs/'+fileName
    asin_list = get_asins(filePath)
    get_descriptions(asin_list)
