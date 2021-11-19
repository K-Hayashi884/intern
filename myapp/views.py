from django.shortcuts import redirect, render
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from .models import Message
from .forms import UserChangeForm,UserPasswordChangeForm
from .forms import MessageForm
from .forms import SignUpForm
from .forms import LoginForm

def index(request):
    params={
        'goto_signup':'signup_view',
        'goto_login':'login_view',
    }
    return render(request, "myapp/index.html",params)

def signup_view(request):
    if request.method=="POST":
        user_form=SignUpForm(request.POST,request.FILES)
        if user_form.is_valid():
            user_form.save()
            username=user_form.cleaned_data.get("username")
            password=user_form.cleaned_data.get("password1")
            new_user=authenticate(username=username,password=password)
            if new_user is not None:
                login(request,new_user)
                return redirect('friends')
    else:
        user_form=SignUpForm()
    params={
        'user_form':user_form,
    }
    return render(request, "myapp/signup.html",params)

def login_view(request):
    if request.method=='POST':
        form=LoginForm(request.POST)
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        if user is not None:
            if user.is_active:
                login(request,user)
                return redirect('friends')
        else:
            pass
    else:
        form=LoginForm()
    return render(request, "myapp/login.html",{'form':form})

@login_required
def friends(request):
    user=request.user
    data = Profile.objects.exclude(id=user.id)
    params = {
        'user':user,
        'data':data,
    }
    return render(request, "myapp/friends.html",params)

@login_required
def talk_room(request,username):
    user=request.user
    if request.method=='POST':
        obj=Message()
        message=MessageForm(request.POST,instance=obj)
        if message.is_valid():
            obj.reciever=Profile.objects.get(username=username)
            content=message.cleaned_data.get("content")
            message.save()
    else:
        message=MessageForm()
    data=Message.objects.all().reverse()
    reciever=Profile.objects.get(username=username)
    params={
        'reciever':reciever,
        'sender':user,
        'data':data,
        'message':message,
    }
    return render(request, "myapp/talk_room.html",params)

def setting(request):
    user=request.user
    params={
        'user':user
    }
    return render(request, "myapp/setting.html",params)

@login_required
def Logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('Login'))

@login_required
def update_username(request):
    if(request.method=="POST"):
        form=UserChangeForm(request.POST)
        if(form.is_valid):
            new_username=request.POST['username']
            old_obj=Profile.objects.get(username=request.user.username)
            old_obj.username=new_username
            old_obj.save()
            return redirect('update_username_complete')
    else:
        form=UserChangeForm()
    params={
        'form':form
    }
    return render(request, "myapp/update_username.html",params)

@login_required
def update_username_complete(request):
    return render(request, "myapp/update_username_complete.html")

@login_required
def update_email(request):
    if(request.method=="POST"):
        form=UserChangeForm(request.POST)
        if(form.is_valid):
            new_email=request.POST['email']
            old_obj=Profile.objects.get(username=request.user.username)
            old_obj.email=new_email
            old_obj.save()
            return redirect('update_email_complete')
    else:
        form=UserChangeForm()
    params={
        'form':form
    }
    return render(request, "myapp/update_email.html",params)

@login_required
def update_email_complete(request):
    return render(request, "myapp/update_email_complete.html")

@login_required
def update_image(request):
    if(request.method=="POST"):
        form=UserChangeForm(request.FILES)
        if(form.is_valid):
            new_image=request.FILES['image']
            old_obj=Profile.objects.get(username=request.user.username)
            old_obj.image=new_image
            old_obj.save()
            return redirect('update_image_complete')
    else:
        form=UserChangeForm()
    params={
        'form':form
    }
    return render(request, "myapp/update_image.html",params)

@login_required
def update_image_complete(request):
    return render(request, "myapp/update_image_complete.html")

@login_required
def update_password(request):
    form=UserPasswordChangeForm(request.user,request.POST)
    if(request.method=='POST' and form.is_valid()):
        form.save()
        return redirect('login_view')
    
    params={
        'form':form,
    }
    return render(request, "myapp/update_password.html",params)

@login_required
def update_password_complete(request):
    return render(request, "myapp/update_password_complete.html")
