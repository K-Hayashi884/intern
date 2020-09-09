from django.shortcuts import redirect, render
from .models import User
from .forms import UserForm


def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    params =  {
        'error_msg':'',
        'form':UserForm(),
    }
    if (request.method == 'POST'):
        if (request.POST['Password'] != request.POST['PasswordConfirmation']):
            params['error_msg'] = "Enter a valid Email adress. <br>The two password fields didn't match."
            return render(request, 'myapp/signup.html', params)
        elif (request.POST['Username'] in request.POST['Password']):
            params['error_msg'] = "username and password were too similar."
            return render(request, 'myapp/signup.html', params)
        else:
            obj = User()
            user = UserForm(request.POST, instance=obj)
            user.save()
            return redirect(to='/index')
    else:
        return render(request, 'myapp/signup.html', params)


def login_view(request):
    return render(request, "myapp/login.html")

def friends(request):
    return render(request, "myapp/friends.html")

def talk_room(request):
    return render(request, "myapp/talk_room.html")

def setting(request):
    return render(request, "myapp/setting.html")
