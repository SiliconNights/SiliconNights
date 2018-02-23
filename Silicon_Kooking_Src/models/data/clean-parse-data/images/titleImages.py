import xml.etree.ElementTree as ET
from bs4 import UnicodeDammit
from ftfy import fix_encoding, fix_text
import re

# get text in between first and last 
def get_between(str, first, last):
	try:
		start = str.index(first) + len(first)
		end = str.index(last, start)
		return str[start:end]
	except ValueError:
		return ""

# clean encoding
def clean_encoding(line):
	line = fix_encoding(line)
	line = fix_text(line)
	line = UnicodeDammit(line)
	return line

# open file to write
f = open('./title-images.xml', 'w', encoding='utf-8')
		
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
							info = info.replace('== Other Links ==', '')
							info = info.replace('== See also ==', '')
							info = re.sub(r'{[\s\S]+align[\s\S]+}', '', info)
							info = re.sub('\{\|[\S\s]+\}', '', info)
							info = re.sub(r'==(.*?)Video(.)*(.*?)==', '', info)
							info = re.sub(r'<(.*?)p(.*?)>', '', info)
							info = re.sub(r'<(.*?)u(.*?)>', '', info)
							info = re.sub(r'<(.*?)ref(.*?)>', '', info)
							info = re.sub(r'<(.*?)br(.*?)>', '', info)
							info = re.sub(r'<(.*?)span(.*?)>', '', info)
							info = re.sub(r'<(.*?)nowiki(.*?)>', '', info)
							info = re.sub(r'<(.*?)small(.*?)>', '', info)
							info = re.sub(r'<(.*?)References(.*?)>', '', info)
							info = re.sub(r'{{DEFAULTSORT:(.*?)}}', '', info)
							info = info.replace('{{wikifiedrecipe}}', '')
							info = re.sub(r'<(.*?)youtube(.*?)>(.*?)<(.*?)youtube(.*?)>', '', info)
							info = re.sub(r'<(.*?)youtube(.*?)>', '', info)
							info = info.replace('&','&amp;')				
							info = re.sub(r'(\n)+$', '', info)
							info = re.sub(r'^(\n)+', '', info)
							info = re.sub(r'(\n)+','\n', info)
							
							# get ingredients
							string = get_between(info,'== Ingredients ==', '== Directions ==')
							string = re.sub(r'(\n)+$', '', string)
							string = re.sub(r'^(\n)+', '', string)
							string = re.sub(r'^=\n', '', string)
							if len(string) > 0 and string[len(string)-1] == '=':
								string = string[0:len(string)-1]
							string = string.replace('[{','[[')
							string = re.sub('\[\[\:Category\:(.*?)\]\]', '', string)
							string = re.sub('\[\[Category(.*?)\]\]', '', string)
							string = re.sub('\[http(.*?)\]','', string)
							ingredients = string
							
							# get list of ingredients
							list = re.findall(r'\[\[(.*?)\]\]', string)
							list = [item.lower() for item in list]
							newlist = []
							for i in list:
								if i not in newlist:
									i = clean_encoding(i)
									newlist.append(i.unicode_markup)
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
								string = re.sub(r'\n\s*\n', '\n', string)
								title = title.strip()
								title = clean_encoding(title)
								title = title.unicode_markup
								title = title.replace('&','&amp;')
								f.write(title)
								f.write('</title>')	
								
								# image
								f.write('\n<image>\n')
								f.write('</image>')
								
								# images
								f.write('\n<images>\n')
								f.write('</images>')				

								f.write('\n</recipe>')
								f.write('\n')
								count = count + 1
f.write('\n</data>')
f.close()
print(count)