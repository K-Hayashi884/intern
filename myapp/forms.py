from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    UserCreationForm,
)
from django.core.exceptions import ValidationError
from django.forms.widgets import Select

from .models import Talk

User = get_user_model()

NG_WORDS = ["バカ", "ばか", "アホ", "あほ", ]


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "icon")


class LoginForm(AuthenticationForm):
    pass


class MailSettingForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email",)
        labels = {"email": "新しいユーザー名"}


class UserNameSettingForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username",)
        labels = {"username": "新しいメールアドレス"}


class ImageSettingForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("icon",)


class PasswordChangeForm(PasswordChangeForm):
    """Django 標準パスワード変更フォーム

    Djangoはユーザモデルに未加工の (単なるテキストの) パスワードは保存せずハッシュ値でのみ保存する。
    したがって、正しく理解しないとユーザのパスワード属性を直接操作できない。
    よってパスワード編集のために標準で用意されているformを使う。
    """


class FriendsSearchForm(forms.Form):
    """友達の中から任意のユーザーを検索"""

    keyword = forms.CharField(
        label="検索",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "ユーザー名で検索"}),
    )


class TalkForm(forms.ModelForm):
    """トークの送信のためのform

    メッセージを送信するだけで、誰から誰か、時間は全て自動で対応できるのでこれだけで十分
    """

    class Meta:
        model = Talk
        fields = ("talk",)
        # 入力予測の表示をさせない（めっちゃ邪魔）
        widgets = {"talk": forms.TextInput(attrs={"autocomplete": "off"})}

    def clean(self):
        cleaned_data = super().clean()
        talk = cleaned_data.get("talk")
        contained_ng_words = [w for w in NG_WORDS if w in talk]
        if contained_ng_words:
            raise ValidationError(
                f"禁止ワード {', '.join(contained_ng_words)} が含まれています")
        return cleaned_data

    # def clean_talk(self):
    #     talk = self.cleaned_data.get("talk")
    #     contained_ng_words = [w for w in NG_WORDS if w in talk]
    #     if contained_ng_words:
    #         raise ValidationError(
    #             f"禁止ワード {', '.join(contained_ng_words)} が含まれています")
    #     return talk
