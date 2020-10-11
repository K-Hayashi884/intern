from django.shortcuts import redirect, render
from .forms import signup,loginform
from django.http import HttpResponse
from django.shortcuts import redirect
# from .models import member,User
from .models import User
from django.contrib.auth.views import LoginView ,LogoutView,PasswordChangeView
from django.contrib.auth import authenticate,get_user,login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import Http404,HttpResponseRedirect


def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    form = signup()
    if (request.method=='POST'):
        form = signup(request.POST, request.FILES)
        if form.is_valid():
            # saveの処理
            form.save()
            return redirect(to='/')
        else:
            params = {
                'title':'会員登録',
                'form': form,
            }
            return render(request, "myapp/signup.html",params)
         
    params = {
        'title':'会員登録',
        'form': form,
    }
    return render(request, "myapp/signup.html",params)

class Login(LoginView):
    authentication_form=loginform
    template_name='myapp/login.html'

def login_view(request):

         



    return render(request, "myapp/login.html")

def friends(request):
    return render(request, "myapp/friends.html")

def talk_room(request):
    return render(request, "myapp/talk_room.html")

def setting(request):
    return render(request, "myapp/setting.html")


