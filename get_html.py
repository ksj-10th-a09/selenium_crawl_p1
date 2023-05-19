import time
from selenium import webdriver

SCROLL_PAUSE_SEC = 1  # Seconds for wait after scroll down


def init(in_domain, in_browser='Edge'):  # Selenium browser init func
    global options
    global domain
    global browser
    global driver
    global cookie

    domain = in_domain
    browser = in_browser
    cookie = {}

    driver_options = {
        'Edge': webdriver.EdgeOptions(),
        'Chrome': webdriver.ChromeOptions(),
        'Firefox': webdriver.FirefoxOptions()
    }

    options = driver_options.get(browser)
    options.add_argument('window-size=1920,1080')

    driver_executables = {
        'Edge': './msedgedriver.exe',
        'Chrome': './chromedriver.exe',
        'Firefox': './geckodriver.exe'
    }

    driver = webdriver.__getattribute__(browser)(executable_path=driver_executables.get(browser), options=options)


def addCookie(name, value):
    print(f'Adding [{name}] = {value}')
    cookie[name] = value


def start(in_url):
    driver.get(url=in_url)
    if len(cookie) != 0:
        for name, value in cookie.items():
            driver.add_cookie({'name': name, 'value': value})
    driver.implicitly_wait(time_to_wait=10)

    while True:
        last_height = driver.execute_script("return document.body.scrollHeight")

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_SEC)

        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break

    html_source = driver.page_source

    try:
        file_name = in_url.replace('http://', '').replace('https://', '').replace(domain, 'root').replace('\n',
                                                                                                          '').replace(
            '\\', '_') \
            .replace('/', '__').replace('"', '_')
        with open(f"./{domain}/{file_name}.txt", "w", encoding='utf-8') as f:
            f.write(html_source)
        print('Saved ' + in_url.strip())

    except OSError as e:
        print('Unsupported file name')
        print(e)
