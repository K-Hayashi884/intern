from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.db.models import Q
from django.views.generic import TemplateView
from .forms import SignupForm, LoginForm, PasswordChange_Form
from django.contrib.auth.views import \
    LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Talk
from .forms import UsernameChangeForm, EmailChangeForm, IconChangeForm, TalkContentForm

from django.utils.timezone import localtime
from django.utils import timezone


class IndexView(TemplateView):
    template_name = 'myapp/index.html'
    
class Signup_View(TemplateView):
    """ 登録用のクラス
        __init__() : 初期値設定、初期化
        get() : GET送信時の関数、フォームをレンダリング
        post() : POST送信時の関数、フォームのチェック、保存をする　"""

    def __init__(self):
        self.params = { 
            'signup_form': SignupForm(),
        }

    def get(self, request):
        self.params['signup_form'] = SignupForm()
        return render(request, 'myapp/signup.html', self.params)

    def post(self, request):
        self.params['signup_form'] = SignupForm(request.POST, request.FILES)
        # フォームのバリデーションチェック
        if self.params['signup_form'].is_valid():
            self.params['signup_form'].save()
            # indexにリダイレクト
            return redirect(to='index')
            

        return render(request, 'myapp/signup.html', self.params)


class Login_View(LoginView):
    """ LoginViewを使用したログインフォームビュー　"""
    form_class = LoginForm
    template_name = 'myapp/login.html'

@login_required
def friends(request):
    # ログインユーザーを取得し、検索から自分の友達を取得
    user = request.user
    friends = CustomUser.objects.exclude(id=user.id)

    # それぞれの友達について最新メッセージと表示時間を取得し、リストに記録
    info = []
    for friend in friends:
        # 最新のメッセージの取得
        latest_message = Talk.objects.select_related('talk_from', 'talk_to').\
            filter(Q(talk_from=user, talk_to=friend)| \
                    Q(talk_from=friend, talk_to=user)).order_by('pub_date').last()
        # 表示情報の処理
        if latest_message:
            # 長すぎる文章のカット
            if len(latest_message.content) > 35:
                latest_message.content = latest_message.content[:35] + '...'
            # 表示したい時刻情報の決定    
            jst_recorded_time = localtime(latest_message.pub_date)
            now = localtime(timezone.now())
            if jst_recorded_time.date() == now.date():
                display_time = f'{jst_recorded_time:%H:%M}'
            elif jst_recorded_time.year == now.year:
                display_time = f'{jst_recorded_time:%m/%d}'
            else:
                display_time = f'{jst_recorded_time:%m/%d/%Y}'
        else:
            display_time = None
        
        room_path = create_room_path(user, friend)


        # 最新のメッセージと対応する相手をタプルとしてリストに格納
        info.append((friend, latest_message, display_time, room_path))

    
    
    carams = {
        'info': info
    }

    return render(request, "myapp/friends.html", carams)

@login_required
def talk_room(request, room_path):
    """ talkroomの関数
        共通でメッセージを表示
        post時メッセージをデータベースに保存 """
    user = request.user

    # pathからidを抽出
    friend_id = int(room_path.replace(str(user.id), '', 1).replace('-', ''))
    friend = CustomUser.objects.get(id=friend_id)

    # postで送られてくるメッセージはデータベースに保存
    #if request.method == 'POST':
    #    talk = Talk(talk_from=user, talk_to=friend, \
    #        content=request.POST['content'])
    #    talk.save()

    messages = Talk.objects.select_related('talk_from', 'talk_to').filter(Q(talk_from=user, talk_to=friend)| \
        Q(talk_from=friend, talk_to=user)).order_by('pub_date')
    
    # messageと表示時間が一体となったタプルを持つリストを制作
    message_list = []
    for message in messages:
        jst_recorded_time = localtime(message.pub_date)
        display_time = f'{jst_recorded_time:%m/%d<br>%H:%M}'
        message_list.append((message, display_time))

    params = {
        'user': user,
        'partner': friend,
        'message_list': message_list,
        'room_path': room_path,
        'form': TalkContentForm()
    }
        
    return render(request, "myapp/talk_room.html", params)

class SettingView(LoginRequiredMixin, TemplateView):
    """ 設定用ページに移動 """
    template_name = "myapp/setting.html"


class PasswordChange(PasswordChangeView):
    """ パスワード変更ビュー """
    form_class = PasswordChange_Form
    success_url = reverse_lazy('pass_change_done')
    template_name = 'myapp/pass_change.html'


class PasswordChangeDone(PasswordChangeDoneView):
    """ パスワード変更完了 """
    template_name = 'myapp/pass_change_done.html'

class Logout(LoginRequiredMixin, LogoutView):
    """ ログアウトビュー """
    pass

@login_required
def edit_username(request):
    """ username変更ビュー """
    obj = request.user
    if request.method == 'POST':
        user = UsernameChangeForm(request.POST, instance=obj)
        if user.is_valid():
            user.save()
            return redirect(to='edit_username_done')

    params = {
        'form':UsernameChangeForm(instance=obj)
    }
    return render(request, 'myapp/edit_username.html', params)

@login_required
def edit_username_done(request):
    """ username変更完了 """
    params = {
        'edit_obj': 'ユーザー名'
    }
    return render(request, 'myapp/done.html', params)

@login_required
def edit_email(request):
    """ email変更ビュー """
    obj = request.user
    if request.method == 'POST':
        user = EmailChangeForm(request.POST, instance=obj)
        if user.is_valid():
            user.save()
            return redirect(to='edit_email_done')

    params = {
        'form':EmailChangeForm(instance=obj)
    }
    return render(request, 'myapp/edit_email.html', params)

@login_required
def edit_email_done(request):
    """ email変更完了 """
    carams = {
        'edit_obj': 'メールアドレス'
    }
    return render(request, 'myapp/done.html', carams)

@login_required
def edit_icon(request):
    """ icon変更ビュー """
    obj = request.user
    if request.method == 'POST':
        user = IconChangeForm(request.POST, request.FILES, instance=obj)
        if user.is_valid():
            user.save()
            return redirect(to='edit_icon_done')

    params = {
        'form':IconChangeForm(instance=obj)
    }
    return render(request, 'myapp/edit_icon.html', params)

@login_required
def edit_icon_done(request):
    """ icon変更完了 """
    carams = {
        'edit_obj': 'アイコン'
    }
    return render(request, 'myapp/done.html', carams)


def create_room_path(user1, user2):
    """userを渡すと一意のroom_pathを生成する関数"""
    user1_id = str(user1.id)
    user2_id = str(user2.id)
    
    num_list = sorted([user1_id, user2_id])
    room_path = '-'.join(num_list)

    return room_path








