from django.shortcuts import render, get_object_or_404
from .models import Recipe, IngredientRecipe, Ingredient, SimilarIngredient
from .forms import UploadRecipeForm
from django.shortcuts import render, redirect
import re
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
import json

# --- Helper --- #
def get_between(str, first, last):
    try:
        start = str.index(first) + len(first)
        end = str.index(last, start)
        return str[start:end]
    except ValueError:
        return ""
        
def get_from(str, first):
    try:
        start = str.index(first) + len(first)
        return str[start:]
    except ValueError:
        return ""


# Use for listing recipes and querying
# Generic Search
def recipes_detail_list(request):
    request_url = request.build_absolute_uri()
    type = re.findall(r'\?(.*?)\=', request_url)
    
    if type[0] == 'all':
        query = request.GET['all']
        queryset = generic_search(query)
    
    elif type[0] == 'recipe':
        query = request.GET['recipe']
        query = query.split(' ')
        queryset = search_by_recipe_name(query)

 
	# Needs to be refined returning ingredients and recipes as results 
    elif type[0] == 'ingredients':
        query = request.GET['ingredients']
        query = query.split(' ')
        queryset = search_by_ingredient_name(query)

    elif type[0] == 'cuisine':
        query = request.GET['cuisine']
        query = query.split(' ')
        
    elif type[0] == 'meal+type':
        query = request.GET['meal type']
        query = query.split(' ')
        
    if len(queryset) == 0:
        return render(request, 'recipes/no_results.html')

    number_of_pages = 1
    page_list = []
    if len(queryset) > 12:
        number_of_pages = (len(queryset) // 12) + 1
        page_list = [x+1 for x in range(number_of_pages)]


    context = {'object_list': queryset,
                'page': page_list,
                'num_pages': len(page_list)}

    return render(request, 'recipes/list_results.html', context)

# Supports advanced search functionality
def advanced_search(request):
    pass

def generic_search(query):
    # Contains all the queries in a generic search
    list_of_queries = parse_query(query)

    queryset = set()

    queryset = queryset.union(search_by_recipe_name(list_of_queries))

    ingredient_set = set()

    ingredient_set = ingredient_set.union(search_by_ingredient_name(list_of_queries))

    ingredient_set = search_similar_ingredients(ingredient_set, list_of_queries)

    queryset = queryset.union(search_ingredient_recipe(ingredient_set))

    return queryset

# Parse a query represented as a string
def parse_query(query):
    query_list = re.split(r'[^a-zA-Z]', query)

    query_list = list(filter(lambda a: a != '', query_list))

    if len(query_list) > 1:
        combined_list_as_string = []
        for q in query_list:
            combined_list_as_string.append(q)
            combined_list_as_string.append(' ')
        else:
            del combined_list_as_string[-1]


        query_list.append(''.join(combined_list_as_string))


    return query_list

def search_by_recipe_name(list_of_queries):
    queryset = set()
    for q in list_of_queries:
        print(q)
        # Search By Recipe Name
        for recipe in Recipe.objects.filter(name__icontains=q):
            queryset.add(recipe)
    return queryset

def search_ingredient_recipe(ingredient_set):
    queryset = set()

    # Adds the remaining results from IngredientRecipe into queryset
    for i in ingredient_set:
        for recipe in IngredientRecipe.objects.filter(ingredient=i):
            queryset.add(recipe.recipe)

    return queryset

def search_by_ingredient_name(list_of_queries):
    ingredient_set = set()
    for q in list_of_queries:
        # Search By Ingredient Name In Ingredient Table
        for i in Ingredient.objects.filter(name__icontains=q):
            ingredient_set.add(i)

    return ingredient_set

def search_similar_ingredients(ingredients, list_of_queries):
    ingredient_set = set()
    similar_ingredient_set = set()

    # Finds Similar Ingredients
    for q in list_of_queries:
        for items in SimilarIngredient.objects.filter(name__icontains=q):
            ingredient_set.add(items.similar)

    for i in ingredients:
        for items in SimilarIngredient.objects.filter(name__icontains=i.name):
            similar_ingredient_set.add(items.similar)

    return ingredient_set.union(similar_ingredient_set)

def get_temp_page(request):
    return render(request, 'recipes/recipe_page.html', {})

def recipes_detail_display(request, pk):
    recipe = Recipe.objects.get(pk=pk)
    
    # Wikimedia Recipes
    if recipe.author == 'wikimedia':

        ingredients = recipe.ingredients.strip('\n') 
        headers = re.findall(r'(\=\=\=.*?\=\=\=)', ingredients)
        
        # Get ingredient sections
        ingredients_sections = []
        ingredients_header = []
        ingredients_body = []
        
        if len(headers) > 0:
        
            if ingredients.index(headers[0]) != 0:
                headers.insert(0, 'none')
                ingredients_header.append('none')
                
            for i in range(0, len(headers)):
                if i == 0 and headers[i] == 'none':
                        section_ingredients = ingredients[0:ingredients.index(headers[1])].strip('\n')
                        list = section_ingredients.split('\n')
                        ingredients_body.append(list)
                
                elif i == 0:
                        section_ingredients = get_between(ingredients, headers[0], headers[1]).strip('\n')
                        ingredients_header.append(headers[0])
                        list = section_ingredients.split('\n')
                        ingredients_body.append(list)
                        
                elif i < len(headers) - 1:
                    section_ingredients = get_between(ingredients, headers[i], headers[i+1]).strip('\n')
                    ingredients_header.append(headers[i])
                    list = section_ingredients.split('\n')
                    ingredients_body.append(list)
            
                elif i == len(headers) - 1:
                    section_ingredients = get_from(ingredients, headers[i]).strip('\n')
                    ingredients_header.append(headers[i])
                    list = section_ingredients.split('\n')
                    ingredients_body.append(list)

            
            ingredients_header = [item.strip('=') for item in ingredients_header]
            ingredients_sections = zip(ingredients_header, ingredients_body)
        
            
        else: 
            ingredients_header.append('none')
            list = ingredients.split('\n')
            ingredients_body.append(list)
            ingredients_sections = zip(ingredients_header, ingredients_body)
            


        instructions = recipe.instructions.strip('\n') 
        headers = re.findall(r'(\=\=\=.*?\=\=\=)', instructions)

        # Get instruction sections
        instructions_sections = []
        instructions_header = []
        instructions_body = []
        if len(headers) > 0:
            
            if instructions.index(headers[0]) != 0:
                headers.insert(0, 'none')
                instructions_header.append('none')
                
            for i in range(0, len(headers)):
                if i == 0 and headers[i] == 'none':
                        section_instructions = instructions[0:instructions.index(headers[1])].strip('\n')
                        list = section_instructions.split('\n')
                        instructions_body.append(list)
                
                elif i == 0:
                        section_instructions = get_between(instructions, headers[0], headers[1]).strip('\n')
                        instructions_header.append(headers[0])
                        list = section_instructions.split('\n')
                        instructions_body.append(list)
                        
                elif i < len(headers) - 1:
                    section_instructions = get_between(instructions, headers[i], headers[i+1]).strip('\n')
                    instructions_header.append(headers[i])
                    list = section_instructions.split('\n')
                    instructions_body.append(list)
            
                elif i == len(headers) - 1:
                    section_instructions = get_from(instructions, headers[i]).strip('\n')
                    instructions_header.append(headers[i])
                    list = section_instructions.split('\n')
                    instructions_body.append(list)

            
            instructions_header = [item.strip('=') for item in instructions_header]
            instructions_sections = zip(instructions_header, instructions_body)
        
        else: 
            instructions_header.append('none')
            list = instructions.split('\n')
            instructions_body.append(list)
            instructions_sections = zip(instructions_header, instructions_body)
                

    
    
    # Uploaded recipes
    else:
        # Get ingredient sections
        ingredients_sections = []
        ingredients_header = []
        ingredients_body = []
        
        ingredients = recipe.ingredients.strip('\n') 
        
        ingredients_header.append('none')
        list = ingredients.split('\n')
        ingredients_body.append(list)
        ingredients_sections = zip(ingredients_header, ingredients_body)

        
        # Get instruction sections
        instructions_sections = []
        instructions_header = []
        instructions_body = []
    
        instructions = recipe.instructions.strip('\n') 
        
        instructions_header.append('none')
        list = instructions.split('\n')
        instructions_body.append(list)
        instructions_sections = zip(instructions_header, instructions_body)
        
        
##      # Parse Ingredients
##      ingredients_list = recipe.ingredients.split('\n')
##      ingredients_list = list(filter(lambda a: a != '', ingredients_list))
##      for i in range(len(ingredients_list)):
##          ingredients_list[i] = ingredients_list[i].strip()

##      # Parse Instructions
##      instruction_list = recipe.instructions.split('\n')
##      instruction_list = list(filter(lambda a: a != '', instruction_list))
##      for i in range(len(instruction_list)):
##          instruction_list[i] = instruction_list[i].strip()

##    if recipe.author == 'wikimedia':
##        # Parse Ingredients
##        ingredients_list = recipe.ingredients.split('\n')
##        ingredients_list = list(filter(lambda a: a != '', ingredients_list))
##        for i in range(len(ingredients_list)):
##            ingredients_list[i] = ingredients_list[i].strip()
##
##        # Parse Instructions
##        instruction_list = recipe.instructions.split('\n')
##        instruction_list = list(filter(lambda a: a != '', instruction_list))
##        for i in range(len(instruction_list)):
##            instruction_list[i] = instruction_list[i].strip()


    args = {'recipe': recipe,
                'ingredients_sections': ingredients_sections,
                'instructions_sections': instructions_sections}
    return render(request, 'recipes/recipe_page.html', args)

def upload_recipe(request):

    if request.method == 'POST':
        form = UploadRecipeForm(request.POST, request.FILES or None)
        #imageForm = ImageUpload(request.POST, request.FILES)

        if form.is_valid():
            form.instance.user = request.user
                #image = Image()
                #Image.image = ImageUpload.cleaned_data["image"]
                #Image.save()
            form.save()
            return redirect('/recipes/upload')
    else:
        form = UploadRecipeForm()
        #imageForm = ImageUpload()
    return render(request,'recipes/uploadRecipe.html',{'form':form})



##    if request.method == 'POST':
##
##        imageForm = ImageUpload(request.POST, request.FILES)
##
##
##        if imageForm.is_valid():
##
##            image = Image(image = request.FILES['image'])
##            #Image.image = ImageUpload.cleaned_data["image"]
##            Image.save()
##
##
##            return HttpResponseRedirect(reverse(''))
##
##    else:
##        imageForm = ImageUpload()
##
##    return render(request,'recipes/uploadRecipe.html',{'imageForm':imageForm})
def get_recipes(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        recipes = Recipe.objects.filter(name__icontains=q)
        results = []
        
        for re in recipes:
            recipe_json = {}
            recipe_json = re.name 
            results.append(recipe_json)
            data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype) 
