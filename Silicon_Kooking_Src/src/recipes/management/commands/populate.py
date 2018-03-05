import os.path
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
import xml.etree.ElementTree as ET
from django.utils import timezone
from recipes.models import Recipe, SimilarIngredient, Ingredient, IngredientRecipe, MealType, MealTypeRecipe, Cuisine, CuisineRecipe
import re, pytz
from time import sleep
from bs4 import UnicodeDammit
from ftfy import fix_encoding, fix_text


'''
	NOTE: create one user first.
	python manage.py createsuperuser
'''




# --- Add Ingredient functions (Pass Tests)--- #

def addAllIngredients():
	pairs = []
	single = []
	ingredientsFile = getFile('final-ingredients.txt')

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



# --- Add Meal Type functions (Pass Tests)--- #

def addAllMealTypes():
	mealTypes = getFile('meal-types-db.txt')
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



# --- Add Cuisines functions (Pass Tests)--- #

def addAllCuisines():
	cuisinesFile = getFile('found-nationalities.txt')
	cuisines = []
	with open(cuisinesFile) as f:
		for line in f:
			cuisines.append(line.strip('\n'))

	iter1 = len(cuisines)

	i = 1
	for cuisine in cuisines:
		cuisine = cuisine.strip()
		addCuisine(cuisine)
		printProgressBar(i, iter1, suffix = ' Cuisines')
		i = i + 1

def addCuisine(cuisine):
	record = Cuisine(name=cuisine)
	record.save()


# --- Add Recipe functions --- #

def addAllRecipes():
	recipeFile = getFile('recipe-data.xml')
	imageFile = getFile('title-images.xml')
	skipFile = getFile('0-images.txt')
	count = getFile('last-recipe.txt')

	max = 0
	j = 0
	with open(count) as f:
			for line in f:
				max = int(line)

	
	skipList = []
	with open(skipFile, 'r', encoding='utf-8') as f:
		for line in f:
			line = re.sub(r'[0-9]+ ', '', line)
			skipList.append(line.strip('\n'))

	with open(imageFile, 'r', encoding='utf-8') as f1:
		with open(recipeFile, 'r', encoding='utf-8') as f2:

			tree1 = ET.parse(f1)
			tree2 = ET.parse(f2)
			images = tree1.getroot()
			data = tree2.getroot()

			name, imageUrl, description, ingredients, ingredientList, instructions, tags = '', '', '', '', '', '', ''
			mealType, cuisine = '', ''


			for i in range(0, (max+1)):
				add = False
				for element in images[i]:
					if element.tag == 'title' and element.text in skipList:
						i = i + 1
						j = j + 1
						break
					elif element.tag == 'title':
						name = element.text
						current = ''
						for element in data[j]:
							if element.tag == 'title':
								current = element.text
								if current == name:
									j = j + 1
									add = True
					elif element.tag == 'image':
						imageUrl = element.text.strip()
						i = i + 1
						break

				printProgressBar(i, max, suffix = ' Recipes')

				if add:
					for element in data[j]:
						if element.tag == 'title':
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
						elif element.tag == 'cuisine':
							cuisine = element.text
						elif element.tag == 'mealType':
							mealType = element.text

					author = 'wikimedia'
					publisher = User.objects.get(id='1')
					time = timezone.now()
					recipe = Recipe(name=name, description=description, image=imageUrl,
										ingredients=ingredients, ingredientList=ingredientList,
										instructions=instructions, cuisine=cuisine, type=mealType,
										author=author, time=time, tags=tags)
					recipe.save()

					addRecipeMeal(recipe, mealType)

					addRecipeCuisine(recipe, cuisine)

					addRecipeIngredients(recipe, ingredientList)


def addRecipeMeal(recipe, mealType):
	added = []
	list = mealType.split(', ')
	for item in list:
		item = item.strip()
		qItem = MealType.objects.filter(type__icontains=item)
		for type in qItem:
			if type.type not in added:
				r1 = MealTypeRecipe(recipe=recipe, type=type)
				r1.save()
				added.append(type.type)


def addRecipeCuisine(recipe, cuisine):
	added = []
	list = cuisine.split(', ')
	for item in list:
		item = item.strip()
		qItem = Cuisine.objects.filter(name__iexact=item)
		for name in qItem:
			if name.name not in added:
				r1 = CuisineRecipe(recipe=recipe, name=name)
				r1.save()
				added.append(name.name)


def addRecipeIngredients(recipe, ingredientList):
	single, pair, added  = [], [], []
	list = ingredientList.split(', ')
	for item in list:
		if '|' in item:
			pair.append(item.strip())
		else:
			single.append(item.strip())

	for item in pair:
		list = item.split('|')
		A = list[0].strip().replace('_', ' ')
		B = list[1].strip().replace('_', ' ')

		# (A, -) -> (A, Rec)
		qA1 = Ingredient.objects.filter(name__iexact=A)
		if len(qA1) > 0:
			for ingredient in qA1:
				if ingredient.id not in added:
					addIngredientRecipe(recipe, ingredient)
					added.append(ingredient.id)


		# (-, A) -> (A.similar, Rec)
		qA2 = SimilarIngredient.objects.filter(name__iexact=A)
		if len(qA2) > 0:
			for ingredient in qA2:
				if ingredient.similar.id not in added:
					addIngredientRecipe(recipe, ingredient.similar)
					added.append(ingredient.similar.id)

		# (B, -) -> (B, Rec)
		qB1 = Ingredient.objects.filter(name__iexact=B)
		if len(qB1) > 0:
			for ingredient in qB1:
				if ingredient.id not in added:
					addIngredientRecipe(recipe, ingredient)
					added.append(ingredient.id)


		# (-, B) -> (B.similar, Rec)
		qB2 = SimilarIngredient.objects.filter(name__iexact=B)
		if len(qB2) > 0:
			for ingredient in qB2:
				if ingredient.similar.id not in added:
					addIngredientRecipe(recipe, ingredient.similar)
					added.append(ingredient.similar.id)

	for A in single:
		A = A.strip().replace('_',' ')

		# (A, -) -> (A, Rec)
		qA1 = Ingredient.objects.filter(name__iexact=A)
		if len(qA1) > 0:
			for ingredient in qA1:
				if ingredient.id not in added:
					addIngredientRecipe(recipe, ingredient)
					added.append(ingredient.id)


		# (-, A) -> (A.similar, Rec)
		qA2 = SimilarIngredient.objects.filter(name__iexact=A)
		if len(qA2) > 0:
			for ingredient in qA2:
				if ingredient.similar.id not in added:
					addIngredientRecipe(recipe, ingredient.similar)
					added.append(ingredient.similar.id)


def addIngredientRecipe(rec, ing):
	record = IngredientRecipe(recipe=rec, ingredient=ing)
	record.save()


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


def cleanEncoding(line):
	line = fix_encoding(line)
	line = fix_text(line)
	line = UnicodeDammit(line).unicode_markup
	return line

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

			print('\n Adding cuisines...')
			addAllCuisines()

		# --- Add Recipes ---	#
		if arg1 == 'rec':

			print('\n Adding recipes...')
			addAllRecipes()

		# --- Add Ingredients, Tags and Recipes --- #
		if arg1 == 'all':

			print('\n Adding ingredients...')
			addAllIngredients()

			print('\n Adding meal types...')
			addAllMealTypes()

			print('\n Adding cuisines...')
			addAllCuisines()

			print('\n Adding recipes...')
			addAllRecipes()

		print('\n Done')
