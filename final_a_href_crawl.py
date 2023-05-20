from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import os
from urllib.error import HTTPError


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


service = Service('./chromedriver.exe')
driver = webdriver.Chrome(service=service)


save_directory = 'crawled_files'
os.makedirs(save_directory, exist_ok=True)

for href_url in href_list:

        try:
            driver.get(href_url)
            html_source = driver.page_source

            sliced_url = href_url[len("http://"):]
            file_name = f'{sliced_url.replace("/", "_").replace("?","_")}.txt'

            file_path = os.path.join(save_directory, file_name)

            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(str(html_source))

            print(f'Page saved as: {file_path}')


        except HTTPError as e:
            print(e)

        except AttributeError as e:
            print(e)

