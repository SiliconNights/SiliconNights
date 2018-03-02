import xml.etree.ElementTree as ET
import re, json, pytz, urllib.parse, urllib.request
from time import sleep
from bs4 import UnicodeDammit
from ftfy import fix_encoding, fix_text
import json, requests
from random import randint

header = {
	'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language': 'en-US,en;q=0.5',
	'Connection' : 'keep-alive',
	'Host' : 'api.qwant.com',
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
	'Content-Type': 'application/json'
}

# get image url
def getImageURL(name):
	print(name)
	name = re.sub(' ', '_', name)
	url = "https://api.qwant.com/api/search/images?ie=UTF-8&count=10&offset=0&q=" + urllib.parse.quote(name)
	resp = requests.get(url, headers=header)
	results = resp.json()
	links = []
	for result in results['data']['result']['items']:
		link = result['media']
		if link.startswith('http') and link.endswith('jpg'):
			links.append(link)
	return links

# last recipe processed
i = 0

# max requests
max = 500
			
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
			sleep(randint(10, 25))
		if i == max:
			break