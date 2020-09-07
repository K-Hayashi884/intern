from django import forms
from .models import User, MyUserManager
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'img', 'password1', 'password2']
