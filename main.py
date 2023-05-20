import argparse
import os

import final_a_href_crawl
import structured_data_save

from urllib.parse import urlparse
from selenium import webdriver

# Parameter parsing
parser = argparse.ArgumentParser(description="K-Shield Jr. 10th Python Crawling Project")
parser.add_argument('-u', '--url', action='store', default='', help='분석을 원하는 사이트 주소', required=True)
parser.add_argument('-b', '--browser', action='store', default='Edge', help='사용할 브라우저 선택 (Edge / Chrome / Firefox)')

# Init var
args = parser.parse_args()
url = args.url.rstrip("/")
domain = urlparse(url).netloc
browser = args.browser

# Make dir with domain name
directory_path = f'./{domain}'
parsing_file_path = f'{directory_path}/_parsing_.txt'
tag_file_path = f'{directory_path}/_tag_struct_.xlsx'

# Make workdir
os.makedirs(directory_path, exist_ok=True)

# Init Browser
driver_options = {
    'Edge': webdriver.EdgeOptions(),
    'Chrome': webdriver.ChromeOptions(),
    'Firefox': webdriver.FirefoxOptions()
}

options = driver_options.get(browser)
options.add_argument('window-size=1920,1080')
options.add_argument('--headless')  # Run Chrome in headless mode (without opening a browser window)

driver_executables = {
    'Edge': './msedgedriver.exe',
    'Chrome': './chromedriver.exe',
    'Firefox': './geckodriver.exe'
}

driver = webdriver.__getattribute__(browser)(executable_path=driver_executables.get(browser), options=options)

# Crawling All Page
try:
    root_href = final_a_href_crawl.root_scan(url, driver)
    final_a_href_crawl.save_to_file(root_href, directory_path, driver)

except FileNotFoundError:
    print('ERROR: File Not Found')

except IOError as e:
    print('Error: ', e)

# Scan specific tag and export to xlsx
try:
    txtf = structured_data_save.scan_txt(directory_path)
    tags = structured_data_save.extract_tags_from_files(txtf)
    structured_data_save.save_tags_to_excel(tags, tag_file_path)

except Exception as e:
    print('Error: ', e)

