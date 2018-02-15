import xml.etree.ElementTree as ET
import re

# finds text in between a first and last substring
def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

# open file to write
f = open('./database.xml', 'wb')
		
# create element tree object
tree = ET.parse('cookbook.xml')
 
# get root element
wikimedia = tree.getroot()

f.write('<? xml version="1.0" encoding="UTF-8"?>'.encode('utf-8'))
f.write('\n<data>'.encode('utf-8'))
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
				# find text tag
				if child.tag == 'text':
					# check if contains recipe
					if child.text != None and '== ingredients ==' in child.text.lower():
							image = find_between(child.text, '== Description ==', '== Ingredients ==')
							if None != re.search(r'\[\[Image:(.*)\]\]', image): 
								# create new recipe
								f.write('\n<recipe>'.encode('utf-8'))
								
								# title
								f.write('\n<title> '.encode('utf-8'))
								string = string.lstrip()
								string = string.rstrip()
								string = string.replace('\n\n','\n')
								f.write(string.encode('utf-8'))
								f.write('<\\title>'.encode('utf-8'))
									
								
								# description
								string = find_between(child.text, '== Description ==', '== Ingredients ==')
								f.write('\n<description>\n'.encode('utf-8'))
								image = re.search(r'\[\[Image:(.*)\]\]', string)
								string = re.sub(r'\[\[Image:(.*)\]\]', '', string)
								string = string.lstrip()
								string = string.rstrip()
								string = string.replace('\n\n','\n')
								string = string.replace('=', '')
								string = string.lstrip()
								string = string.rstrip()
								f.write(string.encode('utf-8'))
								f.write('\n<\description>'.encode('utf-8'))
								
								# image 
								f.write('\n<image>'.encode('utf-8'))
								f.write(image.group().encode('utf-8'))
								f.write('<\image>'.encode('utf-8'))
								
									
								# ingredients 
								string = find_between(child.text,'== Ingredients ==', '== Directions ==')
								f.write('\n<ingredients>\n'.encode('utf-8'))
								string = string.replace('=', '')
								string = string.lstrip()
								string = string.rstrip()
								string = string.replace('\n\n','\n')
								f.write(string.encode('utf-8'))
								f.write('\n<\ingredients>'.encode('utf-8'))
									
								# directions
								string = find_between(child.text,'== Directions ==', '[[Category')
								f.write('\n<directions>\n'.encode('utf-8'))
								string = string.lstrip()
								string = string.rstrip()
								string = string.replace('\n\n','\n')
								string = string.replace('=== Other Links ===\n', '')
								string = string.replace('== See also ==', '')
								string = string.replace('__NOTOC__', '')
								string = string.replace('=', '')
								f.write(string.encode('utf-8'))
								f.write('\n<\directions>'.encode('utf-8'))
									
								f.write('\n<\\recipe>'.encode('utf-8'))
								f.write('\n'.encode('utf-8'))
f.write('\n<\data>'.encode('utf-8'))
f.close()