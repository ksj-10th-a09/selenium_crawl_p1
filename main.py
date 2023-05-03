import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

URL = 'https://www.google.com'

options = webdriver.EdgeOptions()
options.add_argument('window-size=1920,1080')

driver = webdriver.Edge(executable_path='msedgedriver', options=options)
driver.get(url=URL)

# Get URL
# print(driver.current_url)

# Close Driver
# driver.close()

# Wait until load
# driver.implicitly_wait(time_to_wait=5) # Implicit

search_box = driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input')

search_box.send_keys('minnote.net')
search_box.send_keys(Keys.RETURN)

elements = driver.find_elements_by_xpath('//*[@id="rso"]/div[*]/div/div[1]/a/h3/span')

for element in elements:
    print(element.text)
    print(element.text, file=open('output.txt', 'w', encoding='utf-8'))

sleep(3)
driver.close()