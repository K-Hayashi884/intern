from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.db.models import Q
from django.views.generic import TemplateView
from .forms import PasswordChange_Form
from django.contrib.auth.views import \
     LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Talk
from .forms import UsernameChangeForm, IconChangeForm
from .serializers import CustomUserSerializer, TalkSerializer

from django.utils.timezone import localtime
from django.utils import timezone
import operator


class IndexView(TemplateView):
    template_name = 'myapp/index.html'
    

# 小回りが効くようクラスベースは導入していない
@login_required
def friends(request):
    # ログインユーザーを取得し、検索から自分の友達を取得
    user = request.user
    friends = CustomUser.objects.exclude(id=user.id)

    info = create_message_dict(user, friends)
    
    
    carams = {
        'info': info
    }

    return render(request, "myapp/friends.html", carams)

# 小回りが効くようクラスベースは導入していない
@login_required
def talk_room(request, room_path):
    """ talkroomの関数
        共通でメッセージを表示
        post時メッセージをデータベースに保存 """
    user = request.user

    # pathからidを抽出
    friend_id = int(room_path.replace(str(user.id), '', 1).replace('-', ''))
    friend = CustomUser.objects.get(id=friend_id)

    messages = Talk.objects.select_related('talk_from', 'talk_to').filter(Q(talk_from=user, talk_to=friend)| \
        Q(talk_from=friend, talk_to=user)).order_by('pub_date')
    
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

def create_room_path(user1, user2):
     # userを渡すと一意のroom_pathを生成する
    user1_id = int(user1.id)
    user2_id = int(user2.id)
    
    num_list = sorted([user1_id, user2_id])
    num_list = [str(num_list[0]), str(num_list[1])]
    room_path = '-'.join(num_list)

    return room_path


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
        latest_message = Talk.objects.select_related('talk_from', 'talk_to').\
            filter(Q(talk_from=user, talk_to=friend)| \
                    Q(talk_from=friend, talk_to=user)).order_by('pub_date').last()
        # 表示情報の処理
        if latest_message:
            # 長すぎる文章のカット
            cut_length = 25
            if len(latest_message.content) > cut_length:
                latest_message.content = latest_message.content[:cut_length] + '...'
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

        # serialize
        serialize_friend = CustomUserSerializer(friend)
        serialize_message = TalkSerializer(latest_message)

        # 最新のメッセージと対応する相手をリストとしてinfoリストに格納
        if latest_message:
            info_have_message.append([serialize_friend.data, serialize_message.data, display_time, room_path, latest_message.pub_date])
        else:
            info_heve_no_message.append([serialize_friend.data, serialize_message.data, display_time, room_path, None])
    
    # 時間順に並べ替え
    info_have_message = sorted(info_have_message, key=operator.itemgetter(4), reverse=True)
    info.extend(info_have_message)
    info.extend(info_heve_no_message)
    return info

def process_message(message):
        """ 長いメッセージに改行処理 """
        letter_oneline = 20
        processed_message = ''
        message = message.replace('<br>', '').replace('\n', '')
        while message:
            if len(message) <= letter_oneline:
                processed_message += message
                message = False
            else:
                processed_message += message[:letter_oneline] + '<br>'
                message = message[letter_oneline:]
        
        return processed_message







