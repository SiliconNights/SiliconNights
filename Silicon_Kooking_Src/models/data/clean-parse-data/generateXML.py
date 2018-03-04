import xml.etree.ElementTree as ET
from bs4 import UnicodeDammit
from ftfy import fix_encoding, fix_text
import re

# --- String functions --- #

def cleanEncoding(line):
	line = fix_encoding(line)
	line = fix_text(line)
	line = UnicodeDammit(line).unicode_markup 
	return line

def getBetween(str, first, last):
	try:
		start = str.index(first) + len(first)
		end = str.index(last, start)
		return str[start:end]
	except ValueError:
		return ""

def removeBlankLines(text):
	text = re.sub(r'((\s)*\n(\s)*)+','\n', text)
	return text
	
def cleanPrint(text, file):
	text = text.strip()
	text = cleanEncoding(text)
	text = text.replace('&','&amp;')
	file.write(text)
	
	
# --- Helper functions --- #
	
def skipRecipe(filters, text):
	text = str.lower(text)
	for item in filters:
		if item in text:
			return True
	return False

def fileLinesToList(fileName):
	list = []
	with open(fileName) as file:
		for line in file:
			list.append(line.strip('\n').strip())
	return list
	
# Author: https://stackoverflow.com/users/2206251/greenstick
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    if iteration == total: 
        print()
	


# --- Main program --- #

# input files
cuisines = fileLinesToList('found-nationalities.txt')
types = fileLinesToList('meal-types.txt')
filters = fileLinesToList('filters.txt')

# write file
f = open('./recipe-data.xml', 'w', encoding='utf-8')

# data file
with open('datadump.xml', 'r', encoding='utf-8') as file:
	tree = ET.parse(file)

# get root element
wikimedia = tree.getroot()
iteration = 1
count = 1
string = ' '
total = len(wikimedia)

f.write('<?xml version="1.0" encoding="utf-8"?>')
f.write('\n<data>')

print('\n Generating data XML...')
# iterate page items
for page in wikimedia:
	# iterate elements of page
	printProgressBar (iteration, total, suffix = 'Recipe Data')
	iteration = iteration + 1
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
					if child.text != None and '== ingredients ==' in child.text.lower() and not skipRecipe(filters, child.text):
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
							info = removeBlankLines(info)


							# get ingredients
							string = getBetween(info,'== Ingredients ==', '== Directions ==')
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
								title = removeBlankLines(title)
								cleanPrint(title, f)
								f.write('</title>')

								# description
								string = getBetween(info, '== Description ==', '== Ingredients ==')
								f.write('\n<description>\n')
								string = string.replace('.', '')
								string = re.sub(r'^=\n', '', string)
								string = re.sub(r'(<)*', '', string)
								string = string.replace('[[' , '')
								string = string.replace(']]' , '')
								string = string.strip()
								if len(string) > 0 and string[len(string)-1] == '=':
									string = string[0:len(string)-1]
								if len(string) == 0:
									f.write('none')
								else:
									cleanPrint(string, f)
								f.write('\n</description>\n')


								# ingredients
								f.write('<ingredients>\n')
								string = ingredients 
								string = string.replace('[[' , '')
								string = re.sub(r'\|(.*?)\]\]' , '', string)
								string = string.replace(']]' , '')
								string = re.sub(r'\*\s*' , '', string)
								string = re.sub(r'#\s*' , '', string)
								while '\t' in string:
									string = string.replace('\t', ' ')
								while '  ' in string:
									string = string.replace('  ', ' ')
								cleanPrint(string, f)
								f.write('\n</ingredients>\n')


								# ingredient list
								f.write('<ingredientList>\n')
								string = ', '.join(map(str, list))
								cleanPrint(string, f)
								f.write('\n</ingredientList>\n')


								# instructions
								string = getBetween(info,'== Directions ==', '[[Category')
								f.write('<instructions>\n')
								string = re.sub(r'\=\= Source(.)* \=\=[\s\S]+__NOEDITSECTION__', '', string)
								string = string.replace('__NOEDITSECTION__', '')
								string = re.sub(r'\=\= Source(.)* \=\=[\s\S]+$', '', string)
								string = string.replace('== Source ==', '')
								string = re.sub(r'\=\= Other Links \=\=[\s\S]+$', '', string)
								string = re.sub(r'=== See Also ===', '', string)
								string = re.sub(r'(<)*', '', string)
								string = re.sub('\[http(.*?)\]','', string)
								string = string.replace('[[' , '')
								string = re.sub(r'\|(.*?)\]\]' , '', string)
								string = string.replace(']]' , '')
								string = re.sub(r'\*\s*' , '', string)
								string = re.sub(r'#\s*' , '', string)
								string = re.sub(r'\d+\. ', '', string)
								string = re.sub(r'\d+\) ', '', string)
								string = re.sub(r'\d+\.', '', string)
								string = re.sub(r'\d+\)', '', string)
								while '\t' in string:
									string = string.replace('\t', ' ')
								while '  ' in string:
									string = string.replace('  ', ' ')
								cleanPrint(string, f)
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
									cleanPrint(string, f)
								f.write('\n</tags>')

								# cuisine
								f.write('\n<cuisine>\n')
								found = []
								list = [item.lower() for item in list]
								if len(list) == 0:
									f.write('none')
								else:
									for cuisine in cuisines:
										for item in list:
											if re.search(cuisine, item) != None:
												if cuisine not in found:
													found.append(cuisine)
									if len(found) == 0:
										f.write('none')
									else:
										string = ', '.join(map(str, found))
										cleanPrint(string, f)
								f.write('\n</cuisine>')

								# meal-type
								f.write('\n<mealType>\n')
								found = []
								list = [item.lower() for item in list]
								if len(list) == 0:
									f.write('none')
								else:
									for type in types:
										for item in list:
											if re.search(type, item) != None:
												if type not in found:
													found.append(type)
									if len(found) == 0:
										f.write('none')
									else:
										string = ', '.join(map(str, found))
										cleanPrint(string, f)
								f.write('\n</mealType>')

								f.write('\n</recipe>')
								f.write('\n')
								count = count + 1
f.write('\n</data>')
f.close()
print('\n Total recipes added:', count)