from selenium import webdriver
from selenium.common import UnexpectedAlertPresentException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import os
from urllib.error import HTTPError

# URL 입력
url='https://www.google.com'

service = Service('./chromedriver.exe')
driver = webdriver.Chrome(service=service)
driver.get(url)

# a 태그 찾기
a_tag = driver.find_elements(By.TAG_NAME, "a")

# href 속성 리스트 선언
href_list = []

# a 태그 내 href 속성 탐색 후 href_list에 추가
for li in a_tag:
    href_text = li.get_attribute('href')
    href_list.append(href_text)


result = []

# 리스트 중복 제거
for value in href_list:
    if value not in result:
        result.append(value)

strr = "http"

# 수집한 링크 중 http로 시작하지 않는 링크 (ex. javascript;;;, tel.02~ 등 삭제)
for word in result:
    if strr not in word:
        result.remove(word)

"""------------------------"""

service = Service('./chromedriver.exe')
driver = webdriver.Chrome(service=service)

# text 파일 저장 경로 설정
save_directory = 'crawled_dvwa'
os.makedirs(save_directory, exist_ok=True)


for href_url in result:
    try:
        driver.get(href_url)
        html_source = driver.page_source

        # 파일 제목으로 입력할 수 없는 문자 제거
        sliced_url = href_url[len("http://"):]
        file_name = f'{sliced_url.replace("/", "_").replace("?", "_")}.txt'

        file_path = os.path.join(save_directory, file_name)

        # text 파일 저장
        with open(file_path, 'w', encoding='utf-8') as file:
                file.write(str(html_source))

        print(f'Page saved as: {file_path}')


        # 404 not found 에러 예외 처리
    except HTTPError as e:
            print(e)

    # alert창이 나왔을 때 에러 예외 처리
    except UnexpectedAlertPresentException as e:
            print(e)

        # tag 타입 에러 예외 처리
    except AttributeError as e:
            print(e)