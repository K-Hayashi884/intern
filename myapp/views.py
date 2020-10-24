from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from .models import User, Message
from .forms import SignUpForm, LoginForm, FindForm, MessageForm, EmailChangeForm, UsernameChangeForm, IconChangeForm
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    params = {
        'form': SignUpForm(),
    }

    if (request.method == 'POST'):
        obj = User()
        form = SignUpForm(request.POST,request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            image = form.cleaned_data.get('img')
            user = User.objects.get(username=username)
            return redirect(to='/')
        params = {'form': form}
    return render(request, "myapp/signup.html",params)

class Login(LoginView):
    form_class = LoginForm
    template_name = 'myapp/login.html'

def confirm_email(request):
    params = {'title': '登録'}
    if request.method=='POST':
        return redirect(to='/accounts/confirm-email')
    return render(request, "myapp/confirm-email.html", params)

unread_message_num = {}
@login_required(login_url='/')
def friends(request, num=1):
    me = request.user

    sorted_msgs = []
    latest_msgs = []
    no_log_friends = []
    log_exist_friends = []
    global unread_message_num
    # unread_message_num = {}
    # global all_unread_message
    # all_unread_message = 0
    # 検索機能----
    if request.method == 'POST':
        form = FindForm(request.POST)
        find = request.POST.get('find')
        users = User.objects.filter(username__icontains=find, is_superuser=False).exclude(username=me).order_by('date_joined')
    else:
        form = FindForm()
        users = User.objects.filter(is_superuser=False).exclude(username=me).order_by('date_joined')
        # ----
        # トーク履歴を表示
    num = 0
    for friend in users:
        # 相手と自分のトーク履歴を時系列に並べたものをリストに追加(sorted_msgs：相手ごとに時系列に並べた全履歴のリスト)
        sorted_msgs.append(Message.objects.all().filter(Q(send_to=me, send_from=friend)| Q(send_to=friend, send_from=me)).reverse())
        # 相手と自分のトーク履歴だけを取り出す
        sorted_msg = sorted_msgs[num]
        num += 1

        if len(sorted_msg) != 0:
        # 相手と自分のトーク履歴を最新のトーク履歴リストに入れる(latest_msgs:それぞれの友達との最新のトーク履歴だけを集めたリスト)
            latest_msgs.append(sorted_msg[0])
            log_exist_friends.append(friend)
            unread_message_num[friend.username] = sorted_msg.filter(is_read=False, send_from=friend).count()
            # all_unread_message += int(unread_message_num[friend.username])
        else:
            no_log_friends.append(friend)

    all_friends = log_exist_friends + no_log_friends
    page_obj = paginate_query(request, all_friends, 10)

    params = {
        'me': me,
        'form': form,
        'latest_msgs': latest_msgs,
        'page_obj': page_obj,
        'unread_message_num': unread_message_num,
    }
    return render(request, "myapp/friends.html", params)

@login_required(login_url='/')
def talk_room(request, name):
    me = User.objects.get(id=request.user.id)
    friend = User.objects.get(username=name)
    # トーク履歴を時系列に並べてリストに入れる
    message_log = Message.objects.filter(Q(send_to=me, send_from=friend)| Q(send_to=friend, send_from=me)).order_by('posted_date')
    form = MessageForm()

    unread_messages = list(message_log.filter(is_read=False, send_to=me))
    for change_to_read in unread_messages:
        change_to_read.is_read = True
        change_to_read.save()

    if request.method=='POST':
        posted_msg = request.POST['message']
        message = Message(send_to=friend, send_from=me, message=posted_msg)
        message.save()

    params = {
        'name': friend.username,
        'friend': friend,
        'message_log': message_log,
        'me': me,
        'form': form,
        'room_name': name,
    }

    return render(request, "myapp/talk_room.html", params)

@login_required(login_url='/')
def setting(request):
    return render(request, "myapp/setting.html")

@login_required(login_url='/')
def change_username(request):
    form = UsernameChangeForm()

    if request.method=='POST':
        user = request.user
        form = UsernameChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect(to='/setting/username/done')
    params = {
        'title': 'ユーザ名変更',
        'me': request.user,
        'change_what': 'ユーザ名',
        'form': form,
        'change': 'change_username',
    }
    return render(request, "myapp/change.html", params)

@login_required(login_url='/')
def change_username_done(request):
    return render(request, "myapp/change_done.html", {'title': 'ユーザ名変更'})

@login_required(login_url='/')
def change_email(request):
    form = EmailChangeForm()

    if request.method=='POST':
        user = request.user
        form = EmailChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()

            return redirect(to='/setting/email/done')
    params = {
        'title': 'メールアドレス変更',
        'me': request.user,
        'change_what': 'メールアドレス',
        'form':form,
        'change': 'change_email',
    }
    return render(request, "myapp/change.html", params)

@login_required(login_url='/')
def change_email_done(request):
    return render(request, "myapp/change_done.html", {'title': 'メールアドレス変更'})

@login_required(login_url='/')
def change_icon(request):
    form = IconChangeForm()

    if request.method=='POST':
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        form = IconChangeForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user.img = form.cleaned_data.get('img')
            user.save()
            return redirect(to='/setting/icon/done')
    params = {
        'form': form,
        'me': request.user,
    }

    return render(request, "myapp/change_icon.html", params)

@login_required(login_url='/')
def change_icon_done(request):
    return render(request, "myapp/change_done.html", {'title': 'アイコン変更'})

class PasswordChange(LoginRequiredMixin, PasswordChangeView):
    template_name = 'myapp/password_change.html'
    success_url = '/setting/password/done'

class PasswordChangeDone(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = 'myapp/change_done.html'

def paginate_query(request, queryset, count):
    paginator = Paginator(queryset, count)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return page_obj

def my_context_processor(request: HttpRequest):
    all_unread_message = 0
    for item in unread_message_num.values():
        all_unread_message += int(item)
    return {'all_unread_message': all_unread_message }
