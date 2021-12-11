from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from .models import CustomUser
from allauth.account.forms import LoginForm, SignupForm, ResetPasswordKeyForm, ResetPasswordForm


# パスワード変更用フォーム
class PasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs['placeholder'] = '元のパスワード'
        self.fields['new_password1'].widget.attrs['placeholder'] = '新しいパスワード'
        self.fields['new_password2'].widget.attrs['placeholder'] = '新しいパスワード(確認用)'
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

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

# トーク内容送信フォーム
class TalkContentForm(forms.Form):
    content = forms.CharField(max_length=1000, \
        widget=forms.Textarea(attrs={'class':'form-control', 'rows':1}))
    
    def __init__(self, *args, **kwargs):
        super(TalkContentForm, self).__init__(*args, **kwargs)


# ログイン用フォーム
class MyLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

# サインアップ用フォーム
class MySignupForm(SignupForm):
    """ Userクラス用フォーム """
    account_image = forms.ImageField()
    class Meta:
        model = CustomUser

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'ユーザー名'
        self.fields['email'].widget.attrs['placeholder'] = 'メールアドレス'
        self.fields['password1'].widget.attrs['placeholder'] = 'パスワード'
        self.fields['password2'].widget.attrs['placeholder'] = 'パスワード(確認用)'

        for field in self.fields.values():
            if field != self.fields['account_image']:
                field.widget.attrs['class'] = 'form-control'
    
    def signup(self, request, user):
        user.account_image = self.cleaned_data['account_image']
        user.save()
        return user

# パスワードリセット(変更用フォーム)
class MyResetPasswordKeyForm(ResetPasswordKeyForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password2'].widget.attrs['placeholder'] ='パスワード(確認用)'
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

# パスワードリセット(メール送信用フォーム)
class MyResetPasswordForm(ResetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'