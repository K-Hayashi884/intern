
from django import forms
from .models import CustomUser, Talk
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm, AuthenticationForm

class signup_form(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username','email','icon',]


class LoginForm(AuthenticationForm):
    pass

class PostForm(forms.ModelForm):
    class Meta:
        model = Talk 
        fields = ['content',]

class NameForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username',]

class MailForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email',]

class IconForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['icon',]

class PasswordForm(PasswordChangeForm):
    ''''''
    