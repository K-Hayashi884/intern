from django.shortcuts import redirect, render
from .forms import SignUpForm
from .forms import LoginForm
from .forms import TalkForm
from .forms import PasswordChangeForm
from django.contrib.auth import authenticate, get_user, login
from .models import User, UserImage, Talk
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
import datetime
from django.db.models import Q
from django.urls import reverse_lazy


def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    if request.method == "GET":
        signup_form = SignUpForm()
    elif request.method == "POST":
        signup_form = SignUpForm(request.POST, request.FILES)
        if signup_form.is_valid():
            signup_form.save()
            username = signup_form.cleaned_data['username']
            email = signup_form.cleaned_data['email']
            password = signup_form.cleaned_data['password1']
            image = signup_form.cleaned_data['image']
            user = authenticate(username=username, password=password)
            login(request, user)
            user = User.objects.get(username=username)
            user_img = UserImage(
               user=user,
               image=image,
           )
            user_img.save()
            return redirect(to="/")
    params = {
        "form":signup_form
    }
    return render(request, "myapp/signup.html", params)

# def login_view(request):
#     return render(request, "myapp/login.html")

class Login(LoginView):
    form_class = LoginForm
    template_name= 'myapp/login.html'

def friends(request):
    user = request.user
    friends = User.objects.exclude(username=user.username)
    user_imgs = UserImage.objects.all()
    params = {
        "user":user,
        "user_imgs":user_imgs,
        "friends":friends,
    }
    return render(request, "myapp/friends.html", params)

def talk_room(request, partner_name):
    myname = request.user.username
    user = User.objects.get(username=myname)
    partner = User.objects.get(username=partner_name)
    form = TalkForm()
    history = Talk.objects.filter(Q(person_from=user, person_to=partner) | Q(person_from=partner, person_to=user))
    history = history.order_by('time')
    params = {
        "user":user,
        "partner":partner,
        "form":form,
        "history":history,
    }

    if request.method == "POST":
        post = TalkForm(request.POST)
        if post.is_valid():
            text = post.cleaned_data['talk']
            date = datetime.datetime.now()
            message = Talk(talk=text, time=date, person_from=user, person_to=partner)
            message.save()

    return render(request, "myapp/talk_room.html", params)

def setting(request):
    return render(request, "myapp/setting.html")

def change_name(request):
    user = request.user
    return render(request, "myapp/setting.html")

def change_mail(request):
    return render(request, "myapp/setting.html")

def change_icon(request):
    return render(request, "myapp/setting.html")

def change_pass(request):
    return render(request, "myapp/setting.html")

class PasswordChange(PasswordChangeView):
   form_class = PasswordChangeForm
   success_url = 'success/password'
   template_name = 'myapp/change_pass.html'

class PasswordChangeDone(PasswordChangeDoneView):
   template_name = 'myapp/change_success.html'

def change_success(request, name):
    params = {
        "name":name,
    }
    return render(request, "myapp/change_success.html", params)

def logout(request):
    return render(request, "myapp/setting.html")
