from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from urllib.parse import parse_qsl, urljoin, urlparse
from urllib.parse import urlparse
from bs4 import BeautifulSoup

def save_url_as_file(url):

    domain = urlparse(url).netloc


    filename = f'{domain}.txt'


    with open(filename, 'w') as file:
        file.write(url)

    print(f'URL saved as: {filename}')

def crawl_and_save(url):

    driver_path = './chromedriver.exe'  # Replace with the path to your chromedriver executable
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run Chrome in headless mode (without opening a browser window)
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)


    driver.get(url)
    original_content = driver.page_source
    save_url_as_file(url)


    soup = BeautifulSoup(original_content, 'html.parser')


    links = soup.find_all('a')


    for link in links:
        href = link.get('href')
        if href:
            linked_url = urljoin(url, href)
            save_url_as_file(linked_url)


    driver.quit()


url = "https://www.kisec.com/accounts/login_pd.do"
crawl_and_save(url)