import argparse
import os
import re
import get_html
import structured_data_save
from crawler import Crawler
from urllib.parse import urlparse

# Parameter parsing
parser = argparse.ArgumentParser(description="K-Shield Jr. 10th Python Crawling Project")
parser.add_argument('-u', '--url', action='store', default='', help='분석을 원하는 사이트 주소', required=True)
parser.add_argument('-e', '--exclude', action='store', default='', help='URL에서 제외할 단어 혹은 패턴')
parser.add_argument('-b', '--browser', action='store', default='Edge', help='사용할 브라우저 선택 (Edge / Chrome / Firefox)')
parser.add_argument('-t', '--tag', action='store', default='True', help='Tag 검색 유무 (True or False)')
parser.add_argument('-c', '--cookie', action='store', default='', help='추키 여부 (쿠키1이름.쿠키1값,쿠키2이름.쿠키2값 ...')

# Init var
args = parser.parse_args()
url = args.url.rstrip("/")
domain = urlparse(url).netloc

# Make dir with domain name
directory_path = f'./{domain}'
parsing_file_path = f'{directory_path}/_parsing_.txt'
sitemap_file_path = f'{directory_path}/_sitemap_.txt'
tag_file_path = f'{directory_path}/_tag_struct_.xlsx'

if not os.path.exists(directory_path) or not os.path.exists(sitemap_file_path):
    os.makedirs(directory_path, exist_ok=True)

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
    with open(parsing_file_path, "w") as file:
        for link in result:
            file.write(link.strip('/').strip() + '\n')

    with open(parsing_file_path, 'r') as r, open(sitemap_file_path, 'w') as o:
        o.write('\n')
        seen = set()
        for line in r:
            if line.strip() and line not in seen:
                seen.add(line)
                o.write(line)

# Get html source from txt file
    get_html.init(domain, args.browser)

    if args.cookie != '':
        bigList: list = args.cookie.split(',')
        for i in range(0, int(len(bigList) / 2), 2):
            get_html.addCookie(bigList[i].split('.')[0], bigList[i].split('.')[1])

    with open(sitemap_file_path, 'r') as f:
        links = f.readlines()

        for link in links:
            full_link = url + '/' + link
            get_html.start(full_link)

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

