from django.shortcuts import render, redirect
from accounts.forms import (
    RegistrationForm,
    EditProfileForm,
)
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth import update_session_auth_hash


def view_account(request):
    return render(request, 'registration/profile.html')


def login_page(request):
    return render(request, 'registration/login.html', {})

def logout_view(request):
    logout(request)
    return render(request, 'registration/logged_out.html', {})

def register_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/accounts/login')
        else:
            return redirect('/accounts/register')
    else:
        form = RegistrationForm()

        args = {'form': form}
        return render(request, 'registration/registration.html', args)

def profile(request):
    args = {'user': request.user}
    return render(request, 'accounts/profile.html', args)

def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('/accounts/profile')
        else:
            return redirect('/accounts/profile/edit')
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form, 'user': request.user}
        return render(request, 'accounts/editprofile.html', args)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/accounts/profile')
        else:
            return redirect('/accounts/change-password')
    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}

        return render(request, 'accounts/change_password.html', args)
