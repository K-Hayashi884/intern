from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import Image,User,Message

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1','password2')

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('img',)

class LoginForm(AuthenticationForm):
    pass

class MessageForm(forms.ModelForm):
    class Meta:
        model=Message
        fields=('message',)
        widgets={
            'message': forms.Textarea(attrs={'cols':29, 'wrap': 'hard'}),
        }

class ChangeUsernameForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username',)

class ChangeMailForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)

class ChangeImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('img',)

