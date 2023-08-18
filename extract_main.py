#!/Users/mlautman/virtual_python_environment/bin/python3.9

from bs4 import BeautifulSoup
from scrapy.spiders import SitemapSpider
from scrapy.crawler import CrawlerProcess
import sys
import requests
import argparse
import validators
import os
import shutil
from pathlib import Path
from urllib.parse import urlparse
from urllib.parse import parse_qs
#from dict2xml import dict2xml


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
parser.add_argument('-c','--crawl',action=argparse.BooleanOptionalAction, default=False, help="Crawls the sitemaps to generate a list of URLs in the documentation set.")
parser.add_argument('-d','--download', action=argparse.BooleanOptionalAction, default=False, help="Downloads the HTML files listed in the crawled sitemaps, and places them in the directory html_downloads/.")
parser.add_argument('-e','--extract',action=argparse.BooleanOptionalAction, default=False, help="Extracts the <main> element from the raw HTML file into an XML file in the directory xml_extracts/.")
parser.add_argument('-i','--images',action=argparse.BooleanOptionalAction, default=False, help="Downloads images in the HTML files into the folder images/.")
args = parser.parse_args()
print("Running with following options:")
print("* Crawl sitemaps: {}".format(args.crawl))
print("* Download HTML files: {}".format(args.download))
print("* Download images from HTML files: {}".format(args.images))
print("* Extract XML from HTML files: {}".format(args.extract))
print("")

RESPONSE_CODE_BAD_MIN = 400
url_list = []
url_filename = 'urls.txt'
caption_dict = {}

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

print("Assembled list of URLs")

xml_extract_path = 'xml_extracts'
html_download_path = 'html_downloads'
docbook_path = 'docbook_files'
image_path = 'images'

if args.download == True:
	print("Downloading HTML files from crawled sitemaps.")
	if os.path.exists(html_download_path):
		shutil.rmtree(html_download_path, ignore_errors=True)
	os.mkdir(html_download_path)

	ignored_urls = ['https://www.brightspot.com/documentation/', 'https://www.brightspot.com/documentation/4-2-x-x', 'https://www.brightspot.com/documentation/4-5-x-x', 'https://www.brightspot.com/documentation/4-7-releases']

	headers= {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}

	for my_url in url_list:
		if my_url in ignored_urls:
			continue
		if not (validators.url(my_url)):
			print("The following url is invalid, skipping: {0}".format(my_url))
			continue
		print("Downloading URL {0}".format(my_url))
		response = requests.get(my_url)
		if response.status_code >= RESPONSE_CODE_BAD_MIN:
			print("The following URL gave a status code of {0}: {1}".format(response.status_code,my_url))
			continue

		# Create a friendly path for the written file.
		parsed_url = urlparse(my_url)
		my_url_path = parsed_url.path
		my_url_path = my_url_path[1:] # Drop first character which is a leading slash
		my_url_path = my_url_path.replace('/','-')
		my_url_path = html_download_path + '/' + my_url_path
		
		temporary_html = open(my_url_path +".html", "w")
		temporary_html.write(response.text)
		temporary_html.close()

if args.images == True:
	print("Downloding images referenced in HTML files...")

	if not os.path.exists(html_download_path):
		print("The path {0} does not exist. Rerun this command with the --download option.")
		sys.exit()
	
	if os.path.exists(image_path):
		shutil.rmtree(image_path, ignore_errors=True)
	os.mkdir(image_path)

	raw_html_files = os.listdir(html_download_path)
	for my_raw_file in raw_html_files:
		print("Downloading images from file {0}".format(my_raw_file))
		parent_file = open(html_download_path + '/' + my_raw_file,'r')
		soup = BeautifulSoup(parent_file,'html.parser')
		figures = soup.find_all('figure')
		if not figures:
			continue
		for my_figure in figures:
			my_image = my_figure.find('img')
			if not my_image:
				print("Detected a figure with no <img> tag, skipping...")
				continue
			my_src = my_image['src']
			if not my_src:
				print("Detected an image with no <src> tag, skipping...")
				sys.exit()
			my_parse = urlparse(my_src)
			my_query = my_parse.query
			print("query string: " + my_query)
			if my_query:
				my_params = parse_qs(my_query)
				image_url = my_params['url'][0]
			else:
				image_url = my_src
			image_url_parse = urlparse(image_url)
			image_filename = image_url_parse.path
			file_path = image_filename[1:].replace('/','_')
			file_path = file_path.replace(' ','_')
			if my_image['alt']:
				caption_dict[file_path] = my_image['alt']
			else:
				caption_dict[file_path] = None
			response = requests.get(image_url)
			image_file = open(image_path + '/' + file_path,'wb')
			image_file.write(response.content)
			image_file.close()
		parent_file.close()
	caption_file = open('caption-file.xml','w')
	caption_file.write('<?xml version="1.0" encoding="UTF-8" ?>\n<images>\n')
	for x, y in caption_dict.items():
		caption_file.write("\t<image>\n\t\t<filename>{0}</filename>\n\t\t<caption>{1}</caption>\n\t</image>\n".format(x,y))
	caption_file.write('</images>')	
	caption_file.close()

if args.extract == True:
	print("Extracting XML from downloaded HTML files...")
	if not os.path.exists(html_download_path):
		print("The path {0} does not exist. Rerun this command with the --download option.")
		sys.exit()

	if os.path.exists(xml_extract_path):
		shutil.rmtree(xml_extract_path, ignore_errors=True)
	os.mkdir(xml_extract_path)

	raw_html_files = os.listdir(html_download_path)
		
	for my_raw_file in raw_html_files:
		print("Extracting <main> element from file {0}".format(my_raw_file))
		temporary_html = None

		try:
			temporary_html_file = open(html_download_path + '/' + my_raw_file,"r")
			temporary_html = temporary_html_file.read()
			temporary_html_file.close()
		except  Exception as e:
			print("Exception occurred: {0} for URI {1}, skipping".format(type(e).__name__, my_raw_file))
			continue
		temporary_xml_filename = xml_extract_path + '/' + my_raw_file
		temporary_xml_filename = temporary_xml_filename.replace(".html",".xml")
		temporary_xml = open(temporary_xml_filename, "w")
		try:
			soup = BeautifulSoup(temporary_html, 'html.parser')
			main = soup.find('main')
			scripts = main.find_all('script')
			for script in scripts:
				script.decompose()
				print("Destoryed a script")
			meta = soup.find('meta',{'name': 'brightspot.contentId'})
			id = meta['content']
		except Exception as e:
			print("Exception occurred: {0} for URI {1}".format(type(e).__name__), my_raw_file)
			sys.exit()
		main_str = str(main)
		main_str = main_str.replace('\x0a','')
		main_str = main_str.replace('<main','<?xml version="1.0"?>\n<main xmlns="http://www.w3.org/TR/html4/" id="{0}"'.format(id))
		temporary_xml.write(main_str)
		temporary_xml.close()


if os.path.exists(docbook_path):
	shutil.rmtree(docbook_path, ignore_errors=True)
os.mkdir(docbook_path)

print("Converting extracted XML to docbook...")
for xml_input_file in os.listdir(xml_extract_path):
	print("Transforming file xml_extracts/{0}".format(xml_input_file))
	
	source_file = "xml_extracts/" + xml_input_file

	saxon_command = "saxon -s:{0} -xsl:clean_xml_extract.xsl -o:{1}/{2}".format(source_file,docbook_path, xml_input_file)
	print(saxon_command)
	status = os.system(saxon_command)
	if status != 0:
		sys.exit()
	xmllint_command = "xmllint --schema docbook.xsd --noout {0}/{1}".format(docbook_path, xml_input_file)
	print(xmllint_command)
	status = os.system(xmllint_command)
	if status != 0:
		sys.exit()


