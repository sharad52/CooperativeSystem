from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        widgets = {
            'username':forms.TextInput(attrs={'class':'input'}),
            'email':forms.EmailInput(attrs={'class':'input'}),
            'password1':forms.PasswordInput(attrs={'class':'input'}),
            'password2':forms.PasswordInput(attrs={'class':'input'}),
        }