from django.shortcuts import redirect, render
from django.contrib import admin
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from .forms import LoginForm

def index(request):
    params={
        'goto_signup':'signup_view',
        'goto_login':'login_view',
    }
    return render(request, "myapp/index.html",params)

def signup_view(request):
    if request.method=="POST":
        form=SignUpForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get("username")
            password=form.cleaned_data.get("password1")
            new_user=authenticate(username=username,password=password)
            if new_user is not None:
                login(request,new_user)
                return redirect('index')
    else:
        form=SignUpForm()
    return render(request, "myapp/signup.html",{'form':form})

def login_view(request):
    if request.method=='POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            usename=form.cleaned_data.get("username")
            password=form.cleaned_data.get("password1")
            if new_user is not None:
                login(request,new_user)
                return HttpResponseRedirect(reverse('inquiry_apps:inquiry_list'))
            else:
                pass
    else:
        form=LoginForm()
    return render(request, "myapp/login.html",{'form':form})
def friends(request):
    return render(request, "myapp/friends.html")

def talk_room(request):
    return render(request, "myapp/talk_room.html")

def setting(request):
    return render(request, "myapp/setting.html")
