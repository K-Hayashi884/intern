from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
#サインアップ
from .forms import SignupForm
#ログイン
from .forms import LoginForm
from django.contrib.auth import authenticate,login
#フレンド
from .models import CustomUser
#トークルーム
from .models import Message
from .forms import MessageForm
from django.db.models import Q
#settings
from django.contrib.auth import logout
from .forms import UsernameChangeForm
from .forms import UsermailChangeForm
from .forms import UsericonChangeForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView


def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    if(request.method =='POST'):
        form = SignupForm(request.POST, request.FILES) #POSTは大文字 noreverseerrorが出る 画像はrequest.FILES
        # バリデーションする
        if form.is_valid():
            form.save()
            return redirect(to = '/')
        else:
            return render(request, "myapp/signup.html", {"form": form,})
    else:
        form = SignupForm()
        return render(request, "myapp/signup.html", {"form": form,})

def login_view(request):
    if(request.method == 'POST'):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(to = '/friends')
        else:
            return render(request, "myapp/login.html", {"form": form,})
        
    else:
        form = LoginForm()
    return render(request, "myapp/login.html", {"form": form,})

def friends(request):
    data = CustomUser.objects.exclude(id=request.user.id)
    # requestuserとトーク履歴のあるユーザー
    list_w_talks = []
    # request.userとトーク履歴のないユーザー
    list_wo_talks = []
    for friend in data:
        latests = Message.objects.all().filter(Q(sender=request.user.id) | Q(receiver=request.user.id))\
            .filter(Q(sender=friend.id) | Q(receiver=friend.id)).order_by("-msg_date").first()
        if latests != None:
            list_w_talks.append([latests.msg_date, friend, latests])
        else:
            list_wo_talks.append([friend.created_date, friend])

    list_w_talks.sort(key=lambda x: x[0] ,reverse=True)
    list_wo_talks.sort(key=lambda x: x[0] ,reverse=True)
    params={
        'data': data,
        'list_w_talks':list_w_talks,
        'list_wo_talks':list_wo_talks,
    }
    return render(request, "myapp/friends.html", params)

def talk_room(request, num):
    friend = CustomUser.objects.get(id=num)
    msg_data = Message.objects.filter(Q(sender = request.user) | Q(receiver = request.user))\
        .filter(Q(sender = friend) | Q(receiver = friend)).order_by("msg_date")
    params = {
        'username': CustomUser.objects.get(id=num),
        'form': MessageForm(),
        'data': msg_data,
    }
    if (request.method == 'POST'):
        obj = Message(receiver=friend, sender=request.user)
        form = MessageForm(request.POST, instance=obj)
        form.save()
        return render(request, "myapp/talk_room.html", params)
    return render(request, "myapp/talk_room.html", params)

def setting(request):
    return render(request, "myapp/setting.html")

def change_username(request):
    myid = CustomUser.objects.get(id=request.user.id)
    form = UsernameChangeForm(data=request.POST, instance=myid)
    params={
            'form': form,
            'title': 'ユーザーネーム変更',
            'content': 'ユーザーネーム変更完了',
        }
    if(request.method == 'POST'):
        if form.is_valid():
            form.save()
            return render(request, "myapp/complete.html", params)
        else:
            return render(request, "myapp/change_username.html", params)
    return render(request, "myapp/change_username.html", params)

def change_mail(request):
    myid = CustomUser.objects.get(id=request.user.id)
    form = UsermailChangeForm(data=request.POST, instance=myid)
    params={
            'form': form,
            'title': 'メールアドレス変更',
            'content': 'メールアドレス変更完了',
        }
    if(request.method == 'POST'):
        if form.is_valid():
            form.save()
            return render(request, "myapp/complete.html", params)
        else:
            return render(request, "myapp/change_mail.html", params)
    return render(request, "myapp/change_mail.html", params)

def change_icon(request):
    myid = CustomUser.objects.get(id=request.user.id)
    form = UsericonChangeForm(request.POST, request.FILES, instance=myid) #request.POSTが必要
    params={
            'form': form,
            'title': 'アイコン変更',
            'content': 'アイコン変更完了',
        }
    if(request.method == 'POST'):
        if form.is_valid():
            form.save()
            return render(request, "myapp/complete.html", params)
        else:
            return render(request, "myapp/change_icon.html", params)
    return render(request, "myapp/change_icon.html", params)

class PasswordChange(LoginRequiredMixin, PasswordChangeView):
    success_url = reverse_lazy('setting/password_change_done')
    template_name = 'myapp/password_change.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = "password_change"
        return context

class PasswordChangeDone(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = 'myapp/password_change_done.html'

def complete(request):
    return render(request, "myapp/complete.html")

def logout_view(request):
    logout(request)
    return redirect(to = "/")