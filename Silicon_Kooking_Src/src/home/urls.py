from django.conf.urls import url
from . import views
import recipes.views

urlpatterns = [
    url(r'^$', views.home_display, name= 'home_src'),
    url(r'search', recipes.views.recipes_detail_list, name='recipes_detail_list'),
]
