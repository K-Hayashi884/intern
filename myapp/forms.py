
from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class signup_form(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username','email','icon']


class LoginForm(AuthenticationForm):
    pass
