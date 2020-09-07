from django.shortcuts import redirect, render
from django.contrib.auth import get_user
from django.contrib.auth import authenticate,login
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import SignUpForm,LoginForm,TalkForm,FriendsSearchForm
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

    # 最新のトークも表示するVer　上級
    # 最新のトークを表示するためのオブジェクトを作成する
    talk_list = []
    # １．ユーザーひとりずつの最新のトークを特定する
    for friend in friends:
        # そのユーザーとのトークがない場合、objectがないためエラーが返ってくる
        # ＞その場合の分岐を作る
        try:
            # database上での条件に一致する最後の投稿→最新の投稿
            last_message = Talk.objects.filter(Q(talk_from=user, talk_to=friend) | Q(talk_to=user, talk_from=friend)).last()
            # 今日のトークであれば時刻を表示、それより前なら日付を表示
            # 表示に関してはhtml上の組み込みでのフォーマットで対応できるので、ここではflagのみを準備する
            if "{0:%Y-%m-%d}".format(last_message.time) == "{0:%Y-%m-%d}".format(datetime.date.today()):
                time_flag = "time"
            else:
                time_flag = "date"
            # htmlで表示するにあたって必要な情報を紐づけたリストを作成する
            talk_list.append([friend, last_message, time_flag, last_message.time])
        # トーク履歴がない場合、nullで登録する
        except:
            last_message = ''
            mes= ''
            time_flag = ''
            # htmlで表示するにあたって必要な情報を紐づけたリストを作成する

            # ※※時間のソートをかける際に、0やnullでは型が違ってsortできない
            # ＞databaseの初めのメッセージの時間を用いると、必ず降順の最後に置かれる
            talk_list.append([friend, last_message, time_flag, Talk.objects.all().first().time])

    # 最後の要素（＝そのトークのtime）でソートすることで、html上の組み込みでforを回すだけで最新から順に表示することができる
    talk_list = sorted(talk_list, reverse=True, key=lambda x: x[3])
    # 最新のトークも表示するVer　上級

    # 検索機能あり　上級
    form = FriendsSearchForm()
    
    # POST（メッセージ送信あり）
    if request.method == "POST":
        post = FriendsSearchForm(request.POST)
        
        # 送信内容があった場合
        if post.is_valid():
            keyword = post.cleaned_data.get('keyword')
            # 何も入力せずに検索した時に全件を表示するようにするため、分岐しておく
            if keyword != "":
                # 入力に対して部分一致する友達を絞り込む
                friends = friends.filter(username__icontains=keyword)

                # 入力情報を保持してテキストボックスに残すようにする
                # （ユーザーが検索したキーワードを見られるように）
                form = FriendsSearchForm(request.POST)
                request.session['keyword'] = request.POST

                # friendsに情報がなかったとき
                # ＞検索結果がなかった
                if len(friends) == 0:
                    params = {
                        "user": user,
                        "user_img": user_img,
                        "friends": friends,
                        "form": form,
                        "talk_list": talk_list,
                        # 検索結果を表示する画面にするために、そうであることを明示する変数を作る
                        "is_searched": True,
                        # 検索結果がなかったことを示す変数
                        "no_result": True,
                    }
                    return render (request, "myapp/friends.html", params)
                
                # friendsに何らか情報があったとき
                params = {
                    "user": user,
                    "user_img": user_img,
                    "friends": friends,
                    "form": form,
                    "talk_list": talk_list,
                    # 検索結果を表示する画面にするために、そうであることを明示する変数を作る
                    "is_searched": True,
                }
                return render (request, "myapp/friends.html", params)

    # ここまで　検索機能あり　上級

    # POSTでない（リダイレクトorただの更新）&POSTでも入力がない場合
    params = {
        "user": user,
        "user_img": user_img,
        "friends": friends,
        # 検索機能（上級）機能がなければparamsに入れない
        "form": form,
        # 最新トーク表示（上級）機能がなければparamsに入れない
        "talk_list": talk_list,
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
        # talkroomのときのみheaderの表示を変えたい
        # ＞そのページがtalkroomであることを伝えるための変数
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
            
    # POSTでない（リダイレクトorただの更新）&POSTでも入力がない場合
    return render(request,"myapp/talk_room.html",params)

    #     # 送信内容がなかった場合（ただの更新と同じ）
    #     return render(request,"myapp/talk_room.html",params)
    
    # # POSTでない（リダイレクトorただの更新）
    # else:      
    #     return render(request,"myapp/talk_room.html",params)

def setting(request):
    return render (request, "myapp/setting.html")
