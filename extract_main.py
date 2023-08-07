#!/Users/mlautman/virtual_python_environment/bin/python3.9

from bs4 import BeautifulSoup
from scrapy.spiders import SitemapSpider
from scrapy.crawler import CrawlerProcess
import sys
import requests
import argparse
import validators
import urllib.parse
import os
import shutil
from pathlib import Path


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
parser.add_argument('-c','--crawl',action='store_const',const=False, default=False, help="Crawls the sitemaps to generate a list of URLs in the documentation set.")
parser.add_argument('-e','--extract',action='store_const',const=False, default=False, help="Extracts the <main> element from the raw HTML file into an XML file in the directory xml_extracts/.")
args = parser.parse_args()
print("Running with following options:")
print("* Crawl sitemaps: {}".format(args.crawl))
print("")

RESPONSE_CODE_BAD_MIN = 400
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


xml_extract_path = 'xml_extracts'

if args.extract == True:
	ignored_urls = ['https://www.brightspot.com/documentation/', 'https://www.brightspot.com/documentation/4-2-x-x', 'https://www.brightspot.com/documentation/4-5-x-x', 'https://www.brightspot.com/documentation/4-7-releases']

	headers= {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}


	
	if os.path.exists(xml_extract_path):
		shutil.rmtree(xml_extract_path, ignore_errors=True)
	os.mkdir(xml_extract_path)

	for my_url in url_list:
		if my_url in ignored_urls:
			continue
		if not (validators.url(my_url)):
			print("The following url is invalid, skipping: {0}".format(my_url))
			continue
		print("Processing URL {0}".format(my_url))
		response = requests.get(my_url)
		if response.status_code >= RESPONSE_CODE_BAD_MIN:
			print("The following URL gave a status code of {0}: {1}".format(response.status_code,my_url))
			continue

		parsed_url = urllib.parse.urlparse(my_url)
		my_url_path = parsed_url.path
		my_url_path = my_url_path[1:]
		my_url_path = my_url_path.replace('/','-')
		my_url_path = xml_extract_path + '/' + my_url_path
		
		temporary_xml = open(my_url_path +".xml", "w")
		try:
			soup = BeautifulSoup(response.text, 'html.parser')
			main = soup.find('main')
		except Exception as e:
			print("Exception occurred: {0} for URL {1}".format(type(e).__name__), my_url)
			sys.exit()
		main_str = str(main)
		main_str = main_str.replace('\x0a','')
		main_str = main_str.replace('<main','<main xmlns="http://www.w3.org/TR/html4/"')
		temporary_xml.write(main_str)
		temporary_xml.close()

for xml_input_file in os.listdir(xml_extract_path):
	print(xml_input_file)

sys.exit()


