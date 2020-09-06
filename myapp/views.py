from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import User
# from django.contrib.auth import UserCreationForm
from .forms import SignUpForm


def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    params = {
        'form': SignUpForm(),
    }

    if (request.method == 'POST'):
        obj = User()
        user = SignUpForm(request.POST, instance=obj)
        if user.is_valid():
            user.save()
            params = {
                'form' : SignUpForm(request.POST),
            }
            return redirect(to='/')
    return render(request, "myapp/signup.html",params)

def login_view(request):
    return render(request, "myapp/login.html")

def friends(request):
    return render(request, "myapp/friends.html")

def talk_room(request):
    return render(request, "myapp/talk_room.html")

def setting(request):
    return render(request, "myapp/setting.html")
