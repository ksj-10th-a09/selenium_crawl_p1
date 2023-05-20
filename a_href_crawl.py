from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
from urllib import request
from urllib.error import HTTPError

from urllib.request import Request, urlopen

url='http://192.168.161.133/DVWA/'

service = Service('./chromedriver.exe')
driver = webdriver.Chrome(service=service)
driver.get(url)

li_list = driver.find_elements(By.TAG_NAME, "li")
href_list = []

for li in li_list:
    a_tag = li.find_element(By.TAG_NAME, "a")
    href_text=a_tag.get_attribute('href')
    href_list.append(href_text)

    for i in href_list:
        # html = urlopen(str_i)
        try:
            # html = Request(i, headers={'User-Agent':'Chrome/66.0.3359.181'})
            # html_page = urlopen(html).read()
            html = urlopen(i)
            web_data = BeautifulSoup(html, "html.parser")

            file_name = i.replace('/', '-')

            with open(f'{file_name}.txt', 'w', encoding='utf-8') as file:
                file.write(str(web_data))
                file.close()

            print(f'URL saved as: {file_name}')

        except HTTPError as e:
            print(e)

        except AttributeError as e:
            print(e)

