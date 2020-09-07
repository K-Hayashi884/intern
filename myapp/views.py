from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
"""
Django標準のViewClass
"""
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
)
from django.contrib.auth import authenticate,login
from .forms import (
    SignUpForm,
    LoginForm,
    MailSettingForm,
    ImageSettingForm,
    PasswordChangeForm,
    UserNameSettingForm,
)
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from .models import User,UserImage


def index(request):
    return render (request, "myapp/index.html")

def signup_view(request):
    if request.method == "GET":
        form = SignUpForm()
        params = {"form":form,}
        return render(request,"myapp/signup.html",params)
    elif request.method == "POST":
        """
        画像ファイルをformに入れた状態で使いたい時はformに'request.FILES'を加える。
        'request.POST'だけではNoneが入る。
        """
        form = SignUpForm(request.POST,request.FILES)
        if form.is_valid():
            """
            モデルフォームはformの値をmodelsにそのまま格納できるsave()methodがあるので便利。
            """
            form.save()
            #フォームから'username'を読み取る
            username = form.cleaned_data.get('username')
            #フォームから'password1'を読み取る
            password = form.cleaned_data.get('password1')
            #フォームから'img'を読み取る
            image = form.cleaned_data.get('img')
            """
            認証情報のセットを検証するには authenticate() を利用してください。
            このメソッドは認証情報をキーワード引数として受け取ります。
            検証する対象はデフォルトでは username と password であり
            その組み合わせを個々の 認証バックエンド に対して問い合わせ、認証バックエンドで認証情報が有効とされれば 
            User オブジェクトを返します。もしいずれの認証バックエンドでも認証情報が有効と判定されなければ PermissionDenied が送出され、None が返されます。
            (公式ドキュメントより)
            つまり、autenticateメソッドは'username'と'password'を受け取り、その組み合わせが存在すれば
            そのUserを返し、不正であれば'None'を返します。
            """
            user = authenticate(username=username, password=password)
            if user is not None:
                """
                あるユーザーをログインさせる場合は、login() を利用してください。この関数は HttpRequest オブジェクトと User オブジェクトを受け取ります。
                ここでのUserは認証バックエンド属性を持ってる必要がある。
                authenticate()が返すUserはuser.backendを持つので連携可能。
                """
                login(request, user)
                """
                ここで先ほどのUserを使いたいところだがauteticate()が返すUserは<class 'django.contrib.auth.models.User'>で
                user_img.imageには入らない。ここにはインスタンスが入る。
                インスタンスとは?→'https://djangobrothers.com/blogs/basic_knowledge_of_python/'
                """
                user = User.objects.get(username=username)
                user_img = UserImage(
                    user=user,
                    image=image,
                )
                user_img.save()
            return redirect("/")
        params = {"form":form,}
        return render(request,"myapp/signup.html",params)

class Login(LoginView):
    """
    ログインページ
    GETの時は指定されたformを指定したテンプレートに表示
    POSTの時はloginを試みる。→成功すればdettingのLOGIN_REDIRECT_URLで指定されたURLに飛ぶ
    """
    authentication_form = LoginForm
    template_name = 'myapp/login.html'

class Logout(LoginRequiredMixin, LogoutView):
    """ログアウトページ"""
    template_name = 'myapp/login.html'

def friends(request):
    return render (request, "myapp/friends.html")

def talk_room(request):
    return render (request, "myapp/talk_room.html")

@login_required
def setting(request):
    return render (request, "myapp/setting.html")
"""
setting以下のchange系の関数は
request.methodが'GET'か'POST'かで明示的に分けています。
これはformの送信があった時とそうで無いときを区別しています
"""

@login_required
def user_img_change(request):
    user = request.user
    try:
        user_img = UserImage.objects.get(user=user)
    except ObjectDoesNotExist:
        user_img = UserImage.objects.none()
    if request.method == "GET":
        """
        モデルフォームには(instance=user)をつけることで
        userの情報が入った状態のFormを参照できます。
        今回はユーザ情報の変更の関数が多いのでこれをよく使います。
        """
        form = ImageSettingForm(instance=user)
        params = {
            "form":form,
            "user_img":user_img,
        }
        """
        画像に関しては、formに入った状態では表示できないので
        保存されたものを直接参照する必要があります。
        """
        return render(request,"myapp/user_img_change.html",params)
    elif request.method == "POST":
        form = ImageSettingForm(request.POST,request.FILES)
        if form.is_valid():
            user_img.image=form.cleaned_data.get('image')
            user_img.save()
            return user_img_change_done(request)
        params = {
            "form":form,
            "user_img":user_img,
        }
        return render(request,"myapp/user_img_change.html",params)

@login_required
def user_img_change_done(request):
    return render(request,"myapp/user_img_change_done.html")

@login_required
def mail_change(request):
    user = request.user
    if request.method == "GET":
        form = MailSettingForm(instance=user)
        params = {
            "form":form,
        }
        return render (request,"myapp/mail_change.html",params)
    elif request.method == "POST":
        form = MailSettingForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return mail_change_done(request)
        params = {
            "form":form,
        }
        return render(request,"myapp/mail_change.html",params)
@login_required
def mail_change_done(request):
    return render(request,"myapp/mail_change_done.html")

@login_required
def username_change(request):
    user = request.user
    if request.method == "GET":
        form = UserNameSettingForm(instance=user)
        params = {
            "form":form,
        }
        return render (request,"myapp/username_change.html",params)
    elif request.method == "POST":
        form = UserNameSettingForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return username_change_done(request)
        params = {
            "form":form,
        }
        return render(request,"myapp/mail_change.html",params)
@login_required
def username_change_done(request):
    """
    ユーザ名変更後の関数
    """
    return render(request,"myapp/username_change_done.html")

class PasswordChange(PasswordChangeView):
    """
    Django標準パスワード変更ビュー
    Attributes:
    ・template_name
    表示するテンプレート
    ・success_url
    処理が成功した時のリダイレクト先
    ・form_class
    パスワード変更フォーム
    """
    form_class = PasswordChangeForm
    success_url = reverse_lazy('password_change_done')
    template_name = 'myapp/password_change.html'

class PasswordChangeDone(PasswordChangeDoneView):
    """Django標準パスワード変更後ビュー"""
    template_name = 'myapp/password_change_done.html'