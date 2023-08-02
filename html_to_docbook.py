#!/Users/mlautman/virtual_python_environment/bin/python3.9
# Validate against the xsd by running
#
# xmllint --schema docbook.xsd --noout sample.xml
# xmllint --schema docbook.xsd --noout ugly.xml
# xmllint --format --output dockbook.xml ugly.xml
from bs4 import BeautifulSoup
import sys
import re

def spacer(num_tabs):
  return "\t" * num_tabs

#regular expressions
re_paragraph_html = r'(<[/]?)p>'
re_paragraph_db = r'\1para>'

re_bold_html = r'<b>(.*?)</b>'
re_bold_docbook = r'<emphasis role="bold">\1</emphasis>'

re_term_html = r'<span class="Term">(.*?)</span>'
re_term_docbook = r'\1'

re_newline_html = r'<br[/]?>'
re_newline_docbook = r''

xml_file = open("ugly.xml", "w")
xml_file.write("<?xml version='1.0'?>\n")
xml_file.write('<book xmlns="http://docbook.org/ns/docbook">\n')
xml_file.write('<title>{0}</title>\n'.format('Brightspot Documentation Set'))
xml_file.write('<chapter>\n')
xml_file.write('<title>{0}</title>\n'.format('Editorial Guide'))


with open("gs.html") as fp:
	soup = BeautifulSoup(fp, 'html.parser')
	xml_file.write('<section>\n')
	title = soup.find('h1', class_='CreativeWorkPage-headline').string.strip()
	xml_file.write('<title>{0}</title>\n'.format(title))


	body_paragraphs = soup.find('main').find_all('p')
	for paragraph in body_paragraphs:
		local_paragraph = str(paragraph).strip()
		#print(local_paragraph)
		db_version = re.sub(re_paragraph_html,re_paragraph_db,local_paragraph)
		db_version = re.sub(re_bold_html,re_bold_docbook,db_version)
		db_version = re.sub(re_term_html,re_term_docbook,db_version)
		db_version = re.sub(re_newline_html,re_newline_docbook,db_version)
		db_version = db_version.replace('\x0a','')
		print(db_version)
		xml_file.write(db_version)

	xml_file.write('</section>\n')
fp.close()

with open("loggin_in_to_brightspot.html") as fp:
	soup = BeautifulSoup(fp, 'html.parser')
	xml_file.write('<section>\n')
	title = soup.find('h1', class_='CreativeWorkPage-headline').string.strip()
	xml_file.write('<title>{0}</title>\n'.format(title))

	body_paragraphs = soup.find('main').find_all('p')
	for paragraph in body_paragraphs:
		local_paragraph = str(paragraph).strip()
		#print(local_paragraph)
		db_version = re.sub(re_paragraph_html,re_paragraph_db,local_paragraph)
		db_version = re.sub(re_bold_html,re_bold_docbook,db_version)
		db_version = re.sub(re_term_html,re_term_docbook,db_version)
		db_version = re.sub(re_newline_html,re_newline_docbook,db_version)
		db_version = db_version.replace('\x0a','')
		print(db_version)
		xml_file.write(db_version)

	xml_file.write('</section>\n')
fp.close()

xml_file.write('</chapter>\n')
xml_file.write('</book>')
xml_file.close()
