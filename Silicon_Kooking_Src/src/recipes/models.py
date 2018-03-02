from django.db import models
from django.contrib.auth.models import User

class Recipe(models.Model):
    name = models.CharField(db_column='name', max_length=200, null=True)
    description = models.TextField(db_column='description', null=True)
    image = models.CharField(db_column='image', max_length=1000, null=True)
    ingredients = models.TextField(db_column='ingredients', null=True)
    ingredientList = models.TextField(db_column='ingredientList', null=True)
    instructions = models.TextField(db_column='instructions', null=True)
    author = models.CharField(db_column='author', max_length=200, null=True)
    publisher = models.ForeignKey(User, db_column='user', on_delete=models.PROTECT, null=True)
    time = models.DateTimeField(db_column='time', null=True)
    tags = models.TextField(db_column='tags', null=True)

    class Meta:
        managed = True
        db_table = 'recipe'


class RecipesRecipe(models.Model):
    name = models.CharField(db_column='name', max_length=200)
    updated = models.DateTimeField(db_column='updated')
    timestamp = models.DateTimeField(db_column='timestamp')

    class Meta:
        managed = True
        db_table = 'recipes_recipe'


class Ingredient(models.Model):
    name = models.CharField(db_column='name', max_length=200, null=True)
    class Meta:
        managed = True
        db_table = 'ingredient'

class SimilarIngredient(models.Model):
    similar = models.ForeignKey(Ingredient, db_column='similar', on_delete=models.PROTECT)
    name = models.CharField(db_column='name', max_length=200, null=True)
    class Meta:
        managed = True
        db_table = 'similar_ingredient'

class IngredientRecipe(models.Model):
    recipe = models.ForeignKey(Recipe, db_column='recipe', on_delete=models.PROTECT)
    ingredient = models.ForeignKey(Ingredient, db_column='ingredient', on_delete=models.PROTECT)

    class Meta:
        managed = True
        db_table = 'ingredient_recipe'
        unique_together = (('recipe', 'ingredient'),)

class MealType(models.Model):
    type = models.CharField(db_column='type', max_length=100, null=True)
    class Meta:
        managed = True
        db_table = 'meal_type'

class MealTypeRecipe(models.Model):
    recipe = models.ForeignKey(Recipe, db_column='recipe', on_delete=models.PROTECT)
    type = models.ForeignKey(Ingredient, db_column='type', on_delete=models.PROTECT)

    class Meta:
        managed = True
        db_table = 'meal_type_recipe'
        unique_together = (('recipe', 'type'),)

class Ethnicity(models.Model):
    name = models.CharField(db_column='name', max_length=100, null=True)
    class Meta:
        managed = True
        db_table = 'ethnicity'

class EthnicityRecipe(models.Model):
    recipe = models.ForeignKey(Recipe, db_column='recipe', on_delete=models.PROTECT)
    name = models.ForeignKey(Ingredient, db_column='name', on_delete=models.PROTECT)

    class Meta:
        managed = True
        db_table = 'ethnicity_recipe'
        unique_together = (('recipe', 'name'),)

class UploadRecipe(models.Model):
    name = models.CharField(max_length = 200, verbose_name="Recipe_Name_")
    description = models.CharField(max_length = 200,verbose_name="Description")
    instructions = models.TextField()
    #image2 = models.ImageField()
    #image = models.CharField(max_length = 100)
    author = models.CharField(max_length = 100)
    ingredients = models.TextField(db_column='ingredients', null=True)
    user = models.CharField(max_length=11)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'recipe'
