from django import forms
from .models import UserImage, Talk
from django.contrib.auth.models import User
from django.contrib.auth import forms as auth_forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.forms import ModelForm


class SignupForm(auth_forms.UserCreationForm):
    email = forms.EmailField(
        max_length = 200,
        required = True,
        label = 'メールアドレス'
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class ImageForm(forms.ModelForm):
	class Meta:
		model = UserImage
		fields = ['image']

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       self.fields['username'].widget.attrs['class'] = 'form-control'
       self.fields['password'].widget.attrs['class'] = 'form-control'

class PostForm(forms.ModelForm):
  class Meta:
    model = Talk
    fields = ['message']

class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class UserChangeMailForm(ModelForm):
    class Meta:
        model = User
        fields = ['email']

    def __init__(self, email=None, *args, **kwargs):
        self.user = kwargs.get('instance', None)
        super().__init__(*args, **kwargs)
        if email:
            self.fields['email'].widget.attrs['value'] = email

    def update(self, user):
        user.email = self.cleaned_data['email']
        user.save()

class FindForm(forms.Form):
    find = forms.CharField(label='find', required=False, widget=forms.TextInput(attrs={'class' : 'form-control'}))

class UserChangeNameForm(ModelForm):
    class Meta:
        model = User
        fields = [
            'username'
        ]

    def __init__(self, username=None, *args, **kwargs):
        self.user = kwargs.get('instance', None)
        super().__init__(*args, **kwargs)
        if username:
            self.fields['username'].widget.attrs['value'] = username

    def update(self, user):
        user.username = self.cleaned_data['username']
        user.save()