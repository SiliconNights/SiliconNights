import xml.etree.ElementTree as ET
import re, json, urllib.request, urllib.error, pytz
from time import sleep

# http header
# NOTE: Make sure to set your specific User-Agent or remove the field.
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

# get image url
def getImageURL(name):
	name = re.sub(' ', '_', name)
	print(name)
	url = "https://api.qwant.com/api/search/images?count=10&offset=0&q=" + name
	req = urllib.request.Request(url, None, headers={'User-Agent':' Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0'})
	qwantResponse = urllib.request.urlopen(req)
	results = json.loads(qwantResponse.read().decode('utf-8'))
	qwantResponse.close()
	links = []
	for result in results['data']['result']['items']:
		link = result['media']
		if link.startswith('http') and link.endswith('jpg'):
			links.append(link)
	return links

# last recipe processed
i = 0

# max requests
max = 50
			
# get last recipe processed
with open('last-recipe.txt') as f:
	for line in f:
		i = int(line) + 1
		max = max + i

f0 = open('0-images.txt', 'a')
f1 = open('1-image.txt', 'a')
f2 = open('2-images.txt', 'a')
f3 = open('3-images.txt', 'a')

# get title and update images
with open('title-images.xml', 'r', encoding='utf-8') as file:
	tree = ET.parse(file)
	data = tree.getroot()
	imageTag, imagesTag = '', ''
	
	for recipe in data:
		if recipe.attrib['number'] == str(i):
			
			for element in recipe:
				if element.tag == 'title':
					name = element.text.strip()
				if element.tag == 'image':
					imageTag = element
				if element.tag == 'images':
					imagesTag = element
			
			links = getImageURL(name)
			
			if len(links) == 0:
				f0.write(str(i) + ' ' + name + '\n')
				
			elif len(links) == 1:
				f1.write(str(i)  + ' ' + name + '\n')
			elif len(links) == 2:
				f2.write(str(i)  + ' ' + name + '\n')
			elif len(links) == 3:
				f3.write(str(i)  + ' ' + name + '\n')
			
			if len(links) > 0:
				imageTag.text = links[0]
				links.pop(0)
				if len(links) > 0:
					imagesTag.text = '\n' + '\n'.join(map(str, links)) + '\n'
				else:
					imagesTag.text = 'none'
			else:
				imageTag.text = 'none'
				imagesTag.text = 'none'
			
			# save last recipe processed
			tree.write('title-images.xml')
			with open('last-recipe.txt', 'w') as f:
				f.write(str(i))
			print('done: ', str(i))
			i = i + 1
			sleep(10)
		if i == max:
			break