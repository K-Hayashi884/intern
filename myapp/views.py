from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login
from .forms import SignupForm
from .forms import LoginForm
from .models import CustomUser

def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    if(request.method =='POST'):
        form = SignupForm(request.POST, request.FILES) #POSTは大文字 noreverseerrorが出る 画像はrequest.FILES
        # バリデーションする
        if form.is_valid():
            form.save()
            return redirect(to = '/')
        else:
            return render(request, "myapp/signup.html", {"form": form})
    else:
        form = SignupForm()
        return render(request, "myapp/signup.html", {"form": form})

def login_view(request):
    if(request.method == 'POST'):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(to = '/friends')
        else:
            return render(request, "myapp/login.html", {"form": form,})
        
    else:
        form = LoginForm()
    return render(request, "myapp/login.html", {"form": form,})

def friends(request):
    data = CustomUser.objects.all()
    return render(request, "myapp/friends.html", {'data': data})

def talk_room(request, num):
    obj = CustomUser.objects.get(id=num)
    return render(request, "myapp/talk_room.html")

def setting(request):
    return render(request, "myapp/setting.html")
