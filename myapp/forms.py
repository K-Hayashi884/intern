from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import CustomUser

class SignupForm(UserCreationForm):
    email = forms.EmailField(label='Email')
    img = forms.ImageField(label='Img')

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'img')

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'


