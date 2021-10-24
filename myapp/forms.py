from django import forms
from django.db import models
from django.db.models import fields
from .models import User, Message
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm

class UserForm(UserCreationForm):
    class Meta: 
        model = User
        fields = UserCreationForm.Meta.fields + ('username', 'email', 'image')

class UsernameChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']

class EmailChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']

class ImageChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['image']

class MyPasswordChangeForm(PasswordChangeForm):
     def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['message']