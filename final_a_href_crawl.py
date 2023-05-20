from selenium.webdriver.common.by import By
import os
from urllib.error import HTTPError


def root_scan(url, driver):  # Scan root site for scanning internal page
    driver.get(url)

    li_list = driver.find_elements(By.TAG_NAME, "li")
    href_list = []

    for li in li_list:
        a_tag = li.find_element(By.TAG_NAME, "a")
        href_text = a_tag.get_attribute('href')
        href_list.append(href_text)

    return href_list


def save_to_file(list, path, driver):
    for href_url in list:
        try:
            driver.get(href_url)
            html_source = driver.page_source

            sliced_url = href_url[len("http://"):]
            file_name = f'{sliced_url.replace("/", "_").replace("?", "_")}.txt'

            file_path = os.path.join(path, file_name)

            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(str(html_source))

            print(f'Page saved: {file_path}')


        except HTTPError as e:
            print('Error: ', e)

        except AttributeError as e:
            print('Error: ', e)
