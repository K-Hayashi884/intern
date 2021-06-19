from django import forms
from django.contrib.admin.options import get_content_type_for_model
from django.db import models
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django import forms
from django.contrib.auth.forms import UsernameField	
from django.contrib.auth.models import User
from django.contrib.auth import forms as auth_forms
from .models import Photo, Message

class HelloForm(forms.Form):
    Username = forms.CharField(label='Username')
    Passward = forms.CharField(min_length=8, label='Passward')

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('image',)
        labels = {
            'image': 'img'
        }

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError(
            "パスワードが一致しませんでした。パスワードを入力し直してください。"
            )

class NameForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']

class emailchangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']

class passwordchangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['password']


class LoginForm(auth_forms.AuthenticationForm):
    '''ログインフォーム'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label 

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        labels = {
            'content': '',

        }
    
