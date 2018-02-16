import os.path
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from recipes.models import Recipe
from datetime import datetime
import xml.etree.ElementTree as ET
import re


'''
	NOTE: create user (run this once) or use a registered user id

user = User.objects.create_user(username='user',
                                 email='email@ssexample.com',
                                 password='password')
'''

'''
	TODO: argument to specify number of recipes to add.
'''

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
			time = datetime.now()
			tags = ' '
			recipe = Recipe(i, name, image, ingredients, directions, author, 1, time, tags)
			i = i + 1
			recipe.save()
			if i == 100:
				break