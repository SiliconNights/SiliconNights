from django.shortcuts import render, get_object_or_404
from .models import Recipe, IngredientRecipe, Ingredient, SimilarIngredient
from .forms import UploadRecipeForm
from django.shortcuts import render, redirect
import re
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect


# Use for listing recipes and querying
# Generic Search
def recipes_detail_list(request):

    query = request.GET
    query = query['query']

    queryset = generic_search(query)

    print(queryset)

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


    # Parse Ingredients
    ingredients_list = recipe.ingredients.split('\n')
    ingredients_list = list(filter(lambda a: a != '', ingredients_list))
    for i in range(len(ingredients_list)):
        ingredients_list[i] = ingredients_list[i].strip()

    # Parse Instructions
    instruction_list = recipe.instructions.split('\n')
    instruction_list = list(filter(lambda a: a != '', instruction_list))
    for i in range(len(instruction_list)):
        instruction_list[i] = instruction_list[i].strip()


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
            'ingredients_list': ingredients_list,
            'instruction_list': instruction_list}
    return render(request, 'recipes/recipe_page.html', args)

def upload_recipe(request):

    if request.method == 'POST':
        form = UploadRecipeForm(request.POST)
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
