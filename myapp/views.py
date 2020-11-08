from django.shortcuts import redirect, render
from django.http import HttpResponse
from .forms import SignupForm, LoginForm
from .models import Users
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User


def index(request):
    params = {
        'gotoLogin':'login_view',
        'gotoSignup':'signup_view',
    }
    return render(request, "myapp/index.html", params)

def signup_view(request):
    params = {
        'form' : SignupForm(),
    }
    if (request.method == 'POST'):
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
            return redirect(to='/')
        
    return render(request, "myapp/signup.html", params)



"""
ごり押しのやつ、qiitaでみたやつ作ってみる↑
def signup_view(request):
    params = {
        'form': SignupForm(),
    }
    if (request.method == 'POST'):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        img = request.POST['img']
        users = Users(username=username,email=email,password=password,img=img)
        users.save()
        #params['form'] = SignupForm(request.POST)
        return redirect(to='/')
    return render(request, "myapp/signup.html", params)
"""
"""
def login_view(request):
    params = {
        'form': LoginForm(),
    }
    if (request.method == 'POST'):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            user = User.objects.get(username=username)
            login(request, user)
            return redirect('/friends')
    return render(request, "myapp/login.html", params)
"""

"""
def login_view(request):
    params = {
        'form': LoginForm(),
    }
    if (request.method == 'POST'):

        #ここに分岐をつくる？データベース参照して存在したらリダイレクト
        #直接/talk_roomに来る輩も防がないとあかん
        return redirect(to='/talk_room')
    return render(request, "myapp/login.html", params)
"""


def friends(request):
    data = User.objects.all()
    params = {
        'data': data,
        'gotoFriends': 'friends',
        'gotoSetting': 'setting',
    }
    return render(request, "myapp/friends.html", params)

def talk_room(request):
    return render(request, "myapp/talk_room.html")

def setting(request):
    return render(request, "myapp/setting.html")
