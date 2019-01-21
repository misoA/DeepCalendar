# -*- coding: utf-8 -*-
import os
import urllib
from time import sleep
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#%%
cromeDriverPath = "./chromedriver"
driver = webdriver.Chrome(cromeDriverPath)

SCROLL_PAUSE_TIME = 2
scroll_num = 50
delay = 5  # seconds


#%%
#TagURL
rootUrl = "https://www.instagram.com/explore/tags/가을코디룩/"
#UserURL
#rootUrl = "https://www.instagram.com/brandi__official/"
driver.get(rootUrl)
WebDriverWait(driver, delay).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'KL4Bh')))


#%%
# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

media_hrefs = set()

for i in range(scroll_num):
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    sleep(SCROLL_PAUSE_TIME)
    media_divs = driver.find_elements_by_tag_name('a')
    
    for media_div in media_divs:
        media_hrefs.add(media_div.get_attribute('href'))

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height


#%%
for media_href in list(media_hrefs):
    
    driver.get(media_href)
    try:
        imgUrl = BeautifulSoup(
                driver.page_source
                , 'html.parser').select('.KL4Bh')[0].select('img')[0].get('srcset').split(',')[-1:][0][:-5]
        dateSrting = driver.find_element_by_tag_name('time').get_attribute('datetime')[:10]
        
        dateDirPath = '../data/' + dateSrting
        if not os.path.isdir(dateDirPath):
            os.makedirs(dateDirPath)
        print("Downloading images " + dateDirPath)
        urllib.request.urlretrieve(
                imgUrl
                , filename=os.path.join(
                        dateDirPath
                        , imgUrl.split('/')[-1:][0]))
    except:
        pass
        
print("Finished")
driver.close()