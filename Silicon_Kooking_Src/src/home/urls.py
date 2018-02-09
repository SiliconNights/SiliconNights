from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home_display, name= 'home_src'),
]
