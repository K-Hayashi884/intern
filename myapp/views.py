from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model

from .forms import SignupForm 

User=get_user_model()

def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):

    params={
        'form':SignupForm(),
    }

    if (request.method == 'POST'):
            obj = User()
            form = SignupForm(request.POST, request.FILES, instance=obj)
            if (form.is_valid()):
                form.save()
                return redirect(to='/')
            else:
                params['form'] = form

    return render(request, "myapp/signup.html",params)

def login_view(request):
    return render(request, "myapp/login.html")

def friends(request):
    return render(request, "myapp/friends.html")

def talk_room(request):
    return render(request, "myapp/talk_room.html")

def setting(request):
    return render(request, "myapp/setting.html")
