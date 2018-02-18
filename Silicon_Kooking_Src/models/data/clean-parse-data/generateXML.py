import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import re

# inserts text in between first and last 
def get_between(str, first, last):
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
count = 1
string = ' '

f.write('<?xml version="1.0" encoding="utf-8"?>')
f.write('\n<data>')

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
				# get text tag
				if child.tag == 'text':
					# check if contains recipe
					if child.text != None and '== ingredients ==' in child.text.lower():
							# remove/fix misc. tags/data
							info = child.text
							info = re.sub(r'\[\[Image:(.*?)\]\]', '', info)
							info = re.sub(r'\[\[File:(.*?)\]\]', '', info)
							info = re.sub(r'\(\[\[Wikipedia:(.*?)\]\]\)', '', info)
							info = info.replace('__NOTOC__', '')
							info = info.replace('=== Other Links ===', '')
							info = info.replace('== See also ==', '')												
							info = re.sub(r'<(.*?)ref(.*?)>', '', info)
							info = re.sub(r'<(.*?)br(.*?)>', '', info)
							info = re.sub(r'<(.*?)span(.*?)>', '', info)
							info = info.replace('&','&amp;')
							info = re.sub(r'(\n)+','\n', info)
							info = re.sub(r'^\=\n', '\n', info)
							
							# get ingredients
							string = get_between(info,'== Ingredients ==', '== Directions ==')
							string = re.sub(r'(\n)+$', '', string)
							string = re.sub(r'^(\n)+', '', string)
							ingredients = string
							
							# get list of ingredients
							list = re.findall(r'\[\[(.*?)\]\]', string)
							list = [item.lower() for item in list]
							newlist = []
							for i in list:
								if i not in newlist:
									newlist.append(i)
							newlist.reverse()
							list = newlist
							
							if len(list) > 0 :
								# create new recipe
								tag = '\n<recipe number="' + str(count) + '">'
								f.write(tag)
								
								# title
								f.write('\n<title>')
								title = re.sub(r'(\n)+$', '', title)
								title = re.sub(r'^(\n)+', '', title)
								title = re.sub(r'(\n)+','\n', title)
								title = title.strip()
								f.write(title)
								f.write('</title>')
								
								# description
								string = get_between(info, '== Description ==', '== Ingredients ==')
								f.write('\n<description>\n')
								string = string.replace('.', '')
								string = re.sub(r'^= ', '', string)
								string = re.sub(r'(\n)+$', '', string)
								string = re.sub(r'^(\n)+', '', string)
								string = string.strip()
								if len(string) == 0:
									f.write('none')
								else:
									f.write(string)
								f.write('\n</description>\n')
													
													
								# ingredients 
								f.write('<ingredients>\n')
								f.write(ingredients)
								f.write('\n</ingredients>\n')
								
								
								# ingredient list
								f.write('<ingredientList>\n')
								for i in range(0, len(list)-1):
									f.write(list[i])
									f.write(', ')
								f.write(list[len(list)-1])
								f.write('\n</ingredientList>\n')
									
									
								# instructions
								string = get_between(info,'== Directions ==', '[[Category')
								f.write('<instructions>\n')
								string = re.sub(r'(\n)+$', '', string)
								string = re.sub(r'^(\n)+', '', string)
								string = re.sub(r'(\n)+','\n', string)
								string = string.strip()
								f.write(string)
								f.write('\n</instructions>\n')
								
								
								# tags
								f.write('<tags>\n')
								list = re.findall(r'\[\[Category:(.*?)\]\]', info)
								newlist = []
								for item in list:
									item = item.replace('Recipes', '')
									item = item.strip()
									item = item.lstrip('using ')
									if item != 'that need photos' and item != 'with video instruction':
										newlist.append(item)
								list = newlist
								newlist = []
								for i in list:
									if i not in newlist:
										newlist.append(i)
								newlist.reverse()
								list = newlist
								if len(list) == 0: 
									f.write('none')
								else:
									for i in range(0, len(list)-1):
										f.write(list[i])
										f.write(', ')
									f.write(list[len(list)-1])
								f.write('\n</tags>')
								f.write('\n</recipe>')
								f.write('\n')
								count = count + 1
f.write('\n</data>')
f.close()
print(count)