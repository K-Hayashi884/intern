from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User=get_user_model()

class SignupForm(UserCreationForm):

    class Meta:
        model =User
        fields = ('username', 'email','img')

class MessageForm(forms.Form):
    message= forms.CharField()

class ChangeUsernameForm(forms.ModelForm):
    username=forms.CharField(label='New username')
    class Meta:
        model = User
        fields=('username',)

class ChangeEmailForm(forms.ModelForm):
    email=forms.EmailField(label='New email')
    class Meta:
        model = User
        fields=('email',)

class ChangeImageForm(forms.ModelForm):
    img=forms.ImageField()
    class Meta:
        model= User
        fields=('img',)

class ChangePasswordForm(UserCreationForm):

    class Meta:
        model = User
        exclude=['password','last_login','groups','user_permissions','username','date_joined','email','img','first_name','last_name']
        fields={'password'}