from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from .models import CustomUser, Talk

# アカウント作成フォーム
class SignupForm(UserCreationForm):
    """ Userクラス用フォーム """
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'account_image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'ユーザー名'
        self.fields['email'].widget.attrs['placeholder'] = 'メールアドレス'
        self.fields['password1'].widget.attrs['placeholder'] = 'パスワード'
        self.fields['password2'].widget.attrs['placeholder'] = 'パスワード(確認用)'

# ログイン用フォーム
class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'ユーザー名'
        self.fields['password'].widget.attrs['placeholder'] = 'パスワード'
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

# パスワード変更用フォーム
class PasswordChange_Form(PasswordChangeForm):
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