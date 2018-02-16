from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.get_temp_page, name='temp_page'),
    url(r'^(?P<pk>\d+)$', views.recipes_detail_display, name='recipes_detail_display'),
    url(r'^list_recipes/$', views.recipes_detail_list, name='recipes_detail_list'),
]
