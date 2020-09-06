from django import forms
from .models import MyUserManager
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
User = get_user_model()

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'img', 'password1', 'password2']
