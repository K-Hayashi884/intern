from django.shortcuts import redirect, render
from django.contrib.auth import get_user
from django.contrib.auth import authenticate,login
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import SignUpForm,LoginForm,TalkForm
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
import datetime

# Create your views here.
from .models import UserImage,Talk


def index(request):
    return render (request, "myapp/index.html")

def signup_view(request):
    if request.method == "GET":
        form = SignUpForm()
        params = {"form":form,}
        return render(request,"myapp/signup.html",params)
    elif request.method == "POST":
        form = SignUpForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            #フォームから'username'を読み取る
            username = form.cleaned_data.get('username')
            #フォームから'password1'を読み取る
            password = form.cleaned_data.get('password1')
            #フォームから'img'を読み取る
            image = form.cleaned_data.get('img')
            user = authenticate(username=username, password=password)
            login(request, user)
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
    """ログインページ"""
    form_class = LoginForm
    template_name = 'myapp/login.html'

def friends(request):
    user = request.user
    # usernameの重複は許されていないので、usernameだけで一意に定まる
    friends = User.objects.exclude(username=user.username)
    # とりあえずすべてのユーザーアイコンを持っていく
    # ＞html内の組み込みにて、各ユーザーの該当するアイコンを表示することにする
    user_img = UserImage.objects.all()
    params = {
        "user": user,
        "user_img": user_img,
        "friends": friends,
    }
    return render (request, "myapp/friends.html", params)

def talk_room(request,friend_username):
    # ユーザ・友達をともにオブジェクトで取得
    user = get_user(request)
    friend = User.objects.get(username=friend_username)
    # 自分→友達、友達→自分のトークを全て取得
    talk = Talk.objects.filter(Q(talk_from=user, talk_to=friend) | Q(talk_to=user, talk_from=friend))
    # 時系列で並べ直す
    talk = talk.order_by('time')
    # 送信form
    form = TalkForm()
    # メッセージ送信だろうが更新だろが、表示に必要なパラメーターは変わらないので、この時点でまとめて指定
    params = {
        "form": form,
        "user": user,
        "friend": friend, 
        "talk": talk,
        "is_talk_room": True,
    }
    
    # POST（メッセージ送信あり）
    if request.method == "POST":
        # 送信内容を取得
        post = TalkForm(request.POST)

        # 送信内容があった場合
        if post.is_valid():
            # 送信内容からメッセージを取得
            text = post.cleaned_data.get('talk')
            now = datetime.datetime.now()
            # 送信者、受信者、メッセージ、タイムスタンプを割り当てて保存
            new_talk = Talk(talk=text, talk_from=user, talk_to=friend, time=now)
            new_talk.save()
            # 更新
            return render(request,"myapp/talk_room.html",params)

        # 送信内容がなかった場合（ただの更新と同じ）
        return render(request,"myapp/talk_room.html",params)
    
    # POSTでない（リダイレクトorただの更新）
    else:      
        return render(request,"myapp/talk_room.html",params)

def setting(request):
    return render (request, "myapp/setting.html")
