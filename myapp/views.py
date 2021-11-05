from django.contrib.auth.forms import UserCreationForm
from django.db.models.fields import EmailField
from django.db.models.query import QuerySet
from django.shortcuts import redirect, render
from django import forms

from .models import CustomUser
# 会員登録
from .forms import SignupForm
# ログイン
from .forms import LoginForm
from django.contrib.auth import login, authenticate
# 友だち表示, トークルーム
from .models import Message
# トークルーム
from django.db.models import Q
from .forms import MessageForm
from django.utils import timezone
# 設定
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, LogoutView
from django.urls import reverse_lazy
from .forms import UserUpdateForm


def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    params = {
        'header_title':"会員登録",
        'title': "",
        'form': SignupForm(),
    }
    if request.method == 'POST':
        obj = CustomUser()
        form = SignupForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            return redirect(to='/')
        else:
            params['title'] = 'エラー'
            params['form'] = form
    return render(request, "myapp/signup.html", params)

def login_view(request):
    params = {
        'header_title':"ログイン",
        'title': '',
        "errormessage":"",
        'form': LoginForm(),
    }
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user = CustomUser.objects.get(username=username)
            login(request, user)
            return redirect(to="/friends")
        else:
            params["errormessage"] = "正しく入力されていません"
    return render(request, 'myapp/login.html', params)

def friends(request):
    data = CustomUser.objects.all()
    # request.userとトーク履歴のあるユーザー
    list_w_talks = []
    # request.userとトーク履歴のないユーザー
    list_wo_talks = []

    for friend in data:
        if friend.id == request.user.id:
            continue
        latests = Message.objects.all().filter(Q(sender=request.user.id) | Q(receiver=request.user.id))\
        .filter(Q(sender=friend.id) | Q(receiver=friend.id)).order_by("-sendtime").first()
        if latests != None:
            list_w_talks.append([latests.sendtime, friend, latests])
        else:
            list_wo_talks.append([friend.regtime, friend])

    list_w_talks.sort(key=lambda x: x[0], reverse=True)
    list_wo_talks.sort(key=lambda x: x[0],reverse=True)

    params = {
        "user":request.user.username,
        "header_title":"友だち",
        "title":"",
        "list_w_talks":list_w_talks,
        "list_wo_talks":list_wo_talks,
    }

    return render(request, "myapp/friends.html", params)

def talk_room(request, your_id):
    # 送る側のユーザー
    me = request.user
    # 受け取る側のユーザー
    you = CustomUser.objects.get(id = your_id)
    data = Message.objects.filter( Q(sender=me) | Q(receiver=me) ).filter( Q(sender=you) | Q(receiver=you) ).order_by("sendtime")
    params = {
        "sender":me,
        "receiver":you,
        "title":"",
        "form":MessageForm(),
        "data":data,
    }
    # ここから先　以下のコードの代わりにギター本のp.198でできないか？
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            newrecord = Message(
                sender = request.user,
                receiver = you,
                content = form.cleaned_data["content"],
            )
            newrecord.save()
    return render(request, "myapp/talk_room.html", params)

def setting(request):
    params = {
        "user":request.user,
        "header_title":"設定",
    }
    return render(request, "myapp/setting.html", params)

def change_setting(request, change_command, your_id):
    obj = CustomUser.objects.get(id=your_id)
    params = {
        "user":request.user,
        "header_title":"",
        "change_command":"",
        "isform":True,
        "form":UserUpdateForm(),
    }

    if change_command == "change_username":
        params["header_title"] = "ユーザ名変更"
    elif change_command == "change_email":
        params["header_title"] = "メールアドレス変更"
    elif change_command == "change_image":
        params["header_title"] = "アイコン変更"
    params["change_command"] = params["header_title"]

    if request.method == "POST":
        form = UserUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            print("フォームは有効です")
            if change_command == "change_username":
                obj.username = form.cleaned_data["username"]
            elif change_command == "change_email":
                obj.email = form.cleaned_data["email"]
            elif change_command == "change_image":
                obj.image = form.cleaned_data["image"]
            obj.save()
            params["isform"] = False
            return redirect(to="/change_setting_done/" + str(change_command))
        else:
            print("フォームは有効ではありません")
    return render(request, "myapp/change_setting.html", params)

def change_setting_done(request, change_command):
    params = {
        "change_command":"",
    }
    if change_command == "change_username":
        params["change_command"] = "ユーザ名の変更"
    elif change_command == "change_email":
        params["change_command"] = "Eメールアドレスの変更"
    elif change_command == "change_image":
        params["change_command"] = "アイコンの変更"
    return render(request, "myapp/change_setting_done.html", params)

class PasswordChange(LoginRequiredMixin, PasswordChangeView):
    """パスワード変更ビュー"""
    success_url = reverse_lazy('password_change_done')
    template_name = 'myapp/change_password.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # 継承元のメソッドCALL
        context["form_name"] = "password_change"
        return context

class PasswordChangeDone(LoginRequiredMixin,PasswordChangeDoneView):
    """パスワード変更完了"""
    template_name = 'myapp/change_password_done.html'

class Logout(LogoutView):
    success_url = reverse_lazy("index")