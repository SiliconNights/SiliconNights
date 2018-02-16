import xml.etree.ElementTree as ET

# create element tree object
tree = ET.parse('cleandata.xml')
 
# get root element
wikimedia = tree.getroot()

# iterate page items
for page in wikimedia:
	# iterate elements of page
	for element in page:
		# if title, store title
		if element.tag == 'title':
			print(element.text)
		# if revision
		if element.tag == 'revision':
			for child in element:
				# find text tag
				if child.tag == 'text':
					print(child.text)
print('\n')