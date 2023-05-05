import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup

URL = 'https://minnote.net'

options = webdriver.EdgeOptions()
options.add_argument('window-size=1920,1080')

driver = webdriver.Edge(executable_path='msedgedriver', options=options)
driver.get(url=URL)

# Get URL
# print(driver.current_url)

# Close Driver
# driver.close()

# Wait until load
driver.implicitly_wait(time_to_wait=10) # Implicit
html_source = driver.page_source
f=open("output.txt","w", encoding='utf-8')
f.write(html_source)
f.close()