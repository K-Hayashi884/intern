from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import (
  FileExtensionValidator
)
from django.contrib.auth.forms import AuthenticationForm
from .models import User
from django.contrib.auth.forms import PasswordChangeForm

class SignUpForm(UserCreationForm):
   image = forms.ImageField( required=False, validators=[FileExtensionValidator(["jpg", "jpeg", "png"])],)
   class Meta:
    model = User
    fields = ('username', 'email', 'password1', 'password2')

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
     super().__init__(*args, **kwargs)
     self.fields['username'].widget.attrs['class'] = 'form-control'
     self.fields['password'].widget.attrs['class'] = 'form-control'

class TalkForm(forms.Form):
  talk = forms.CharField(label='talk')


class PasswordChangeForm(PasswordChangeForm):
   def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       for field in self.fields.values():
           field.widget.attrs['class'] = 'form-control'


