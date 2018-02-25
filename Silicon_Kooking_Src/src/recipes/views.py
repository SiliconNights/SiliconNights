from django.shortcuts import render, get_object_or_404
from .models import Recipe, IngredientRecipe, Ingredient, SimilarIngredient

# Use for listing recipes and querying
# Generic Search
def recipes_detail_list(request):

    query = request.GET
    query = query['query']

    # A more robust parse is needed
    # parse_query(query)
    query = query.split()

    # Contains all the queries in a generic search
    list_of_queries = []

    for q in query:
        list_of_queries.append(q)

    queryset = set()

    ingredients_set = set()

    similar_ingredient_set = set()

    for q in list_of_queries:
        # Search By Recipe Name
        for recipe in Recipe.objects.filter(name__icontains=q):
            queryset.add(recipe)

        # Search By Ingredient Name In Ingredient Table
        for i in Ingredient.objects.filter(name__icontains=q):
            ingredients_set.add(i)

    # Finds Similar Ingredients
    for i in ingredients_set:
        for similar in SimilarIngredient.objects.filter(name__icontains=i.name):
            similar_ingredient_set.add(similar.similar)

    ingredients_set = ingredients_set.union(similar_ingredient_set)

    for i in ingredients_set:
        for recipe in IngredientRecipe.objects.filter(ingredient=i):
            queryset.add(recipe.recipe)


    if len(queryset) == 0:
        return render(request, 'recipes/no_results.html')

    context = {'object_list': queryset}
    return render(request, 'recipes/list_results.html', context)

# Supports advanced search functionality
def advanced_search(request):
    pass

# Parse a query represented as a string
def parse_query(query):
    pass

def get_temp_page(request):
    return render(request, 'recipes/recipe_page.html', {})

def recipes_detail_display(request, pk):
    recipe = Recipe.objects.get(pk=pk)
    args = {'recipe': recipe}
    return render(request, 'recipes/recipe_page.html', args)
