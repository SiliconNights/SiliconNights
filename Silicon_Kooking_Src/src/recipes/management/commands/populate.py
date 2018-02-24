import os.path
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
import xml.etree.ElementTree as ET
from django.utils import timezone
from recipes.models import Recipe, SimilarIngredient, Ingredient, IngredientRecipe
import re, pytz
from time import sleep


'''
	NOTE: create user (run this once) or use a registered user id
user = User.objects.create_user(username='user',
                                 email='email@ssexample.com',
                                 password='password')
'''

class Command(BaseCommand):
	args = '<arg1>'
	help = 'first run with "ing" argument, then run with "rec" argument'
	def add_arguments(self, parser):
			parser.add_argument('arg1')

	def handle(self, *args, **options):

		arg1 = options['arg1']	
		
		# add ingredients
		if arg1 == 'ing':
			pair = []
			single = []
			i = 1
			j = 1
			scriptpath = os.path.dirname(__file__)
			ingredientsFile = os.path.join(scriptpath, 'ingredients.txt')
			with open(ingredientsFile, 'r', encoding='utf-8') as file:
				for line in file:
					if '|' in line:
						pair.append(line.strip('\n'))
					else:
						single.append(line.strip('\n'))
				
				# add pairs
				for item in pair: 
					print(item)
					list = item.split('|')
					first = list[0].strip().replace('_', ' ')
					second = list[1].strip().replace('_', ' ')
					print(first, second)
					try:
						q1 = Ingredient.objects.get(name=first)
					except ObjectDoesNotExist:
						try:
							q2 = SimilarIngredient.objects.get(name=first)
						except ObjectDoesNotExist:
							try:
								q3 = Ingredient.objects.get(name=second)
								r1 = SimilarIngredient(j, q3.id, first)
								r1.save()
								j = j + 1
							except ObjectDoesNotExist:
								try:
									q4 = SimilarIngredient.objects.get(name=second)
									r1 = SimilarIngredient(j, q4.similar.id, first)
									r1.save()
									j = j + 1
								except ObjectDoesNotExist:
									r1 = Ingredient(i, first)
									r1.save()
									i = i + 1
									r2 = SimilarIngredient(j, r1.id, second)
									r2.save()
									j = j + 1
									pass
					
				# add single
				for item in single:
					item = item.strip().replace('_',' ')
					print(item)
					try:
						q1 = Ingredient.objects.get(name=item)
					except ObjectDoesNotExist:
						try:
							q2 = SimilarIngredient.objects.get(name=item)
						except ObjectDoesNotExist:
							r1 = Ingredient(i, item)
							i = i + 1
							r1.save()
							pass
							
		
		# add recipes and setup search tables
		if arg1 == 'rec':
			scriptpath = os.path.dirname(__file__)
			xmlFile = os.path.join(scriptpath, 'recipe-data.xml')
			imageFile = os.path.join(scriptpath, 'title-images.xml')
			skipFile = os.path.join(scriptpath, '0-images.txt')
			count = os.path.join(scriptpath, 'last-recipe.txt')
			
			
			j = 1
			k = 1
			# get last recipe processed by images
			with open(count) as f:
				for line in f:
					max = int(line)
			
			skipList = []
			# get recipes without images
			with open(skipFile) as f:
				for line in f:
					line = re.sub(r'[0-9]+ ', '', line)
					skipList.append(line.strip('\n'))

			with open(imageFile, 'r', encoding='utf-8') as f1:
				with open(xmlFile, 'r', encoding='utf-8') as f2:
					
					tree1 = ET.parse(f1)
					tree2 = ET.parse(f2)
					images = tree1.getroot()

					name, imageUrl, ingredients, ingredientList, instructions, tags = '', '', '', '', '', ''
						
					# check if should skip, else get image url 
					for i in range(0, (max+1)):
						add = True
						data = tree2.getroot()
						
						for element in images[i]:
							if element.tag == 'title' and element.text in skipList:
								i = i + 1
								add = False
								break
							elif element.tag == 'title':
								name = element.text
							elif element.tag == 'image':
								imageUrl = element.text.strip()
								i = i + 1
							# get recipe information 
								print('image ', name)
								break
						
						if add:
							for recipe2 in data:
								found = False
								for element in recipe2:
									if element.tag == 'title' and element.text != name:
										break
									elif element.tag == 'title':
										test = element.text
									elif element.tag == 'description':
										description = element.text
									elif element.tag == 'ingredients':
										ingredients = element.text
									elif element.tag == 'ingredientList':
										ingredientList = element.text
									elif element.tag == 'instructions':
										instructions = element.text
									elif element.tag == 'tags':
										tags = element.text
										found = True
								if found:
									# add recipe
									author = 'wikimedia'
									publisher = 1
									time = timezone.now()
									print('data  ', test)
									recipe = Recipe(j, name, description, imageUrl, ingredients, ingredientList, instructions, author, 1, time, tags)
									recipe.save()
									j = j + 1
									pair = []
									single = []
									
									added = []
									
									# add ingredient search
									list = ingredientList.split(', ')
									for item in list:
										if '|' in item:
											pair.append(item.strip())
										else:
											single.append(item.strip())
									
									# add pairs
									for item in pair: 
										list = item.split('|')
										first = list[0].strip().replace('_', ' ')
										second = list[1].strip().replace('_', ' ')
										
										try:
											q1 = Ingredient.objects.get(name=first)
											if q1.id not in added:
												r1 = IngredientRecipe(k, recipe.id, q1.id)
												r1.save()
												k = k + 1
												added.append(q1.id)
										except ObjectDoesNotExist:
											try:
												q2 = SimilarIngredient.objects.get(name=first)
												if q2.similar.id not in added:
													r2 = IngredientRecipe(k, recipe.id, q2.similar.id)
													r2.save()
													k = k + 1
													added.append(q2.similar.id)
											except ObjectDoesNotExist:
												print(first, second)
												print('WARNING!')
												sleep(10)
										
									# add single
									for item in single:
										item = item.strip().replace('_',' ')
										try:
											q1 = Ingredient.objects.get(name=item)
											if q1.id not in added:
												r1 = IngredientRecipe(k, recipe.id, q1.id)
												r1.save()
												k = k + 1
												added.append(q1.id)
										except ObjectDoesNotExist:
											try:
												q2 = SimilarIngredient.objects.get(name=item)
												if q2.similar.id not in added: 
													r2 = IngredientRecipe(k, recipe.id, q2.similar.id)
													r2.save()
													k = k + 1
													added.append(q2.similar.id)
											except ObjectDoesNotExist:
												print(item)
												print('WARNING!')
												sleep(10)
		print('done')