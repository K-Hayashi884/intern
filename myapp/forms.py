from django import forms
from .models import User, UserImage, Talk
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import get_user_model

class SignUpForm(UserCreationForm):
    img = forms.ImageField(required = False)

    class Meta:
        model= User
        fields = [ 'username', 'email', 'password1', 'password2']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=128)

class TalkForm(forms.Form):
    talk_msg = forms.CharField(max_length=100)

class ChangeNameForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username']

class ChangeMailForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['email']

class ChangeIconForm(forms.ModelForm):
    class Meta:
        model = UserImage
        fields=['user','image']

    

class MyPasswordChangeForm(PasswordChangeForm):
    """パスワード変更フォーム"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'