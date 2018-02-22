from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<pk>\d+)$', views.recipes_detail_display, name='recipes_detail_display'),
]
