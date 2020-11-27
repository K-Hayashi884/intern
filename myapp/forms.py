from django import forms
from django.contrib.auth.forms import (
    UserCreationForm, AuthenticationForm, PasswordChangeForm
)
from .models import User, UserImage

from django.core.exceptions import ValidationError
from django.core.validators import (
  FileExtensionValidator
)

class SignupForm(UserCreationForm):
    img = forms.ImageField(required=False,validators=[FileExtensionValidator(["jpg", "jpeg", "png"])],)


    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='ユーザーネーム', required=True)
    password = forms.CharField(label='パスワード', required=True, min_length=8)

class TalkroomForm(forms.Form):
    talk = forms.CharField(label='talk', \
        widget=forms.TextInput(attrs={'class': 'form-talk'}))

class MyPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class EmailChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', )
    def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       for field in self.fields.values():
           default_label = str(field.label)
           new_label = "new" + default_label
           field.label = new_label

class UserImageChangeForm(forms.ModelForm):
    class Meta:
        model = UserImage
        fields = ("image", )

class UsernameChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', )
    def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       for field in self.fields.values():
           default_label = str(field.label)
           new_label = "new" + default_label
           field.label = new_label
