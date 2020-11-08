from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
#from .models import Users

#と思ったけど、やっぱモデルつかう
class SignupForm(UserCreationForm):
    img = forms.ImageField(label="Img", required=False)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


"""
class SignupForm(forms.Form):
    # Djangoの標準フォームがよう分からんからそのままつくる
    username = forms.CharField(label='Username',required=True)
    email = forms.EmailField(label='Email',required=True,)
    password = forms.CharField(label='Password',required=True,min_length=8)
    corfirmation = forms.CharField(label='Password confirmation',\
        required=True,min_length=8)
    img = forms.ImageField(label='Img', required=False)
"""

"""
#ModelFormもちょっと疑問点多いから保留
class SignupForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = []
"""

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='ユーザーネーム', required=True)
    password = forms.CharField(label='パスワード', required=True, min_length=8)

