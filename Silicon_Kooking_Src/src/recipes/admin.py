from django.contrib import admin

from .models import (
    Recipe,
    RecipesRecipe,
    Ingredient,
    IngredientRecipe,
    SimilarIngredient,
    Cuisine,
    CuisineRecipe,
    MealType,
    MealTypeRecipe,
)
# Register your models here.

admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(RecipesRecipe)
admin.site.register(IngredientRecipe)
admin.site.register(SimilarIngredient)
admin.site.register(Cuisine)
admin.site.register(CuisineRecipe)
admin.site.register(MealType)
admin.site.register(MealTypeRecipe)
