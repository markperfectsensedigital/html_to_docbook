#!/Users/mlautman/virtual_python_environment/bin/python3.9

from bs4 import BeautifulSoup
from scrapy.spiders import SitemapSpider
from scrapy.crawler import CrawlerProcess
import sys


class MySpider(SitemapSpider):
	name = "bsp_sitemap"
	sitemap_urls = ['https://www.brightspot.com/documentation/sitemap.xml']
	sitemap_rules = [('/documentation/', 'parse_documentation')]
	sitemap_follow = ['/documentation/']


	def parse_documentation(self, response):
		if response.url not in url_list:
			url_list.append(response.url)

url_list = []

c = CrawlerProcess({
    'USER_AGENT': 'Mozilla/5.0',
	'REQUEST_FINGERPRINTER_IMPLEMENTATION': '2.7',
	'format': 'csv',
})
c.crawl(MySpider)
c.start()
url_list.sort()

url_file = open("urls.txt","w")
for myurl in url_list:
	url_file.write("{0}\n".format(myurl))
url_file.close()

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
