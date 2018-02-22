import os.path
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
import xml.etree.ElementTree as ET
from django.utils import timezone
from recipes.models import Recipe
import re, json, urllib.request, pytz
from time import sleep


'''
	NOTE: create user (run this once) or use a registered user id
user = User.objects.create_user(username='user',
                                 email='email@ssexample.com',
                                 password='password')
'''

'''
	TODO: argument to specify number of recipes to add.
'''

header = {'User-Agent': 'bots',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

# get image url
def getImageURL(name):
	name = name.lstrip(' ')
	name = name.rstrip(' ')
	name = re.sub(' ', '_', name)
	url = "https://api.qwant.com/api/search/images?count=10&offset=0&q=" + name
	req = urllib.request.Request(url, None, header)
	qwantResponse = urllib.request.urlopen(req)
	results = json.loads(qwantResponse.read().decode('utf-8'))
	qwantResponse.close()
	for i in range(0,10):
		link = results['data']['result']['items'][i]['media']
		if link.endswith('jpg'):
			print(link)
			return link


class Command(BaseCommand):
	args = '<none>'
	help = 'Adds recipes to recipe table'

	def handle(self, *args, **options):
		scriptpath = os.path.dirname(__file__)
		xmlfile = os.path.join(scriptpath, 'recipe-data.xml')

		with open(xmlfile, 'r', encoding='utf-8') as file:
			tree = ET.parse(file)

		data = tree.getroot()

		name, image, ingredients, directions = '', '', '', ''
		i = 1
		for recipe in data:
			for element in recipe:
				if element.tag == 'title':
					name = element.text
				elif element.tag == 'image':
					image = element.text
				elif element.tag == 'ingredients':
					ingredients = element.text
				elif element.tag == 'directions':
					directions = element.text
			author = 'wikimedia'
			publisher = 1
			time = timezone.now()
			tags = ' '
			image = getImageURL(name)
			recipe = Recipe(i, name, image, ingredients, directions, author, 1, time, tags)
			i = i + 1
			recipe.save()
			sleep(7)
			if i == 100:
				break
