from django.contrib.auth import login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from .forms import NameForm, PasswordForm, signup_form, LoginForm ,PostForm, MailForm, IconForm
from .models import CustomUser, Talk
from django.contrib.auth.decorators import login_required
from django.db.models import Q

def index(request):
    return render(request, "myapp/index.html")


def signup_view(request):
    msg = '必要事項を入力してください'
    if request.method == 'POST':
        obj = CustomUser()
        form = signup_form(request.POST,request.FILES,instance=obj)
        if form.is_valid():
            form.save()
            return redirect(to='/')
        else:
            msg = '不正な入力'
    params = {
        'form':signup_form(),
        'msg':msg,
    }
    return render(request,'myapp/signup.html',params)


class login_view(LoginView):
    authentication_form = LoginForm
    template_name ='myapp/login.html'

@login_required
def friends(request):
    data = CustomUser.objects.all()
    user = request.user
    params = {
        'data':data,
        'user':user,
    }
    return render(request, "myapp/friends.html",params)

@login_required
def talk_room(request,user_id):
    user = request.user
    friend = get_object_or_404(CustomUser,id=user_id)
    data = Talk.objects.filter(Q(sender=user,receiver=friend) | Q(sender=friend,receiver=user)).order_by("date")
    

    if request.method == "POST":
        obj = Talk(sender=user,receiver=friend)
        form = PostForm(request.POST,instance=obj)

        if form.is_valid():
            form.save()
            url = f'/talk_room/{friend.id}'
            return redirect(to=url)
    
    params = {
        'user' : user,
        'friend' : friend,
        'data' : data,
        'form' : PostForm(),
    }
    return render(request, "myapp/talk_room.html",params)

@login_required
def setting(request):
    return render(request, "myapp/setting.html")

class logout_view(LoginRequiredMixin,LogoutView):
    ''''''
@login_required
def set_name(request):
    user = request.user
    if request.method == 'GET':
        form = NameForm(instance=user)
    elif request.method =='POST':
        form = NameForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return redirect(to='/notification')
    params = {
        'form' : NameForm(),
    }
    return render(request, "myapp/set_name.html", params)

@login_required
def set_mail(request):
    user = request.user
    if request.method == 'GET':
        form = MailForm(instance=user)
    elif request.method =='POST':
        form = MailForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return redirect(to='/notification')
    params = {
        'form' : MailForm(),
    }
    return render(request, 'myapp/set_mail.html', params)

@login_required
def set_icon(request):
    user = request.user
    if request.method == 'GET':
        form = IconForm(instance=user)
    elif request.method =='POST':
        form = IconForm(request.POST,request.FILES,instance=user)
        if form.is_valid():
            form.save()
            return redirect(to='/notification')
    params = {
        'form' : IconForm(),
    }
    return render(request, 'myapp/set_icon.html', params)

class set_password(PasswordChangeView):
    form_class = PasswordForm
    success_url = '/notification'
    template_name = 'myapp/set_password.html'

def notification(request):
    return render(request,"myapp/notification.html")