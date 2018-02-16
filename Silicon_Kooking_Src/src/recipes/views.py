from django.shortcuts import render, get_object_or_404
from .models import Recipe

# Use for listing recipes and querying
def recipes_detail_list(request):
    queryset = Recipe.objects.all()
    context = {'object_list': queryset}

    return render(request, 'recipes/recipe_list.html', context)

def get_temp_page(request):
    return render(request, 'recipes/recipe_page.html', {})

def recipes_detail_display(request, pk):
    recipe = Recipe.objects.get(pk=pk)
    args = {'recipe': recipe}
    return render(request, 'recipes/recipe_page.html', args)
