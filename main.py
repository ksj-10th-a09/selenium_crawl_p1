import selenium
import time
import os
from urllib.parse import urlparse

from selenium import webdriver

URL = 'https://minnote.net'
domain = urlparse(URL).netloc

options = webdriver.EdgeOptions()
options.add_argument('window-size=1920,1080')

driver = webdriver.Edge(executable_path='msedgedriver', options=options)
driver.get(url=URL)

# Wait until load
driver.implicitly_wait(10) # Implicit

SCROLL_PAUSE_SEC = 1

# Get Scroll Height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to end
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_SEC)

    # Get scroll height again after scroll down
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

html_source = driver.page_source
title = driver.title

os.mkdir("./" + domain)
f=open("./" + domain + "/" + title + ".txt", "w", encoding='utf-8')
f.write(html_source)
f.close()
