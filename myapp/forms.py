from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Talk

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'img')

class LoginForm(AuthenticationForm):
    pass

class TalkForm(forms.ModelForm):
    class Meta:
        model = Talk
        fields = ('message', )
        widgets = {
            'message': forms.Textarea,
        }