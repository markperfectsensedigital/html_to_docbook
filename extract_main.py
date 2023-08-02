#!/Users/mlautman/virtual_python_environment/bin/python3.9

from bs4 import BeautifulSoup

temporary_html = open("temporary.html", "w")

with open("gs.html") as fp:
	soup = BeautifulSoup(fp, 'html.parser')
	main = soup.find('main')
	main_str = str(main)
	main_str = main_str.replace('\x0a','')
	temporary_html.write(main_str)

fp.close()
temporary_html.close()
