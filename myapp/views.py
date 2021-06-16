from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate
from django.views.generic import CreateView
from django.views.generic import View
from . forms import UserCreateForm
from . forms import LoginForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    return render(request, "myapp/signup.html")

def login_view(request):
    return render(request, "myapp/login.html")

@login_required
def friends(request):
    friends = User.objects.all()
    params = {
        "friends": friends,
    }
    return render(request, "myapp/friends.html", params)

def talk_room(request):
    return render(request, "myapp/talk_room.html")

def setting(request):
    return render(request, "myapp/setting.html")

def change_user(request):
    return render(request, "myapp/change_user.html")

def change_email(request):
    return render(request, "myapp/change_email.html")

def change_icon(request):
    return render(request, "myapp/change_icon.html")

def change_pass(request):
    return render(request, "myapp/change_pass.html")

def logout(request):
    return render(request, "myapp/logout.html")        

#アカウント作成
class Create_account(CreateView):
    def post(self, request, *args, **kwargs):
        form = UserCreateForm(data=request.POST)
        if form.is_valid():
            form.save()
            #フォームから'username'を読み取る
            username = form.cleaned_data.get('username')
            #フォームから'password1'を読み取る
            password = form.cleaned_data.get('password1')
            image = form.cleaned_data.get('image')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
        return render(request, 'myapp/signup.html', {'form': form,})

    def get(self, request, *args, **kwargs):
        form = UserCreateForm(request.POST)
        return  render(request, 'myapp/signup.html', {'form': form,})

signup_view = Create_account.as_view()

#ログイン機能
class Account_login(View):
    def post(self, request, *arg, **kwargs):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            user = User.objects.get(username=username)
            login(request, user)
            return redirect('/friends')
        return render(request, 'myapp/login.html', {'form': form,})

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        return render(request, 'myapp/login.html', {'form': form,})

login_view = Account_login.as_view()