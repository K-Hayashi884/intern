from django import forms
from django.core.validators import MinLengthValidator
from django.contrib.auth.forms import(AuthenticationForm)
from .models import User
from django.contrib.auth.forms import UserCreationForm


class signup (UserCreationForm):
    class Meta():
        model = User
        fields = ("username", "mail", "image",)


class loginform (AuthenticationForm):
    username=forms.CharField(max_length=20, unique=True)
    password = forms.CharField(max_length=50,blank=True,null=True,validators=[MinLengthValidator(8)])
 
