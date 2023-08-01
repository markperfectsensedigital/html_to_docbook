#!/Users/mlautman/virtual_python_environment/bin/python3.9
# Validate against the xsd by running
#
# xmllint --schema docbook.xsd --noout sample.xml
# xmllint --schema docbook.xsd --noout ugly.xml
# xmllint --format --output dockbook.xml ugly.xml
from bs4 import BeautifulSoup
import sys

def spacer(num_tabs):
  return "\t" * num_tabs

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
#	print(body_paragraphs)
	for paragraph in body_paragraphs:
		xml_file.write('<para>{0}</para>\n'.format(paragraph.get_text().strip()))
#		print(paragraph)
		inside = paragraph.find_all()
#		print("inside")
#		print(inside)
#		print("outside")
#		rst.write('{0}\n\n'.format(paragraph.get_text()))
#	for sibling in body_element.find_next_siblings():
#		if sibling.name == 'p':
#			rst.write('{0}\n\n'.format(sibling.get_text()))
#		if sibling.name == 'ul':
#			line_item = sibling.find('li')
#			rst.write('{0}\n\n'.format(line_item.get_text()))
#			for sibling_line_item in line_item.find_next_siblings():
#				rst.write('* {0}\n\n'.format(sibling_line_item.get_text()))
		

	xml_file.write('</section>\n')
#fp.close()
xml_file.write('</chapter>\n')
xml_file.write('</book>')
xml_file.close()
