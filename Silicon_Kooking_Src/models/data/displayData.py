import xml.etree.ElementTree as ET
import re

# create element tree object
tree = ET.parse('cookbook.xml')
 
# get root element
wikimedia = tree.getroot()

title = ' '
# iterate page items
for page in wikimedia:
	# iterate elements of page
	for element in page:
		# if title, store title
		if element.tag == 'title':
			title = element.text
		# if revision
		if element.tag == 'revision':
			for child in element:
				# find text tag
				if child.tag == 'text':
					print(child.text)
	print('\n')