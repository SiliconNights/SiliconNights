from django.shortcuts import render, get_object_or_404
from .models import Recipe

# Use for listing recipes and querying
def recipes_detail_list(request):

    query = request.GET
    query = query['query']

    print(query)
    print(Recipe.objects.filter(name=query))
    queryset = Recipe.objects.filter(name=query)

    if len(queryset) == 0:
        return render(request, 'recipes/no_results.html')

    context = {'recipe': queryset}
    return render(request, 'recipes/list_results.html', context)

def get_temp_page(request):
    return render(request, 'recipes/recipe_page.html', {})

def recipes_detail_display(request, pk):
    recipe = Recipe.objects.get(pk=pk)
    args = {'recipe': recipe}
    return render(request, 'recipes/recipe_page.html', args)
