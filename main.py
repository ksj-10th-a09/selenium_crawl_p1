import argparse
import os
from crawler import Crawler
from urllib.parse import urlparse

# Parameter parsing
parser = argparse.ArgumentParser(description="K-Shield Jr. 10th Python Crawling Project")
parser.add_argument('--url', action='store', default='', help='분석을 원하는 사이트 주소를 입력해 주십시오.')
parser.add_argument('--exclude', action='store', default='', help='URL에서 제외할 단어 혹은 패턴을 입력해 주십시오.')

# Init var
args = parser.parse_args()
url = args.url.rstrip("/")
domain = urlparse(url).netloc

# Make dir with domain name
os.makedirs('./' + domain, exist_ok=True)

crawler = Crawler(url, exclude=args.exclude, no_verbose=False)
links = crawler.start()

# Write all url to text file
with open('./' + domain + '/sitemap.txt', "w") as file:
	for link in links:
		file.write("{0}{1}\n".format(url, link))