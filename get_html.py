import time
from urllib.parse import urlparse
from selenium import webdriver

SCROLL_PAUSE_SEC = 1

def init(in_domain, in_browser='Edge'):
    global options
    global domain
    global browser
    global driver

    domain = in_domain
    browser = in_browser

    if browser == 'Edge':
        options = webdriver.EdgeOptions()
        options.add_argument('window-size=1920,1080')
        driver = webdriver.Edge(executable_path='msedgedriver', options=options)

    elif browser == 'Chrome':
        options = webdriver.ChromeOptions()
        options.add_argument('window-size=1920,1080')
        driver = webdriver.ChromeOptions(executetable_path='chromedriver', options=options)

    else:
        options = webdriver.EdgeOptions()
        options.add_argument('window-size=1920,1080')
        driver = webdriver.Edge(executable_path='msedgedriver', options=options)

def start(in_url):
    driver.get(url=in_url)

    # Wait until load
    driver.implicitly_wait(time_to_wait=10) # Implicit

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
    try:
        file_name = in_url.replace('http://', '').replace('https://', '').replace('\n', '').replace('\\', '_').replace(domain, '').replace('/', '')

        f=open("./" + domain + '/' + file_name + ".txt", "w", encoding='utf-8')
        f.write(html_source)
        f.close()

    except Exception as e:
        print(e)