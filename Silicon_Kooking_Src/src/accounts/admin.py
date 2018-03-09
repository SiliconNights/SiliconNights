from django.contrib import admin

from .models import Favorite, ProfileImage

# Register your models here.

admin.site.register(Favorite)
admin.site.register(ProfileImage)
