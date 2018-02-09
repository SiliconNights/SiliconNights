from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^home/$', views.home_display, name='home_display')
]
