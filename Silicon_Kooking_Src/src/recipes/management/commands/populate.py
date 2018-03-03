import os.path
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
import xml.etree.ElementTree as ET
from django.utils import timezone
from recipes.models import Recipe, SimilarIngredient, Ingredient, IngredientRecipe, MealType, MealTypeRecipe, Ethnicity, EthnicityRecipe
import re, pytz
from time import sleep


'''
	NOTE: create one user first.
	python manage.py createsuperuser
'''


# --- Add Ingredient functions --- #

def addAllIngredients():
	pairs = []
	single = []
	ingredientsFile = getFile('ingredients.txt')

	with open(ingredientsFile, 'r', encoding='utf-8') as file:
		for line in file:
			if '|' in line:
				pairs.append(line.strip('\n'))
			else:
				single.append(line.strip('\n'))

	iter1 = (len(pairs)*2)
	iter2 = len(single)

	i = 2		
	for pair in pairs: 
		addIngredientPair(pair)
		printProgressBar(i, iter1, suffix = ' Pair Ingredients')
		i = i + 2
		
	print()
	i = 1
	for ingredient in single:
		addSingleIngredient(ingredient)
		printProgressBar(i, iter2, suffix = ' Single Ingredients')
		i = i + 1

	
def addIngredientPair(pair):
	list = pair.split('|')											
	A = list[0].strip().replace('_', ' ')
	B = list[1].strip().replace('_', ' ')
	
	qA = Ingredient.objects.filter(name__iexact=A) 					
	qB = SimilarIngredient.objects.filter(name__iexact=B)			
																	
	if len(qA) > 0 and len(qB) > 0 and qB[0].similar.id == qA[0].id:
		pass		
	
	elif len(qA) > 0 and len(qB) > 0 and qB[0].similar.id != qA[0].id:
		addSimilarIngredient(qA[0], B)
	
	elif len(qA) > 0 and len(qB) == 0:								
		addSimilarIngredient(qA[0], B)							
		
	elif len(qA) == 0 and (len(qB) > 0 or len(qB) == 0) :
		rA = addIngredient(A)
		addSimilarIngredient(rA, B)
	
	
def addSingleIngredient(A):
	q1A = Ingredient.objects.filter(name__iexact=A)
	
	if len(q1A) == 0:
		addIngredient(A)
	else:
		pass
	
	
def addSimilarIngredient(similarTo, ingredient):
	record = SimilarIngredient(similar=similarTo, name=ingredient)
	record.save()
	
	
def addIngredient(ingredient):
	record = Ingredient(name=ingredient)
	record.save()
	return record

	

# --- Add Meal Type functions --- #

def addAllMealTypes():
	mealTypes = getFile('meal-types.txt')
	types = []
	with open(mealTypes) as f:
		for line in f:
			types.append(line.strip('\n'))
			
	iter1 = len(types)
	i = 1
	for type in types:
		type = type.strip()
		addMealType(type)
		printProgressBar(i, iter1, suffix = ' Meal Types')
		i = i + 1
	
	
def addMealType(type):
	record = MealType(type=type)
	record.save()
	
	
	
# --- Add Ethnicities functions --- #	

def addAllEthnicities():
	ethnicitiesFile = getFile('found-nationalities.txt')		
	ethnicities = []
	with open(ethnicitiesFile) as f:
		for line in f:
			ethnicities.append(line.strip('\n'))
	
	iter1 = len(ethnicities)
	
	i = 1
	for ethnicity in ethnicities:
		ethnicity = ethnicity.strip()
		addEthnicity(ethnicity)
		printProgressBar(i, iter1, suffix = ' Ethnicities')
		i = i + 1
		
def addEthnicity(ethnicity):
	record = Ethnicity(name=ethnicity)
	record.save()
	
	
# --- Add Recipe functions --- #	

def addAllRecipes():
	recipeFile = getFile('recipe-data.xml')
	imageFile = getFile('title-images.xml')
	skipFile = getFile('0-images.txt')
	count = getFile('last-recipe.txt')
	
	max = 0
	with open(count) as f:
			for line in f:
				max = int(line)
				
	skipList = []
	with open(skipFile) as f:
		for line in f:
			line = re.sub(r'[0-9]+ ', '', line)
			skipList.append(line.strip('\n'))

	with open(imageFile, 'r', encoding='utf-8') as f1:
		with open(recipeFile, 'r', encoding='utf-8') as f2:
					
		tree1 = ET.parse(f1)
		tree2 = ET.parse(f2)
		images = tree1.getroot()

		name, imageUrl, ingredients, ingredientList, instructions, tags = '', '', '', '', '', ''
		mealType, ethnicity = '', ''
						
		
		for i in range(0, (max+1)):
			add = True
			data = tree2.getroot()
			
			for element in images[i]:
				if element.tag == 'title' and element.text in skipList:
					add = False
					break
				elif element.tag == 'title':
					name = element.text
				elif element.tag == 'image':
					imageUrl = element.text.strip()
					i = i + 1
					print('image ', name)
					break
			
			if add:
				for recipe in data:
					found = False
					for element in recipe:
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
						elif element.tag == 'ethnicity':
							ethnicity = element.text
						elif element.tag == 'mealType':
							mealType = element.text
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
						
						added = []
						# add meal type
						list = mealType.split(', ')
						for item in list:
							item = item.strip()
							try:
								q1 = MealType.objects.get(type=item)
								if q1.id not in added:
									r1 = MealTypeRecipe(x, recipe.id, q1.id)
									r1.save()
									x = x + 1
									added.append(q1.id)
									print('add meal type ', item)
							except ObjectDoesNotExist:
								pass
						
						
						added = []
						# add ethnicity
						list = ethnicity.split(', ')
						for item in list:
							item = item.strip()
							try:
								q1 = Ethnicity.objects.get(name=item)
								if q1.id not in added:
									r1 = EthnicityRecipe(y, recipe.id, q1.id)
									r1.save()
									y = y + 1
									added.append(q1.id)
									print('add ethnicity', item)
							except ObjectDoesNotExist:
								pass
						
						
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
							
							# (A, -) -> (A, Rec)
							try:
								q1 = Ingredient.objects.get(name=first)
								if q1.id not in added:
									r1 = IngredientRecipe(k, recipe.id, q1.id)
									r1.save()
									k = k + 1
									added.append(q1.id)
							except ObjectDoesNotExist:
								
								# (-, A) -> (A.similar, Rec)
								try:
		
									q2 = SimilarIngredient.objects.filter(name=first)
									if len(q2) > 0:
										for item in q2:
											if item.similar.id not in  added:
												r2 = IngredientRecipe(k, recipe.id, item.similar.id)
												r2.save()
												k = k + 1
												added.append(item.similar.id)
												
									else:
										print(first, second)
										print('WARNING!')
										sleep(10)
								except ObjectDoesNotExist:
									pass
							
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
								# (-, A) -> (A.similar, Rec)
								try:
		
									q2 = SimilarIngredient.objects.filter(name=item)
									if len(q2) > 0:
										for result in q2:
											if result.similar.id not in  added:
												r2 = IngredientRecipe(k, recipe.id, result.similar.id)
												r2.save()
												k = k + 1
												added.append(result.similar.id)
												
									else:
										print(first, second)
										print('WARNING!')
										sleep(10)
								except ObjectDoesNotExist:
									pass
	
# --- Helper functions --- #

def getFile(name):
	scriptpath = os.path.dirname(__file__)
	return os.path.join(scriptpath, name)
	
# Author: https://stackoverflow.com/users/2206251/greenstick
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    if iteration == total: 
        print()
	


# --- Main function --- #	

class Command(BaseCommand):
	args = '<arg1>'
	help = 'first run with "ing", "tag", then "rec" argument'
	
	def add_arguments(self, parser):
			parser.add_argument('arg1')

	def handle(self, *args, **options):

		arg1 = options['arg1']	
		
		
		# --- Add Ingredients --- #
		if arg1 == 'ing':
			
			print('\n Adding ingredients...')
			addAllIngredients()
				
							
		# --- Add Tags ---	#						
		if arg1 == 'tag':
			
			print('\n Adding meal types...')
			addAllMealTypes()
			
			print('\n Adding ethnicities...')
			addAllEthnicities()
		
		
		# --- Add Recipes ---	#
		if arg1 == 'rec':
			`
			
		print('done')