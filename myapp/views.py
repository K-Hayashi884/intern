import operator

from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LogoutView,
    PasswordChangeDoneView,
    PasswordChangeView,
)
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.timezone import localtime
from django.views.generic import TemplateView

from .forms import IconChangeForm, PasswordChangeForm, UsernameChangeForm
from .models import CustomUser, Talk
from .serializers import CustomUserSerializer, TalkSerializer
from .utils import (
    create_room_path,
    get_display_message,
    get_display_time,
    process_message,
)


class IndexView(TemplateView):
    template_name = 'myapp/index.html'
    

# 小回りが効くようクラスベースは導入していない
@login_required
def friends(request):
    # ログインユーザーを取得し、検索から自分の友達を取得
    user = request.user
    friends = CustomUser.objects.exclude(id=user.id)
    info = create_message_dict(user, friends)
    params = {
        'info': info
    }
    return render(request, "myapp/friends.html", params)


# 小回りが効くようクラスベースは導入していない
@login_required
def talk_room(request, room_path):
    """ talkroomの関数
        共通でメッセージを表示
        post時メッセージをデータベースに保存 """
    user = request.user

    # pathからidを抽出
    member = [int(x) for x in room_path.split("-")]
    assert len(member) == 2, "Invalid Roomname"
    friend_id = member[0] if member[0] != user.id else member[1]
    friend = CustomUser.objects.get(id=friend_id)

    messages = (
        Talk.objects.select_related('talk_from', 'talk_to')
        .filter(Q(talk_from=user, talk_to=friend)| Q(talk_from=friend, talk_to=user))
        .order_by('pub_date')
    )
    
    # messageと表示時間が一体となったタプルを持つリストを制作
    message_list = []
    for message in messages:
        pro_message = process_message(message.content)
        jst_recorded_time = localtime(message.pub_date)
        display_time = f'{jst_recorded_time:%m/%d<br>%H:%M}'
        message_list.append((message, pro_message, display_time))

    params = {
        'user': user,
        'partner': friend,
        'message_list': message_list,
        'room_path': room_path,
    }
        
    return render(request, "myapp/talk_room.html", params)


class SettingView(LoginRequiredMixin, TemplateView):
    """ 設定用ページに移動 """
    template_name = "myapp/setting.html"


class PasswordChange(PasswordChangeView):
    """ パスワード変更ビュー """
    form_class = PasswordChangeForm
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
    error = ''
    if request.method == 'POST':
        user = UsernameChangeForm(request.POST, instance=obj)
        if user.is_valid():
            user.save()
            return redirect(to='edit_username_done')
        else:
            error = '既に同名のユーザーが存在します。'
    params = {
        'form':UsernameChangeForm(instance=obj),
        'error': error
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


def create_message_dict(user, friends):
    """
    それぞれの友達について最新メッセージと表示時間を取得し、
    リストに記録し、ルームIDを作成
    """
    info = []
    info_have_message = []
    info_heve_no_message = []
    for friend in friends:
        # 最新のメッセージの取得
        latest_message = (
            Talk.objects.select_related('talk_from', 'talk_to')
            .filter(
                Q(talk_from=user, talk_to=friend)
                | Q(talk_from=friend, talk_to=user)
            )
            .order_by('pub_date')
            .last()
        )
        # 表示情報の処理
        if latest_message:
            # 長すぎる文章のカット
            raw_message = latest_message.content
            latest_message.content = get_display_message(raw_message)
            # 表示したい時刻情報の決定 
            send_time = latest_message.pub_date
            jst_recorded_time = localtime(send_time)
            now = localtime(timezone.now())
            display_time, _ = get_display_time(now, send_time, jst_recorded_time)
        else:
            display_time = None
        
        room_path = create_room_path(user.id, friend.id) 

        # serialize
        serialize_friend = CustomUserSerializer(friend)
        serialize_message = TalkSerializer(latest_message)

        # 最新のメッセージと対応する相手をリストとしてinfoリストに格納
        if latest_message:
            info_have_message.append(
                [
                    serialize_friend.data,
                    serialize_message.data,
                    display_time,
                    room_path,
                    latest_message.pub_date
                ]
            )
        else:
            info_heve_no_message.append(
                [
                    serialize_friend.data,
                    serialize_message.data,
                    display_time,
                    room_path,
                    None
                ]
            )
    
    # 時間順に並べ替え
    info_have_message = sorted(info_have_message, key=operator.itemgetter(4), reverse=True)
    info.extend(info_have_message)
    info.extend(info_heve_no_message)
    return info







