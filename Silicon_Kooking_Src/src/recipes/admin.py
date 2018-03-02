from django.contrib import admin

from .models import Recipe, RecipesRecipe, Ingredient, IngredientRecipe, SimilarIngredient
# Register your models here.

admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(RecipesRecipe)
admin.site.register(IngredientRecipe)
admin.site.register(SimilarIngredient)
