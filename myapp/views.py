from django.shortcuts import redirect, render
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
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
        user_form=SignUpForm(request.POST,request.FILES)
        if user_form.is_valid():
            user_form.save()
            username=user_form.cleaned_data.get("username")
            password=user_form.cleaned_data.get("password1")
            new_user=authenticate(username=username,password=password)
            if new_user is not None:
                login(request,new_user)
                return redirect('friends')
    else:
        user_form=SignUpForm()
    params={
        'user_form':user_form,
    }
    return render(request, "myapp/signup.html",params)

def login_view(request):
    if request.method=='POST':
        form=LoginForm(request.POST)
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        if user is not None:
            if user.is_active:
                login(request,user)
                return redirect('friends')
        else:
            pass
    else:
        form=LoginForm()
    return render(request, "myapp/login.html",{'form':form})

@login_required
def friends(request):
    user=request.user
    data = Profile.objects.exclude(id=user.id)
    params = {
        'user':user,
        'data':data,
    }
    return render(request, "myapp/friends.html",params)

def talk_room(request):
    return render(request, "myapp/talk_room.html")

def setting(request):
    return render(request, "myapp/setting.html")

@login_required
def Logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('Login'))
