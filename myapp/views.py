from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import User, Message
from .forms import SignUpForm, LoginForm, FindForm
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

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

@csrf_exempt
def friends(request):
    me = request.user
    sorted_msgs = []
    latest_msgs = []
    no_log_friends = []
    log_exist_friends = []
    # 検索機能----
    if request.method == 'POST':
        form = FindForm(request.POST)
        find = request.POST.get('find')
        users = User.objects.filter(username=find, is_superuser=False).exclude(username=me).order_by('date_joined')
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
        else:
            no_log_friends.append(friend)

    params = {
        'log_exist_friends': log_exist_friends,
        'no_log_friends': no_log_friends,
        'form': form,
        'latest_msgs': latest_msgs,
    }
    return render(request, "myapp/friends.html", params)

def talk_room(request, num):
    return render(request, "myapp/talk_room.html", {'id': num, 'user': User.objects.get(id=num)})

def setting(request):
    return render(request, "myapp/setting.html")
