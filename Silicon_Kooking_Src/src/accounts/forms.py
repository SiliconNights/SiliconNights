from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import (
	authenticate,
	get_user_model,
	login,
	logout,
	)

User = get_user_model()
	
class RegistrationForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = (
			'username',
			'first_name',
			'last_name',
			'email',
			'password1',
			'password2',
		)
		
	def save(self, commit=True):
		user = super(RegistrationForm, self).save(commit=False)
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']
		user.email = self.cleaned_data['email']
		user.password1 = self.cleaned_data['password1']

		if commit:
			user.save()

		return user
	
class UserLoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)
	print("here")
	
	def clean(self, *args, **kwargs):
		print("here")
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")
		user = authenticate(username=username, password=password)
		if not user:
			raise forms.ValidationError("Username does not exist")
		if not user.check_password(password):
			raise forms.ValidationError("Incorrect password")
		return super(UserLoginForm, self).clean(*args, **kwargs)


class EditProfileForm(UserChangeForm):

	class Meta:
		model = User
		fields = (
			'username',
			'email',
			'first_name',
			'last_name',
			'password',
		)
