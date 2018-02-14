from django.db import models 
from django.contrib.auth.models import User

class Recipe(models.Model):
    name = models.CharField(db_column='name', max_length=45, null=True)
    image = models.CharField(db_column='image', max_length=200, null=True)
    ingredients = models.TextField(db_column='ingredient', null=True)
    instructions = models.TextField(db_column='instructions', null=True)
    author = models.CharField(db_column='author', max_length=45, null=True)
    publisher = models.ForeignKey(User, db_column='user', on_delete=models.PROTECT, null=True)
    time = models.DateTimeField(db_column='time', null=True)
    tags = models.TextField(db_column='tags', null=True)

    class Meta:
        managed = True
        db_table = 'recipe'

		
class RecipesRecipe(models.Model):
    name = models.CharField(db_column='name', max_length=30)
    updated = models.DateTimeField(db_column='updated')
    timestamp = models.DateTimeField(db_column='timestamp')

    class Meta:
        managed = True
        db_table = 'recipes_recipe'
		
		
class Ingredient(models.Model):
    name = models.CharField(db_column='name', max_length=45, null=True)  

    class Meta:
        managed = True
        db_table = 'ingredient'

		
class Ingredientrecipe(models.Model):
    recipe = models.ForeignKey(Recipe, db_column='recipe', on_delete=models.PROTECT)
    ingredient = models.ForeignKey(Ingredient, db_column='ingredient', on_delete=models.PROTECT)

    class Meta:
        managed = True
        db_table = 'ingredientrecipe'
        unique_together = (('recipe', 'ingredient'),)