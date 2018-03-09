from django.db import models
from django.contrib.auth.models import User
from recipes.models import Recipe




class Favorite(models.Model):
    recipe = models.ForeignKey(Recipe, db_column='recipe', on_delete=models.PROTECT)
    user = models.ForeignKey(User, db_column='user', on_delete=models.PROTECT)

    class Meta:
        managed = True
        db_table = 'favorite'
        unique_together = (('recipe', 'user'),)

class ProfileImage(models.Model):
    user = models.ForeignKey(User, db_column='user', on_delete=models.PROTECT, null=True)
    avatar = models.ImageField(db_column="avatar", upload_to = 'profile-img/', default = 'profile-img/default.jpg', blank=True)

    class Meta:
        managed = True
        db_table = 'profile_image'
