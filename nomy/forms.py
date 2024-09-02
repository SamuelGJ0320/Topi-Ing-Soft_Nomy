from django.forms import ModelForm
from .models import Nomy
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class NomyForm(ModelForm):
    class Meta:
        model = Nomy
        fields = '__all__'
        exclude = ['author']

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

