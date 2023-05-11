import argparse
import os
import get_html
from crawler import Crawler
from urllib.parse import urlparse

global links

# Parameter parsing
parser = argparse.ArgumentParser(description="K-Shield Jr. 10th Python Crawling Project")
parser.add_argument('-u', '--url', action='store', default='', help='분석을 원하는 사이트 주소를 입력해 주십시오.', required=True)
parser.add_argument('-e', '--exclude', action='store', default='', help='URL에서 제외할 단어 혹은 패턴을 입력해 주십시오.')
parser.add_argument('-b', '--browser', action='store', default='Edge', help='사용할 브라우저를 선택 합니다')

# Init var
args = parser.parse_args()
url = args.url.rstrip("/")
domain = urlparse(url).netloc

# Make dir with domain name
path = './' + domain
if not os.path.exists(path):
	os.makedirs('./' + domain, exist_ok=True)
	crawler = Crawler(url, exclude=args.exclude, no_verbose=True)
	print('Please Wait for scan what target site...\nStart for ' + url)
	links = crawler.start()

	# Write all url to text file
	with open('./' + domain + '/_sitemap_.txt', "w") as file:
		for link in links:
			file.write("{0}\n".format(link).lstrip('/'))

f = open(path + '/_sitemap_.txt', 'r')
links = f.readlines()

get_html.init(domain)
for link in links:
	get_html.start(url + '/' + link)
