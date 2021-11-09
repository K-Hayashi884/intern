from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm

def index(request):
    params={
        'goto_signup':'signup_view',
        'goto_login':'login_view',
    }
    return render(request, "myapp/index.html",params)

def signup_view(request):
    if request.method=="POST":
        form=SignUpForm(request.POST)
        if form.is_valid:
            usename=form.cleaned_data.get("username")
            password=form.cleaned_data.get("password1")
            form.save()
            new_user=authenticate(username=username,password=password)
            if new_user is not None:
                login(request,new_user)
                redirect('index')
    form=SignUpForm()
    return render(request, "myapp/signup.html",{'form':form})

def login_view(request):
    return render(request, "myapp/login.html")

def friends(request):
    return render(request, "myapp/friends.html")

def talk_room(request):
    return render(request, "myapp/talk_room.html")

def setting(request):
    return render(request, "myapp/setting.html")
