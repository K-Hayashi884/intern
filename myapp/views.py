from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from .models import User
from .forms import SignupForm, LoginForm


def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST, request.FILES, instance=User())
        if form.is_valid():
            form.save()
            return redirect(to='/')
        else:
            return render(request, "myapp/signup.html", {'form': form})
    return render(request, "myapp/signup.html", {'form': SignupForm()})

class login_view(LoginView):
    form_class = LoginForm
    template_name = 'myapp/login.html'    

def friends(request):
    return render(request, "myapp/friends.html")

def talk_room(request):
    return render(request, "myapp/talk_room.html")

def setting(request):
    return render(request, "myapp/setting.html")
