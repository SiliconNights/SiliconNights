from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.accounts_page, name='accounts_page')
]
