from django.db import models
from recipes.models import Recipe


class Home(models.Model):
    week = models.IntegerField(db_column='week')
    type = models.CharField(db_column='type', max_length=45, null=True)
    comments = models.TextField(db_column='comments', blank=True, null=True)
    time = models.DateTimeField(db_column='time', null=True)
    recipe = models.ForeignKey(Recipe, db_column='recipe', on_delete=models.PROTECT)

    class Meta:
        managed = True
        db_table = 'home'
        unique_together = (('week', 'recipe'),)
		

class Pick(models.Model):
    week = models.ForeignKey(Home, db_column='week', on_delete=models.PROTECT) 
    recipe = models.ForeignKey(Recipe, db_column='recipe', on_delete=models.PROTECT)
	
    class Meta:
        managed = True
        db_table = 'pick'
        unique_together = (('week', 'recipe'),)
