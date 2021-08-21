from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import User


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'icon')


class LoginForm(AuthenticationForm):        
    def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       #htmlの表示を変更可能にします
       self.fields['username'].widget.attrs['class'] = 'form-control'
       self.fields['password'].widget.attrs['class'] = 'form-control'


class MailSettingForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = "新しいメールアドレス"


class UserNameSettingForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "新しいユーザー名"
        

class ImageSettingForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("icon", )


class PasswordChangeForm(PasswordChangeForm):
    """
    Django標準パスワード変更フォーム
    Djangoはユーザモデルに未加工の (単なるテキストの) パスワードは保存せず
    ハッシュ値でのみ保存します。
    したがって、ユーザのパスワード属性を直接操作できない。
    よってパスワード編集のために標準で用意されているformを使います。
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


# 友達の中から任意のユーザーを検索
class FriendsSearchForm(forms.Form):
    keyword = forms.CharField(label='検索', required=False, widget=forms.TextInput(attrs={'placeholder': 'ユーザー名で検索'}))
    

# トークの送信のためのform
# メッセージを送信するだけで、誰から誰か、時間は全て自動で対応できるのでこれだけで十分
class TalkForm(forms.Form):
    talk = forms.CharField(label='talk')
