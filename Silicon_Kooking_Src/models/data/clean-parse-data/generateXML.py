import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import re

# inserts text in between first and last 
def insert_between(str, first, last):
	try:
		start = str.index(first) + len(first)
		end = str.index(last, start)
		return str[start:end]
	except ValueError:
		return ""

# open file to write
f = open('./recipe-data.xml', 'w', encoding='utf-8')
		
# create element tree object
with open('datadump.xml', 'r', encoding='utf-8') as file:
	tree = ET.parse(file)
 
# get root element
wikimedia = tree.getroot()

f.write('<?xml version="1.0" ?>')
f.write('\n<data>')
string = ' '
# iterate page items
for page in wikimedia:
	# iterate elements of page
	for element in page:
		# if title, store title
		if element.tag == 'title':
			string = element.text
		# if revision
		if element.tag == 'revision':
			for child in element:
				# insert text tag
				if child.tag == 'text':
					# check if contains recipe
					if child.text != None and '== ingredients ==' in child.text.lower():
							image = insert_between(child.text, '== Description ==', '== Ingredients ==')
							if None != re.search(r'\[\[Image:(.*)\]\]', image): 
								info = child.text
								info = re.sub(r'<(.*)ref(.*)>', '', info)
								info = re.sub(r'<(.*)br(.*)>', '', info)
								info = info.replace('&','&amp;')
								
								# create new recipe
								f.write('\n<recipe>')
								
								# title
								f.write('\n<title> ')
								string = string.lstrip()
								string = string.rstrip()
								string = string.replace('\n\n','\n')
								f.write(string)
								f.write('</title>')
									
								
								# description
								string = insert_between(info, '== Description ==', '== Ingredients ==')
								f.write('\n<description>\n')
								image = re.search(r'\[\[Image:(.*)\]\]', string)
								string = re.sub(r'\[\[Image:(.*)\]\]', '', string)
								string = string.lstrip()
								string = string.rstrip()
								string = string.replace('\n\n','\n')
								string = string.replace('=', '')
								string = string.lstrip()
								string = string.rstrip()
								f.write(string)
								f.write('\n</description>')
								
								# image 
								f.write('\n<image>')
								f.write(image.group())
								f.write('</image>')
								
									
								# ingredients 
								string = insert_between(info,'== Ingredients ==', '== Directions ==')
								f.write('\n<ingredients>\n')
								string = string.replace('=', '')
								string = string.lstrip()
								string = string.rstrip()
								string = string.replace('\n\n','\n')
								f.write(string)
								f.write('\n</ingredients>')
									
								# directions
								string = insert_between(info,'== Directions ==', '[[Category')
								f.write('\n<directions>\n')
								string = string.lstrip()
								string = string.rstrip()
								string = string.replace('\n\n','\n')
								string = string.replace('== Other Links ==', '')
								string = string.replace('== See also ==', '')
								string = string.replace('__NOTOC__', '')
								string = string.replace('=', '')
								f.write(string)
								f.write('\n</directions>')
									
								f.write('\n</recipe>')
								f.write('\n')
f.write('\n</data>')
f.close()