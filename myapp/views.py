from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
)
from django.db.models import Q
from django.shortcuts import get_object_or_404,redirect, render
from django.urls import reverse_lazy

from .forms import (
    
    SignUpForm,
    LoginForm,
    TalkForm,
    UserNameChangeForm,
    MailChangeForm,
    ImageChangeForm,
    PasswordChangeForm,
)
from .models import Talk

User = get_user_model()


def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    if request.method == "GET":
        form = SignUpForm()
    elif request.method =="POST":
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("/")
    context = {
        "form": form,
    }
    return render(request, "myapp/signup.html", context)

class Login(LoginView):
    """ログインページ
    GETの時は指定されたformを指定したテンプレートに表示
    POSTの時はloginを試みる。→成功すればdettingのLOGIN_REDIRECT_URLで指定されたURLに飛ぶ
    """

    authentication_form = LoginForm
    template_name = "myapp/login.html"

class Logout(LoginRequiredMixin, LogoutView):
    """ログアウトページ"""


@login_required
def friends(request):
    user = request.user

    friends = (
        User.objects.exclude(id=user.id)
    )
    context = {
        "friends": friends,
    }
    return render(request, "myapp/friends.html",context)


@login_required
def talk_room(request, user_id):
    user = request.user
    friend = get_object_or_404(User, id=user_id)

    
    talk = Talk.objects.filter(
        Q(talk_from=user, talk_to=friend) | Q(talk_to=user, talk_from=friend)
    ).order_by("time")

    form = TalkForm()

    # メッセージ送信だろうが更新だろが、表示に必要なパラメーターは変わらないので、この時点でまとめて指定
    context = {
        "form": form,
        "talk": talk,
        "name": friend.username,
    }

    # POST（メッセージ送信あり）
    if request.method == "POST":
        # 送信内容を取得
        new_talk = Talk(talk_from=user, talk_to=friend)
        form = TalkForm(request.POST, instance=new_talk)

        # 送信内容があった場合
        if form.is_valid():
            # 保存
            form.save()
            # 更新
            return redirect("talk_room", user_id)

    # POSTでない（リダイレクトorただの更新）&POSTでも入力がない場合
    return render(request, "myapp/talk_room.html", context)




@login_required
def setting(request):
    return render(request, "myapp/setting.html")


@login_required
def username_change(request):
    user = request.user
    if request.method == "GET":
        form = UserNameChangeForm(instance=user)

    if request.method =="POST":
        form = UserNameChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("username_change_done")
    context = {
        "form": form,
    }
    return render(request, "myapp/username_change.html", context)

@login_required
def username_change_done(request):
    return render(request, "myapp/username_change_done.html")

@login_required
def mail_change(request):
    user = request.user
    if request.method == "GET":
        form = MailChangeForm(instance=user)

    if request.method =="POST":
        form = MailChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("mail_change_done")
    context = {
        "form": form,
    }
    return render(request, "myapp/mail_change.html", context)

@login_required
def mail_change_done(request):
    return render(request, "myapp/mail_change_done.html")


@login_required
def image_change(request):
    user = request.user
    if request.method == "GET":
        form = ImageChangeForm(instance=user)
    
    elif request.method == "POST":
        form = ImageChangeForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("image_change_done")

    context = {
        "form": form,
    }
    return render(request, "myapp/image_change.html", context)

@login_required
def image_change_done(request):
    return render(request, "myapp/image_change_done.html")


class PasswordChange(PasswordChangeView):
    """Django標準パスワード変更ビュー
    Attributes:
        template_name: 表示するテンプレート
        success_url: 処理が成功した時のリダイレクト先
        form_class: パスワード変更フォーム
    """

    form_class = PasswordChangeForm
    success_url = reverse_lazy("password_change_done")
    template_name = "myapp/password_change.html"


def password_change_done(request):
    return render(request, "myapp/password_change_done.html")
