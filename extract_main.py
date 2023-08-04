#!/Users/mlautman/virtual_python_environment/bin/python3.9

from bs4 import BeautifulSoup
from scrapy.spiders import SitemapSpider
from scrapy.crawler import CrawlerProcess
import sys
import requests
import argparse



class MySpider(SitemapSpider):
	name = "bsp_sitemap"
	sitemap_urls = ['https://www.brightspot.com/documentation/sitemap.xml']
	sitemap_rules = [('/documentation/', 'parse_documentation')]
	sitemap_follow = ['/documentation/']


	def parse_documentation(self, response):
		if response.url not in url_list:
			url_list.append(response.url)


parser = argparse.ArgumentParser(
                    prog='Documentation Retriever',
                    description='Retrieves all HTML files in Brightspot\'s documentation sitemaps.',
                    )
parser.add_argument('-c','--crawl',action='store_const',const=False, default=False)
args = parser.parse_args()
print("Running with following options:")
print("* Crawl sitemaps: {}".format(args.crawl))
print("")
url_list = []
url_filename = 'urls.txt'

if args.crawl == True:
	print("Crawling sitemaps...")
	c = CrawlerProcess({
	    'USER_AGENT': 'Mozilla/5.0',
		'REQUEST_FINGERPRINTER_IMPLEMENTATION': '2.7',
		'format': 'csv',
	})
	c.crawl(MySpider)
	c.start()
	url_list.sort()

	# Save the URLS in a temporary file.
	url_file = open(url_filename,"w")
	for myurl in url_list:
		url_file.write("{0}\n".format(myurl))
	url_file.close()
else:
	print("Reading URLs from previously crawled sitemaps...")
	url_file = None
	try:
		url_file = open(url_filename,"r")
		data = url_file.read()
		url_list = data.split("\n")
		url_file.close()
	except FileNotFoundError as e:
		print("Exception occurred while reading the file {0}; {1}".format(url_filename,type(e).__name__))
		sys.exit()

	except Exception as e:
		print("Exception occurred: {0}".format(type(e).__name__))
		sys.exit()

ignored_urls = ['https://www.brightspot.com/documentation/', 'https://www.brightspot.com/documentation/4-2-x-x', 'https://www.brightspot.com/documentation/4-5-x-x', 'https://www.brightspot.com/documentation/4-7-releases']

headers= {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}

for my_url in url_list:
	r = requests.get(myurl)
	print(r.text)
	sys.exit()


sys.exit()


temporary_xml = open("temporary.xml", "w")
with open("gs.html") as fp:
	soup = BeautifulSoup(fp, 'html.parser')
	main = soup.find('main')
	main_str = str(main)
	main_str = main_str.replace('\x0a','')
	main_str = main_str.replace('<main','<main xmlns="http://www.w3.org/TR/html4/"')
	temporary_xml.write(main_str)

fp.close()
temporary_xml.close()
