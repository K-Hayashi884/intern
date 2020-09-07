from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import User
from .forms import SignUpForm
from django.urls import reverse_lazy


def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    params = {
        'form': SignUpForm(),
    }

    if (request.method == 'POST'):
        obj = User()
        form = SignUpForm(request.POST,request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            image = form.cleaned_data.get('img')
            user = User.objects.get(username=username)
            return redirect(to='/')
        params = {'form': form}
    return render(request, "myapp/signup.html",params)

def login_view(request):
    return render(request, "myapp/login.html")

def friends(request):
    return render(request, "myapp/friends.html")

def talk_room(request):
    return render(request, "myapp/talk_room.html")

def setting(request):
    return render(request, "myapp/setting.html")
