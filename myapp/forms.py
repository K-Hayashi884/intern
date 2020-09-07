from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import (
    FileExtensionValidator
)
# from .models import User

class SignUpForm(UserCreationForm):
    img = forms.ImageField(
        required=False, validators=[FileExtensionValidator(["jpg", "jpeg", "png"])],
    )
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class LoginForm(AuthenticationForm):        
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(
                _("This account is inactive."),
                code='inactive',
            )

    def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       #htmlの表示を変更可能にします
       self.fields['username'].widget.attrs['class'] = 'form-control'
       self.fields['password'].widget.attrs['class'] = 'form-control'

# 友達の中から任意のユーザーを検索
class FriendsSearchForm(forms.Form):
    keyword = forms.CharField(label='検索',required=False,widget=forms.TextInput(attrs={'placeholder': 'ユーザー名で検索'}))
    
# トークの送信のためのform
# メッセージを送信するだけで、誰から誰か、時間は全て自動で対応できるのでこれだけで十分
class TalkForm(forms.Form):
    talk = forms.CharField(label='talk')