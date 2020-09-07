from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
)
from .forms import (
    SignUpForm,
    LoginForm,
    MailSettingForm,
    ImageSettingForm,
    PasswordChangeForm,
    UserNameSettingForm,
)
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.
from .models import User,UserImage


def index(request):
    return render (request, "myapp/index.html")

def signup_view(request):
    if request.method == "GET":
        form = SignUpForm()
        params = {"form":form,}
        return render(request,"myapp/signup.html",params)
    elif request.method == "POST":
        form = SignUpForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            #フォームから'username'を読み取る
            username = form.cleaned_data.get('username')
            #フォームから'password1'を読み取る
            password = form.cleaned_data.get('password1')
            #フォームから'img'を読み取る
            image = form.cleaned_data.get('img')
            user = authenticate(username=username, password=password)
            login(request, user)
            user = User.objects.get(username=username)
            user_img = UserImage(
                user=user,
                image=image,
            )
            user_img.save()
            return redirect("/")
        params = {"form":form,}
        return render(request,"myapp/signup.html",params)


class Login(LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'myapp/login.html'

class Logout(LoginRequiredMixin, LogoutView):
    """ログアウトページ"""
    template_name = 'myapp/login.html'

def friends(request):
    return render (request, "myapp/friends.html")

def talk_room(request):
    return render (request, "myapp/talk_room.html")

@login_required
def setting(request):
    return render (request, "myapp/setting.html")

@login_required
def user_img_change(request):
    user = request.user
    try:
        user_img = UserImage.objects.get(user=user)
    except ObjectDoesNotExist:
        user_img = UserImage.objects.none()
    if request.method == "GET":
        form = ImageSettingForm(instance=user)
        params = {
            "form":form,
            "user_img":user_img,
        }
        return render(request,"myapp/user_img_change.html",params)
    elif request.method == "POST":
        form = ImageSettingForm(request.POST,request.FILES)
        if form.is_valid():
            user_img.image=request.FILES["image"]
            user_img.save()
            return user_img_change_done(request)
        params = {
            "form":form,
            "user_img":user_img,
        }
        return render(request,"myapp/user_img_change.html",params)


@login_required
def user_img_change_done(request):
    return render(request,"myapp/user_img_change_done.html")
@login_required
def mail_change(request):
    print("mail_change")
    user = request.user
    if request.method == "GET":
        form = MailSettingForm(instance=user)
        params = {
            "form":form,
        }
        return render (request,"myapp/mail_change.html",params)
    elif request.method == "POST":
        form = MailSettingForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return mail_change_done(request)
        params = {
            "form":form,
        }
        return render(request,"myapp/mail_change.html",params)
@login_required
def mail_change_done(request):
    return render(request,"myapp/mail_change_done.html")

@login_required
def username_change(request):
    print("username_change")
    user = request.user
    if request.method == "GET":
        form = UserNameSettingForm(instance=user)
        params = {
            "form":form,
        }
        return render (request,"myapp/username_change.html",params)
    elif request.method == "POST":
        form = UserNameSettingForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return username_change_done(request)
        params = {
            "form":form,
        }
        return render(request,"myapp/mail_change.html",params)
@login_required
def username_change_done(request):
    return render(request,"myapp/username_change_done.html")

class PasswordChange(PasswordChangeView):
    """パスワード変更ビュー"""
    form_class = PasswordChangeForm
    success_url = reverse_lazy('register:password_change_done')
    template_name = 'myapp/password_change.html'

class PasswordChangeDone(PasswordChangeDoneView):
    """パスワード変更しました"""
    template_name = 'myapp/password_change_done.html'