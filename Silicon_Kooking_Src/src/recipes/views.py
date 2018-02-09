from django.shortcuts import render, get_object_or_404
from .models import Recipe

def recipes_detail(request):
    queryset = Recipe.objects.all()
    context = {'object_list': queryset}

    return render(request, 'recipes/recipe_page.html', context)
