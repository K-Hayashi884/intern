from django.shortcuts import redirect, render
from .forms import signup
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import member

def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    params = {
        'title':'会員登録',
        'form':signup(),
    }
    if (request.method=='POST'):
        username=request.POST['name']
        mail=request.POST['e_mail']
        password=request.POST['password']
        image=request.POST['img']
        mem=member(username=username,mail=mail,password=password,image=image)
        mem.save()
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
