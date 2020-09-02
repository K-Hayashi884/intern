from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import (
    SignUpForm,LoginForm,
    UserSettingForm,
    ImageSettingForm
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
        
def login_view(request):
    print("login_view")
    if request.method == "GET":
        form = LoginForm()
        params = {"form":form}
        return render (request, "myapp/login.html",params)
    elif request.method == "POST":
        print("login_view post")
        form = LoginForm(request.POST)
        username = request.POST['username'] 
        password = request.POST['password'] 
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("/") 
        else: 
            messages.error(request,'username or password not correct') 
            params = {"form":form}
            return render(request,"myapp/login.html",params)

def friends(request):
    return render (request, "myapp/friends.html")

def talk_room(request):
    return render (request, "myapp/talk_room.html")

@login_required
def setting(request):
    print('setting')
    user = request.user
    if request.method == "GET":
        print("GET")
        try:
            user_img = UserImage.objects.get(user=user)
        except ObjectDoesNotExist:
            user_img = UserImage.objects.none()
        setting_form = UserSettingForm(instance=user)
        image_setting_form = ImageSettingForm(instance=user)
        params = {
            "user_img":user_img,
            "setting_form":setting_form,
            "image_setting_form":image_setting_form,
        }
    elif request.method == "POST":
        print('POST')
        setting_form = UserSettingForm(request.POST)
        image_setting_form = ImageSettingForm(request.POST,request.FILES)
        user_data = User.objects.filter(pk=user.pk)
        try:
            user_img = UserImage.objects.get(user=user)
        except ObjectDoesNotExist:
            user_img = UserImage.objects.none()
        if setting_form.is_valid() and image_setting_form.is_valid():
            username = request.POST["username"]
            email = request.POST["email"]
            password = request.POST["password1"]
            if username is not None:
                user_data.update(username=username)
            if email is not None:
                user_data.update(email=email)
            if password is not None:
                user_data.update(password=password)
            try:
                user_img = UserImage.objects.get(user=user)
            except ObjectDoesNotExist:
                user_img = UserImage.objects.none()
            user_img.delete()
            image_setting_data = image_setting_form.save(commit=False)
            image_setting_data.user = user
            image_setting_data.save()
            params = {"setting_done":True}
        else:
            params = {
                "setting_form":setting_form,
                "image_setting_form":image_setting_form,
            }
    return render (request, "myapp/setting.html",params)
