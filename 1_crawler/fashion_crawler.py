# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup
from time import sleep
from multiprocessing import Pool
import urllib
import argparse
import os, sys
from tqdm import trange


def check_exists_by_class(className):
    try:
        driver.find_element_by_class_name(className)
    except NoSuchElementException:
        return False
    return True

def scroll(scroll_num=50):
    element = driver.find_element_by_tag_name("body")
    print("Processing scrolling")
    if scroll_num < 25:
        for _ in trange(scroll_num):
            element.send_keys(Keys.PAGE_DOWN)
            sleep(0.2)
    elif scroll_num >= 25:
        for _ in trange(25):
            element.send_keys(Keys.PAGE_DOWN)
            sleep(0.2)
        driver.find_element_by_id("smb").click()
        for _ in trange(scroll_num - 25):
            element.send_keys(Keys.PAGE_DOWN)
            sleep(0.2)
    print("Scrolling Done")

def click_image(driver):
    if check_exists_by_class("rg_ic"):
        imgs = driver.find_elements_by_class_name('rg_ic')
        links = set()
        print("\nImage length :", len(imgs))
        for i in trange(len(imgs)):
            driver.execute_script("document.querySelectorAll('.rg_ic')[%i].click()" % i)
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            html_irc = soup.select('.irc_mi')
            for i in range(3):
                src = html_irc[i].get('src')
                links.add(src)
        links = list(links)
        if None in links:
            links.remove(None)
        print("Parsed number :", len(links))
        return (links)
    else:
        print('There is no element')

def change_dir(query):
    if not os.path.isdir(query):
        os.makedirs(query)
    path = str(os.getcwd()) + '/' + query
    os.chdir(path)

def download_img(link):
    try:
        if link.split('.')[-1] == ('jpg' or 'png' or 'jpeg'):
            urllib.request.urlretrieve(link, link.split('/')[-1])
    except:
        pass

if __name__ == '__main__':
#    import pdb;pdb.set_trace()
    cromeDriverPath = "./chromedriver"
    driver = webdriver.Chrome(cromeDriverPath)
    
    parser = argparse.ArgumentParser()
    parser.add_argument("keyword", help="the keyword to search")
    parser.add_argument("-s", "--scroll", required=False)
    args = parser.parse_args()
    query = args.keyword
    scroll_num = 50
    scroll_check = args.scroll
    if scroll_check != None:
        scroll_num = int(args.scroll)

    # set stack limit
    sys.setrecursionlimit(100000000)
    
    rootUrl = "https://www.google.co.kr/search?q=" + query + \
                  "&hl=ko&tbs=isz:m,itp:photo&tbm=isch&source=lnt&sa=X&ved=0ahUKEwik15nahpDdAhVGvrwKHU9JCsIQpwUIGw&biw=1249&bih=883&dpr=1"

    driver.get(rootUrl)

    # Use scroll for several times.
    # DEFAULT scroll_num=50
    scroll(scroll_num)
    
    # Get the image links
    links = click_image(driver)
    
    # Create the directory
    print("Create directory :", query)
    change_dir(query)
    
    # Download image links
    print("Downloading images")
    with Pool() as pool:
        pool.map(download_img, links)
    print("Finished")