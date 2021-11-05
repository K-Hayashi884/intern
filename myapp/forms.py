from os import truncate
from django import forms
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields import CharField, TextField
from django.forms import fields, widgets
from django.forms.forms import Form
from django.contrib.auth.forms import AuthenticationForm

from myapp.models import CustomUser
from myapp.models import Message


class SignupForm(UserCreationForm):
    username = forms.CharField(
        max_length=30,
        required=True,
        label="Username",
    )
    email = forms.EmailField(
        max_length=100,
        required=True,
        label="Email",
    )
    image = forms.ImageField(
        required=False,
        label="Image",
    )

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'image')

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'

class MessageForm(forms.Form):
    content = forms.CharField(
        label="message", 
        required=True,
        max_length=1000,
        widget=forms.TextInput(
            attrs={
                "class":"form-control",
            }
        )
    )

class UserUpdateForm(forms.Form):
    username = forms.CharField(
        max_length=30,
        required=False,
        label="Username",
    )
    email = forms.EmailField(
        max_length=100,
        required=False,
        label="Email",
    )
    image = forms.ImageField(
        required=False,
        label="Image",
    )

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'image')