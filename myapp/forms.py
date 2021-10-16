from django import forms
from django.db.models import fields
from .models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class UserForm(UserCreationForm):
    class Meta: 
        model = User
        fields = UserCreationForm.Meta.fields + ('username', 'email', 'image')