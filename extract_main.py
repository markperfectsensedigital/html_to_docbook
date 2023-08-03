#!/Users/mlautman/virtual_python_environment/bin/python3.9

from bs4 import BeautifulSoup

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
