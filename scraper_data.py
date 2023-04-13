from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd
from bs4 import BeautifulSoup
driver = webdriver.Chrome()
driver.maximize_window()
home_list=[]
def getHomeData(pages):
    url = f"https://www.redfin.com/city/30772/OR/Portland/filter/include=sold-3mo/page-{pages}"
    # Go to site
    driver.get(url)
    # It takes awhile to load so we want to wait until the page is fully loaded
    # We also want to make sure we don't overload the server or get banned for acting too quickly
    time.sleep(20)
    # Get all links on the page
    links = driver.find_elements(By.TAG_NAME, "a")
    # get urls of the links
    urls = [link.get_attribute("href") for link in links]
    # filter out none
    urls = [url for url in urls if url is not None]
    # filter down to links that contain "homedetails"
    urls = [url for url in urls if "/home/" in url] # Redfin
    # Remove duplicates
    urls = list(set(urls))
    
    for x in urls:
        # GO to the link
        driver.get(x)
        time.sleep(20)
        ### Get all data on the house  
        html = driver.page_source
        s_redfin = BeautifulSoup(html, 'html.parser') 
        try:    
            home= {
            # Get Url
            'url': x,
            # Get sold price
            'price' : s_redfin.find('div', {'data-rf-test-id':'abp-price'}).find('div', {'class':'statsValue'}).text,
            # Get beds
            'bed': s_redfin.find('div', {'data-rf-test-id':'abp-beds'}).find('div', {'class':'statsValue'}).text,
            # Get bathroom
            'bath' : s_redfin.find('div', {'data-rf-test-id':'abp-baths'}).find('div', {'class':'statsValue'}).text,
            # Get sqft
            'sqft' : s_redfin.find('div', {'data-rf-test-id':'abp-sqFt'}).find('span', {'class':'statsValue'}).text,
            # Get address
            'address' : s_redfin.find('div', {'data-rf-test-id':'abp-streetLine'}).text,
            # Get City
            'city' : s_redfin.find('div', {'data-rf-test-id':'abp-cityStateZip'}).text,
            # Get property Type
            'type' :driver.find_element(By.CSS_SELECTOR,'div.keyDetailsList:nth-child(2) > div:nth-child(2) > span:nth-child(2)').text,
            # Get Year built
            'year_built' :driver.find_element(By.CSS_SELECTOR,'div.keyDetailsList:nth-child(2) > div:nth-child(3) > span:nth-child(2)').text,
            # Get estimate price
            'est_price' : driver.find_element(By.CSS_SELECTOR,'div.keyDetailsList:nth-child(4) > div:nth-child(1) > span:nth-child(2)').text,
            # Get price per sqft
            'price_per_sqft' : driver.find_element(By.CSS_SELECTOR,'div.keyDetailsList:nth-child(4) > div:nth-child(2) > span:nth-child(2)').text,
            }   
            home_list.append(home) 
        except NoSuchElementException:
            print(f"Error: {x}")
            continue
    return     
for x in range(1,7):
    getHomeData (x)
# Put the data in a Pandas Dataframe 
df = pd.DataFrame(home_list)
df.to_csv('houses.csv', index=False, encoding='utf-8')
driver.quit()
