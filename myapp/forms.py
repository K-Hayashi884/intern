from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from .models import CustomUser

# アカウント作成フォーム
class SignupForm(UserCreationForm):
    """ Userクラス用フォーム """
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'account_image')

# ログイン用フォーム
class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label

# パスワード変更用フォーム
class PasswordChange_Form(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label

# ユーザー名変更用フォーム
class UsernameChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', )

# メールアドレス変更用フォーム
class EmailChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('email', )

# ユーザーアイコン変更用フォーム
class IconChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('account_image', )