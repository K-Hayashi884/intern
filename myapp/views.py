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

# 復習がしたいと思いクラスと関数が入り乱れています。ご了承ください。

def index(request):
    return render(request, "myapp/index.html")
    
class Signup_View(TemplateView):
    """ 登録用のクラス
        __init__() : 初期値設定、初期化
        get() : GET送信時の関数、フォームをレンダリング
        post() : POST送信時の関数、フォームのチェック、保存をする　"""

    def __init__(self):
        self.params = {
            'error_display': False, 
            'signup_form': SignupForm(),
        }

    def get(self, request):
        self.params['signup_form'] = SignupForm()
        self.params['error_display'] = False
        return render(request, 'myapp/signup.html', self.params)

    def post(self, request):
        self.params['signup_form'] = SignupForm(request.POST, request.FILES)
        # フォームのバリデーションチェック
        if self.params['signup_form'].is_valid():
            self.params['signup_form'].save()
            # indexにリダイレクト
            return redirect(to='index')
        else:
            # エラー表示
            self.params['error_display'] = True
            print(self.params['signup_form'].errors)
            

        return render(request, 'myapp/signup.html', self.params)


class Login_View(LoginView):
    """ LoginViewを使用したログインフォームビュー　"""
    form_class = LoginForm
    template_name = 'myapp/login.html'

@login_required(login_url='/login')
def friends(request):
    user = request.user
    friends = CustomUser.objects.exclude(id=user.id)
    carams = {
        'friends':friends
    }

    return render(request, "myapp/friends.html", carams)

@login_required(login_url='/login')
def talk_room(request, id):
    user = request.user
    friend = CustomUser.objects.get(id=id)
    member = [user, friend]
    # talkroomの取得
    talkroom_A = Talk.objects.filter(talk_from=user)\
        .filter(talk_to=friend)
    talkroom_B = Talk.objects.filter(talk_from=friend)\
        .filter(talk_to=user)
    if talkroom_A == None:
        create_talkroom(user, friend)
    if talkroom_B ==None:
        create_talkroom(friend, user)

    if request.method == 'POST':
        talk = Talk(talk_from=user, talk_to=friend, \
            content=request.POST['content'])
        talk.save()

    messages = Talk.objects.filter(Q(talk_from=user, talk_to=friend)| \
        Q(talk_from=friend, talk_to=user)).order_by('pub_date')
    
    params = {
        'partner': friend.username,
        'messages': messages,
        'id': id,
        'form': TalkContentForm()
    }
        
    return render(request, "myapp/talk_room.html", params)

@login_required(login_url='/login')
def setting(request):
    """ 設定用ページに移動 """
    return render(request, "myapp/setting.html")


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

@login_required(login_url='/login')
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

@login_required(login_url='/login')
def edit_username_done(request):
    """ username変更完了 """
    params = {
        'edit_obj': 'ユーザー名'
    }
    return render(request, 'myapp/done.html', params)

@login_required(login_url='/login')
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

@login_required(login_url='/login')
def edit_email_done(request):
    """ email変更完了 """
    carams = {
        'edit_obj': 'メールアドレス'
    }
    return render(request, 'myapp/done.html', carams)

@login_required(login_url='/login')
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

@login_required(login_url='/login')
def edit_icon_done(request):
    """ icon変更完了 """
    carams = {
        'edit_obj': 'アイコン'
    }
    return render(request, 'myapp/done.html', carams)


def create_talkroom(talk_from, talk_to):
    talk = Talk(talk_from=talk_from, talk_to=talk_to)
    talk.save()








