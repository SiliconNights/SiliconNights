from django.db import models
# Create your models here

class Recipe(models.Model):
    name = models.CharField(max_length=30)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.name
