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
							info = info.replace('== Other Links ==', '')
							info = info.replace('== See also ==', '')
							info = re.sub(r'{[\s\S]+align[\s\S]+}', '', info)
							info = re.sub('\{\|[\S\s]+\}', '', info)
							info = re.sub(r'==(.*?)Video(.)*(.*?)==', '', info)
							info = re.sub(r'<(.*?)p(.*?)>', '', info)
							info = re.sub(r'<(.*?)i(.*?)>', '', info)
							info = re.sub(r'<(.*?)gallery(.*?)>', '', info)
							info = re.sub(r'<(.*?)s(.*?)>', '', info)
							info = re.sub(r'<(.*?)b(.*?)>', '', info)
							info = re.sub(r'<(.*?)tr(.*?)>', '', info)
							info = re.sub(r'<(.*?)td(.*?)>', '', info)
							info = re.sub(r'<(.*?)table(.*?)>', '', info)
							info = re.sub(r'<(.*?)u(.*?)>', '', info)
							info = re.sub(r'<(.*?)ref(.*?)>', '', info)
							info = re.sub(r'<(.*?)br(.*?)>', '', info)
							info = re.sub(r'<(.*?)span(.*?)>', '', info)
							info = re.sub(r'<(.*?)nowiki(.*?)>', '', info)
							info = re.sub(r'\-\=>(.*?)<\=\-', '', info)
							info = re.sub(r'<(.*?)small(.*?)>', '', info)
							info = re.sub(r'<(.*?)@gmail(.*?)>', '', info)
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
							string = re.sub(r'#(.*?)\|','|', string)
							string = re.sub(r'special\:(.*?),', '', string)
							string = re.sub(r"'''(.*?)'''", '', string)
							string = re.sub(r'\[\[\|', '[[', string)
							string = re.sub(r'\|\|', '|', string)
							string = re.sub('(.)ikipedia:', '', string)
							string = string.replace('w:c:bakingrecipes:', '')
							string = string.replace('"', '')
							ingredients = string
							
							# get list of ingredients
							list = re.findall(r'\[\[(.*?)\]\]', string)
							list = [item.lower() for item in list]
							newlist = []
							for i in list:
								if i not in newlist:
									i = clean_encoding(i)
									i = i.unicode_markup
									i = i.strip()
									i = re.sub(r'^\|', '', i)
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
								string = re.sub(r'\n\s*\n', '\n', string)
								title = title.strip()
								title = clean_encoding(title)
								title = title.unicode_markup
								title = title.replace('&','&amp;')
								f.write(title)
								f.write('</title>')
								
								# description
								string = get_between(info, '== Description ==', '== Ingredients ==')
								f.write('\n<description>\n')
								string = string.replace('.', '')
								string = re.sub(r'^=\n', '', string)
								string = re.sub(r'(<)*', '', string)
								string = string.strip()
								if len(string) > 0 and string[len(string)-1] == '=':
									string = string[0:len(string)-1]
								string = re.sub(r'(\n)+$', '', string)
								string = re.sub(r'^(\n)+', '', string)
								string = re.sub(r'\n\s*\n', '\n', string)
								if len(string) == 0:
									f.write('none')
								else:
									string = clean_encoding(string)
									string = string.unicode_markup 
									string = string.replace('&','&amp;')
									f.write(string)
								f.write('\n</description>\n')
													
													
								# ingredients 
								f.write('<ingredients>\n')
								ingredients = clean_encoding(ingredients)
								ingredients = ingredients.unicode_markup
								ingredients = ingredients.replace('&','&amp;')
								f.write(ingredients)
								f.write('\n</ingredients>\n')
								
								
								# ingredient list
								f.write('<ingredientList>\n')
								string = ', '.join(map(str, list))
								string = clean_encoding(string)
								string = string.unicode_markup 
								string = string.replace('&','&amp;')
								f.write(string)
								f.write('\n</ingredientList>\n')
									
									
								# instructions
								string = get_between(info,'== Directions ==', '[[Category')
								f.write('<instructions>\n')
								string = re.sub(r'\=\= Source(.)* \=\=[\s\S]+__NOEDITSECTION__', '', string)
								string = string.replace('__NOEDITSECTION__', '')
								string = re.sub(r'\=\= Source(.)* \=\=[\s\S]+$', '', string)
								string = string.replace('== Source ==', '')
								string = re.sub(r'\=\= Other Links \=\=[\s\S]+$', '', string)
								string = re.sub(r'=== See Also ===', '', string)
								string = re.sub(r'(\n)+$', '', string)
								string = re.sub(r'(<)*', '', string)
								string = re.sub(r'^(\n)+', '', string)
								string = re.sub(r'(\n)+','\n', string)
								string = re.sub(r'\s*\n\s*\n', '\n', string)
								string = string.strip()
								string = clean_encoding(string)
								string = string.unicode_markup 
								string = string.replace('&','&amp;')
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
									string = ', '.join(map(str, list))
									string = clean_encoding(string)
									string = string.unicode_markup
									string = string.replace('&','&amp;')
									f.write(string)
								f.write('\n</tags>')
								f.write('\n</recipe>')
								f.write('\n')
								count = count + 1
f.write('\n</data>')
f.close()
print(count)