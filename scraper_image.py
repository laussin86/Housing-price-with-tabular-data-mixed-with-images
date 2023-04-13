from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import urllib
from bs4 import BeautifulSoup
import urllib.error

driver = webdriver.Chrome()
driver.maximize_window()

def getHomeImages(pages):
    src = []
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
    urls = list(set(urls))
    for x in urls:
        driver.get(x)
    # Click on a picture
        try:
            driver.find_element(By.CLASS_NAME, "landscape").click()
            time.sleep(10)
        except NoSuchElementException:
            print("exception handled")
            continue
    # Download all photos
        try:
            html = driver.page_source
            s_redfin = BeautifulSoup(html, 'html.parser')
            try:
                photo_count_text = s_redfin.find('div', {'class':'PagerIndex'}).text.split('<!-- -->')[0].split(' ')
                photo_count = int(photo_count_text[2])
            except AttributeError:
            # handle the case where the 'div' element with class 'PagerIndex' is not found
                photo_count = 0
            for num in range(0, photo_count):
                next=driver.find_element(By.CSS_SELECTOR, "div.nav:nth-child(3)").click()
                time.sleep(5)
            images = driver.find_elements(By.XPATH, "//img[contains(@class,'inline-block')]")
            for img in images:
                src.append(img.get_attribute('src'))
            driver.find_element(By.CSS_SELECTOR, "svg.close:nth-child(3)").click()
            time.sleep(5)
            driver.find_element(By.CSS_SELECTOR, ".backButton > svg:nth-child(1)").click()
            time.sleep(5)
        except NoSuchElementException:
            print("exception handled")
        for i in range(len(src)):
            if src[i] is None:
                continue
            try:
                urllib.request.urlretrieve(str(src[i]), f'Houses/house{pages}_{i}.jpg')   
            except urllib.error.HTTPError:
                continue    
    return
for x in range(6,7):
    getHomeImages (x)
driver.quit()
        
