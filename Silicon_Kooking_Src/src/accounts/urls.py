from django.conf.urls import url, include
from . import views


urlpatterns = [
    url(r'^$', views.view_account, name='view_account'),
    url(r'^login/$', views.login_page, name ='login_page'),
    url(r'logout/$', views.logout_view, name='logout_view'),
    url(r'^register/$', views.register_user, name='registration'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile/edit/$', views.edit_profile, name='edit_profile'),
    url(r'^profile/change-password/$', views.change_password, name='change_password'),
]
