from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, OuterRef, Subquery
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from .forms import (
    SignUpForm,
    LoginForm,
    TalkForm,
    FriendsSearchForm,
    MailSettingForm,
    ImageSettingForm,
    PasswordChangeForm,
    UserNameSettingForm,
)
from .models import User, Talk


def index(request):
    return render(request, "myapp/index.html")


def signup_view(request):
    if request.method == "GET":
        form = SignUpForm()
    elif request.method == "POST":
        """
        画像ファイルをformに入れた状態で使いたい時はformに"request.FILES"を加える。
        "request.POST"だけではNoneが入る。
        """
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            """
            モデルフォームはformの値をmodelsにそのまま格納できるsave()methodがあるので便利。
            """
            form.save()
            #フォームから"username"を読み取る
            username = form.cleaned_data.get("username")
            #フォームから"password1"を読み取る
            password = form.cleaned_data.get("password1")
            """
            認証情報のセットを検証するには authenticate() を利用してください。
            このメソッドは認証情報をキーワード引数として受け取ります。
            検証する対象はデフォルトでは username と password であり
            その組み合わせを個々の 認証バックエンド に対して問い合わせ、認証バックエンドで認証情報が有効とされれば 
            User オブジェクトを返します。もしいずれの認証バックエンドでも認証情報が有効と判定されなければ PermissionDenied が送出され、None が返されます。
            (公式ドキュメントより)
            つまり、autenticateメソッドは"username"と"password"を受け取り、その組み合わせが存在すれば
            そのUserを返し、不正であれば"None"を返します。
            """
            user = authenticate(username=username, password=password)
            if user is not None:
                """
                あるユーザーをログインさせる場合は、login() を利用してください。この関数は HttpRequest オブジェクトと User オブジェクトを受け取ります。
                ここでのUserは認証バックエンド属性を持ってる必要がある。
                authenticate()が返すUserはuser.backendを持つので連携可能。
                """
                login(request, user)
            return redirect("/")
    context = {"form": form, }
    return render(request, "myapp/signup.html", context)


class Login(LoginView):
    """
    ログインページ
    GETの時は指定されたformを指定したテンプレートに表示
    POSTの時はloginを試みる。→成功すればdettingのLOGIN_REDIRECT_URLで指定されたURLに飛ぶ
    """
    authentication_form = LoginForm
    template_name = "myapp/login.html"


class Logout(LoginRequiredMixin, LogoutView):
    """ログアウトページ"""
    pass


@login_required
def friends(request):
    user = request.user

    # 最新のトークも表示するVer 上級
    # ユーザーひとりずつの最新のトークを特定する
    latest_msg = Talk.objects.filter(
        Q(talk_from=OuterRef("pk"), talk_to=user) | Q(talk_from=user, talk_to=OuterRef("pk"))
    ).order_by("-time")

    friends = User.objects.exclude(id=user.id).annotate(
        latest_msg_pk=Subquery(
            latest_msg.values("pk")[:1]
        ),
        latest_msg_talk=Subquery(
            latest_msg.values("talk")[:1]
        ),
        latest_msg_time=Subquery(
            latest_msg.values("time")[:1]
        ),
    ).order_by("-latest_msg_pk")

    # 検索機能あり　上級
    form = FriendsSearchForm()
    
    if request.method == "GET" and "friends_search" in request.GET:
        form = FriendsSearchForm(request.GET)
        
        # 送信内容があった場合
        if form.is_valid():
            keyword = form.cleaned_data.get("keyword")
            # 何も入力せずに検索した時に全件を表示するようにするため、分岐しておく
            if keyword:
                # 入力に対して部分一致する友達を絞り込む
                friends = friends.filter(username__icontains=keyword)

                # 入力情報を保持してテキストボックスに残すようにする
                # （ユーザーが検索したキーワードを見られるように）
                request.session["keyword"] = request.GET

                # friendsに何らか情報があったとき
                context = {
                    "friends": friends,
                    "form": form,
                    # 検索結果を表示する画面にするために、そうであることを明示する変数を作る
                    "is_searched": True,
                }
                # friendsに情報がなかったとき
                # ＞検索結果がなかった
                if not friends:
                    context["no_result"] = True
                return render(request, "myapp/friends.html", context)

    # ここまで　検索機能あり　上級

    # POSTでない（リダイレクトorただの更新）& 検索欄に入力がない場合
    context = {
        "friends": friends,
        # 検索機能（上級）機能がなければcontextに入れない
        "form": form,
        # 最新トーク表示（上級）機能がなければcontextに入れない
        "friends": friends,
    }
    return render(request, "myapp/friends.html", context)


@login_required
def talk_room(request, user_id):
    # ユーザ・友達をともにオブジェクトで取得
    user = request.user
    try:
        friend = User.objects.get(id=user_id)
    except ObjectDoesNotExist:
        raise Http404
    # 自分→友達、友達→自分のトークを全て取得
    talk = Talk.objects.filter(Q(talk_from=user, talk_to=friend) | Q(talk_to=user, talk_from=friend))
    # 時系列で並べ直す
    talk = talk.order_by("time")
    # 送信form
    form = TalkForm()
    # メッセージ送信だろうが更新だろが、表示に必要なパラメーターは変わらないので、この時点でまとめて指定
    context = {
        "form": form,
        "talk": talk,
    }
    
    # POST（メッセージ送信あり）
    if request.method == "POST":
        # 送信内容を取得
        form = TalkForm(request.POST)

        # 送信内容があった場合
        if form.is_valid():
            # 送信内容からメッセージを取得
            text = form.cleaned_data.get("talk")
            # 送信者、受信者、メッセージ、タイムスタンプを割り当てて保存
            new_talk = Talk(talk=text, talk_from=user, talk_to=friend)
            new_talk.save()
            # 更新
            return render(request, "myapp/talk_room.html", context)
            
    # POSTでない（リダイレクトorただの更新）&POSTでも入力がない場合
    return render(request, "myapp/talk_room.html", context)


@login_required
def setting(request):
    return render(request, "myapp/setting.html")


# setting以下のchange系の関数は
# request.methodが"GET"か"POST"かで明示的に分けています。
# これはformの送信があった時とそうで無いときを区別しています。
@login_required
def user_img_change(request):
    user = request.user
    if request.method == "GET":
        # モデルフォームには(instance=user)をつけることで
        # userの情報が入った状態のFormを参照できます。
        # 今回はユーザ情報の変更の関数が多いのでこれをよく使います。
        form = ImageSettingForm(instance=user)

    elif request.method == "POST":
        form = ImageSettingForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return  redirect("user_img_change_done")
    context = {
        "form":form,
    }
    return render(request, "myapp/user_img_change.html", context)


@login_required
def user_img_change_done(request):
    return render(request, "myapp/user_img_change_done.html")


@login_required
def mail_change(request):
    user = request.user
    if request.method == "GET":
        form = MailSettingForm(instance=user)

    elif request.method == "POST":
        form = MailSettingForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return  redirect("mail_change_done")
    context = {
        "form":form,
    }
    return render(request,"myapp/mail_change.html",context)


@login_required
def mail_change_done(request):
    return render(request, "myapp/mail_change_done.html")


@login_required
def username_change(request):
    user = request.user
    if request.method == "GET":
        form = UserNameSettingForm(instance=user)

    elif request.method == "POST":
        form = UserNameSettingForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return  redirect("username_change_done")
    context = {
        "form":form,
    }
    return render(request, "myapp/username_change.html", context)


@login_required
def username_change_done(request):
    return render(request, "myapp/username_change_done.html")


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
    success_url = reverse_lazy("password_change_done")
    template_name = "myapp/password_change.html"


class PasswordChangeDone(PasswordChangeDoneView):
    """Django標準パスワード変更後ビュー"""
    template_name = "myapp/password_change_done.html"
