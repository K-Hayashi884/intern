from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import login, authenticate
from .forms import UserForm,LoginForm
from .models import User
from django.contrib import messages


def index(request):
    params = {
        'title': 'DeMiAインターン'
    }
    return render(request, "myapp/index.html", params)

def signup_view(request):
    if request.method == 'POST':
        #print("hello")
        form = UserForm(request.POST)
        if form.is_valid():
            #print("hello2")
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
        else:
            print(form.errors)
    else:
        form = UserForm()
    return render(request, 'myapp/signup.html', {'form': form})
    # if (request.method == 'POST'):
    #     obj = User()
    #     user = UserForm(request.POST, instance=obj)
        
    #     user.save()
    #     return redirect(to='/')
    # params = {
    #     'form': UserForm(),
    #     'err_msg': '',
    # }
    # return render(request, "myapp/signup.html", params)

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            user = User.objects.get(username=username)
            if user is not None:
                # print("ok")
                login(request, user)
                return redirect('/friends')
            else:
                # print("no match")
                params = {
                    'form': form,
                    'err_msg': "ユーザー名またはパスワードが間違っています。"
                }
                return render(request, "myapp/login.html", params)
        else:
            form = LoginForm(request.POST)
            # print("no valid")
            params = {
                'form': form,
                'err_msg': "ユーザー名またはパスワードが間違っています。"
            }
            return render(request, "myapp/login.html", params)
    else:
        form = LoginForm()
        return render(request, "myapp/login.html", {'form': form,})

def friends(request):
    return render(request, "myapp/friends.html")

def talk_room(request):
    return render(request, "myapp/talk_room.html")

def setting(request):
    return render(request, "myapp/setting.html")
