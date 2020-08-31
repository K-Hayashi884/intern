from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import SignUpForm,LoginForm
from django.contrib import messages 

# Create your views here.
from .models import User,UserImage


def index(request):
    return render (request, "myapp/index.html")

def signup_view(request):
    if request.method == "GET":
        form = SignUpForm()
        params = {"form":form,}
        return render(request,"myapp/signup.html",params)
    elif request.method == "POST":
        form = SignUpForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            #フォームから'username'を読み取る
            username = form.cleaned_data.get('username')
            #フォームから'password1'を読み取る
            password = form.cleaned_data.get('password1')
            #フォームから'img'を読み取る
            image = form.cleaned_data.get('img')
            user = authenticate(username=username, password=password)
            login(request, user)
            user = User.objects.get(username=username)
            user_img = UserImage(
                user=user,
                image=image,
            )
            user_img.save()
            return redirect("/")
        params = {"form":form,}
        return render(request,"myapp/signup.html",params)
            
class Login(LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'myapp/login.html'

def friends(request):
    return render (request, "myapp/friends.html")

def talk_room(request):
    return render (request, "myapp/talk_room.html")

def setting(request):
    return render (request, "myapp/setting.html")
