import time
from selenium import webdriver

SCROLL_PAUSE_SEC = 1    # Seconds for wait after scroll down


def init(in_domain, in_browser='Edge'):  # Selenium browser init func
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
        driver = webdriver.Chrome(executetable_path='chromedriver', options=options)

    elif browser == 'Firefox':
        options = webdriver.FirefoxOptions()
        options.add_argument('window-size=1920,1080')
        driver = webdriver.Firefox(executetable_path='chromedriver', options=options)


def start(in_url):
    driver.get(url=in_url)

    # Wait until load
    driver.implicitly_wait(time_to_wait=10)  # Implicit

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

    # File write part
    try:
        file_name = in_url.replace('http://', '').replace('https://', '').replace('\n', '').replace('\\', '_') \
            .replace('/', '__').replace('"', '_').replace(domain, 'root')

        f = open("./" + domain + '/' + file_name + ".txt", "w", encoding='utf-8')
        print('Saved ' + in_url)
        f.write(html_source)
        f.close()

    except FileNotFoundError as e:
        print('Unsupported file name')

    except Exception as e:
        print(e)
