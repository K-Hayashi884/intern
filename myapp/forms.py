# from django.db import models
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from .models import User

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'image']

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

class MessageForm(forms.Form):
    contents = forms.CharField(max_length=150)

class PasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

class UsernameChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username'] 

class ImageChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['image'] 

class EmailChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email'] 




