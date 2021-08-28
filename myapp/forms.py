from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import User

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "icon")


class LoginForm(AuthenticationForm):        
    def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       #htmlの表示を変更可能にします
       self.fields["username"].widget.attrs["class"] = "form-control"
       self.fields["password"].widget.attrs["class"] = "form-control"


# 友達の中から任意のユーザーを検索
class FriendsSearchForm(forms.Form):
    keyword = forms.CharField(label="検索", required=False, widget=forms.TextInput(attrs={"placeholder": "ユーザー名で検索"}))


# トークの送信のためのform
# メッセージを送信するだけで、誰から誰か、時間は全て自動で対応できるのでこれだけで十分
class TalkForm(forms.Form):
    talk = forms.CharField(label="talk")