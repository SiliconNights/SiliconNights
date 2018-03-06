from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Recipe, IngredientRecipe, Ingredient, SimilarIngredient

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

class UploadRecipeForm(forms.ModelForm):


    class Meta:
        model = Recipe

        exclude = (
            'user',
            'image',
            'time',
            )
        fields = (
            'name',
            'description',
            'static_image',
            'ingredients',
            'cuisine',
            'type',
            'instructions',
            'author',
            'tags',
            )


'''
class ImageUpload(forms.Form):
    image = forms.ImageField(label = "Upload Photo")
'''
##    recipeName = models.CharField(required=True, max_length = 100, label="Recipe Name")
##    description = models.CharField(required=True)
##    instructions =  models.CharField(
##        widget=models.Textarea(attrs={'cols':'22', 'rows':'10'}),
##    )
    #image = forms.ImageField()
    #author = models.CharField(required=True, max_length = 100, label="Author")
    #publisher = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly','placeholder': User.username}))

##    quantity1 = forms.CharField(label='quantity')
##    ingredient1 = forms.CharField(label='ingredient')
##    quantity2 = forms.CharField(label='quantity')
##    ingredient2 = forms.CharField(label='ingredient')
##    quantity3 = forms.CharField(label='quantity')
##    ingredient3 = forms.CharField(label='ingredient')
##    quantity4 = forms.CharField(label='quantity')
##    ingredient4 = forms.CharField(label='ingredient')
##    quantity5 = forms.CharField(label='quantity')
##    ingredient5 = forms.CharField(label='ingredient')
##    quantity6 = forms.CharField(label='quantity')
##    ingredient6 = forms.CharField(label='ingredient')
##    quantity7 = forms.CharField(label='quantity')
##    ingredient7 = forms.CharField(label='ingredient')
##    quantity8 = forms.CharField(label='quantity')
##    ingredient8 = forms.CharField(label='ingredient')
##    quantity9 = forms.CharField(label='quantity')
##    ingredient9 = forms.CharField(label='ingredient')
##    quantity10 = forms.CharField(label='quantity')
##    ingredient10 = forms.CharField(label='ingredient')


##    def clean(self):
##        cleaned_data = super(UploadRecipeForm, self).clean()
##        recipeName = cleaned_data.get('recipeName')
##        description = cleaned_data.get('description')
##        instructions = cleaned_data.get('instructions')
##        author = cleaned_data.get('author')
##        if not recipeName and not description and not instructions and not author:
##            raise forms.ValidationError('You have to write something!')
##
