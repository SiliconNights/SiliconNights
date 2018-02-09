from django.shortcuts import render, HttpResponse
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,

)

from .forms import UserLoginForm

def accounts_page(request):
    return render(request, 'index.html', {})

'''
def login_view(request):
    form = UserLoginForm(request.Post or None)

    if(form.isValid())

    return render(request, 'form.html', {})


def register_view(request):
    return render(request, 'form.html', {})


def logout_view(request):
    return render(request, 'from.html', {})
'''
