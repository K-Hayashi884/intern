from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    PasswordChangeForm,
)
from .models import User, Talk


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'img')
        labels = {
            'username': 'ユーザーネーム',
            'email': 'メールアドレス',
            'img': 'アイコン',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = 'パスワード'
        self.fields['password2'].label = 'パスワード確認'


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'ユーザーネーム'
        self.fields['password'].label = 'パスワード'


class ChangeUsernameForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', )
        labels = {
            'username': '新しいユーザーネーム',
        }

class ChangeEmailForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', )
        labels = {
            'email': '新しいメールアドレス',
        }

class ChangeIconForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('img', )
        labels = {
            'img': '新しいアイコン',
        }

class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].label = '現在のパスワード'
        self.fields['new_password1'].label = '新しいパスワード'
        self.fields['new_password2'].label = '新しいパスワード確認'
    pass

class TalkForm(forms.ModelForm):
    class Meta:
        model = Talk
        fields = ('message', )
        widgets = {
            'message': forms.Textarea,
        }