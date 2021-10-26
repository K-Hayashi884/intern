from django import forms
from django.contrib.auth.models import User
from .models import Account, Message
#フォームクラス作成
class AccountForm(forms.ModelForm):
    #パスワード入力：非表示対応
    password = forms.CharField(widget=forms.PasswordInput(),label="パスワード")

    class Meta():
        #ユーザー認証
        model = User
        #フィールド指定
        fields = ('username','email','password')
        labels = {'username':"ユーザーID",'email':"メール", 'password':"パスワード"}

class AddAccountForm(forms.ModelForm):
    class Meta():
        #モデルクラスを指定
        model = Account
        fields = ('last_name','first_name','account_image',)
        labels = {'last_name':"苗字",'first_name':"名前",'account_image':"写真アップロード",}

#メッセージクラス
class MessageForm(forms.ModelForm):
    class Meta():
        model = Message
        fields = ('title','content')
        labels =  {'title':"タイトル",'content':"本文"}

#名前変更のフォーム
class NameChangeForm(forms.ModelForm):
    class Meta():
        model = Account
        fields = ('last_name', 'first_name')
        labels = {'last_name':"苗字",'first_name':"名前"}
#メールアドレス変更フォーム
class EmailChangeForm(forms.ModelForm):
    class Meta():
        model = User
        fields = ('email',)
        labels = {'email':'メ-ルアドレス'}
#アイコン変更フォーム
class IconChangeForm(forms.ModelForm):
    class Meta():
        model = Account
        fields = ('account_image',)
        labels = {'account_image':"新しいアイコン"}
#パスワード変更
class PasswordChange(forms.ModelForm):
    class Meta():
        model = User
        fields = ('password',)
        labels = {'password':'新しいパスワード'}