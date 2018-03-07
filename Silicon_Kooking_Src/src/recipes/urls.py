from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<pk>\d+)$', views.recipes_detail_display, name='recipes_detail_display'),
    url(r'^upload', views.upload_recipe, name='upload_recipe'),
    url(r'^api/get_recipes/', views.get_recipes, name='get_recipes'),
]
