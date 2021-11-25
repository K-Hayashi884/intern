from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView
from .forms import signup_form, LoginForm
from .models import CustomUser

def index(request):
    return render(request, "myapp/index.html")


def signup_view(request):
    msg = '必要事項を入力してください'
    if request.method == 'POST':
        obj = CustomUser()
        form = signup_form(request.POST,request.FILES,instance=obj)
        if form.is_valid():
            form.save()
            return redirect(to='/')
        else:
            msg = '不正な入力'
    params = {
        'form':signup_form(),
        'msg':msg,
    }
    return render(request,'myapp/signup.html',params)


class login_view(LoginView):
    authentication_form = LoginForm
    template_name ='myapp/login.html'

def friends(request):
    return render(request, "myapp/friends.html")

def talk_room(request):
    return render(request, "myapp/talk_room.html")

def setting(request):
    return render(request, "myapp/setting.html")
