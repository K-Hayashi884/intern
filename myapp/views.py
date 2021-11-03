from django.shortcuts import redirect, render


def index(request):
    params={
        'goto_signup':'signup_view',
        'goto_login':'login_view',
    }
    return render(request, "myapp/index.html",params)

def signup_view(request):
    return render(request, "myapp/signup.html")

def login_view(request):
    return render(request, "myapp/login.html")

def friends(request):
    return render(request, "myapp/friends.html")

def talk_room(request):
    return render(request, "myapp/talk_room.html")

def setting(request):
    return render(request, "myapp/setting.html")
