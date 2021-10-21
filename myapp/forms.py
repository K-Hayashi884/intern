from django import forms
from django.db import models
from django.db.models import fields
from .models import User, Message
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class UserForm(UserCreationForm):
    class Meta: 
        model = User
        fields = UserCreationForm.Meta.fields + ('username', 'email', 'image')

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['message']