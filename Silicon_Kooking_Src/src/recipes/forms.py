from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


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

class UploadRecipeForm(forms.Form):
    recipeName = forms.CharField(required=True, max_length = 100, label="Recipe Name")
    description = forms.CharField(required=True)
    instructions =  forms.CharField(widget=forms.Textarea(attrs={'cols':'25',
'rows':'10'}), required=True,)
    image = forms.ImageField()
    author = forms.CharField(required=True, max_length = 100, label="Author")
    publisher = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly','placeholder': User.username}))

 
        
           
    
    
