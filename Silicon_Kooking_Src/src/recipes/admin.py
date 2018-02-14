from django.contrib import admin

from .models import Recipe, RecipesRecipe, Ingredient, Ingredientrecipe
# Register your models here.

admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(RecipesRecipe)
admin.site.register(Ingredientrecipe)