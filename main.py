import argparse
import os
import get_html
import re
from crawler import Crawler
from urllib.parse import urlparse

global links

# Parameter parsing
parser = argparse.ArgumentParser(description="K-Shield Jr. 10th Python Crawling Project")
parser.add_argument('-u', '--url', action='store', default='', help='분석을 원하는 사이트 주소를 입력해 주십시오.', required=True)
parser.add_argument('-e', '--exclude', action='store', default='', help='URL에서 제외할 단어 혹은 패턴을 입력해 주십시오.')
parser.add_argument('-b', '--browser', action='store', default='Edge', help='사용할 브라우저를 선택 합니다')
parser.add_argument('-t', '--tag', action='store', default='True', help='Tag를 검색합니다')

# Init var
args = parser.parse_args()
url = args.url.rstrip("/")
domain = urlparse(url).netloc

# Make dir with domain name
path = f'./{domain}'
if not os.path.exists(path) or not os.path.exists(path + '/_sitemap_.txt'):
    os.makedirs(path, exist_ok=True)

    crawler = Crawler(url, exclude=args.exclude, no_verbose=False)
    links = crawler.start()

    # Write all url to text file
    result = []

    for link in links:
        if not re.match(r'^https?://', link):
            if args.tag == 'False':
                link = re.sub(r'(?:tags?|tag|#.*$)', '', link)
            result.append(link.strip())

    try:
        with open(path + '/_parsing_.txt', "w") as file:
            for link in result:
                file.write(link.strip('/').strip() + '\n')

    except IOError as e:
        print('Error: ', e)

try:
    with open(path + '/_parsing_.txt', 'r') as r, open(path + '/_sitemap_.txt', 'w') as o:
        o.write('\n')
        seen = set()
        for line in r:
            if line.strip():
                if line not in seen:
                    seen.add(line)
                    o.write(line)
except IOError as e:
    print('Error: ', e)

try:
    f = open(path + '/_sitemap_.txt', 'r')

except FileNotFoundError:
    print('ERROR: File Not Found')

else:
    links = f.readlines()

    get_html.init(domain)
    for link in links:
        get_html.start(url + '/' + link)
