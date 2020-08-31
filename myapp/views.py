from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login
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
        
def login_view(request):
    if request.method == "GET":
        form = LoginForm()
        params = {"form":form}
        return render (request, "myapp/login.html",params)
    elif request.method == "POST":
        form = LoginForm(request.POST)
        username = request.POST['username'] 
        password = request.POST['password'] 
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("/") 
        else: 
            messages.error(request,'username or password not correct') 
            params = {"form":form}
            return render(request,"myapp/login.html",params)

def friends(request):
    user = request.user
    # usernameの重複は許されていないので、usernameだけで一意に定まる
    friends = User.objects.exclude(username=user.username)
    # user_img = UserImage.objects.get(user=user)
    user_img = UserImage.objects.all()
    params = {
        "user": user,
        "user_img": user_img,
        "friends": friends,
    }
    return render (request, "myapp/friends.html", params)

def talk_room(request,friend_username):
    user = request.user
    friend = User.objects.get(username=friend_username)
    params = {
        "user": user,
        "friend": friend, 
    }
    return render (request, "myapp/talk_room.html", params)

def setting(request):
    return render (request, "myapp/setting.html")
