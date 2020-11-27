from django.shortcuts import redirect, render
from django.http import HttpResponse
from .forms import (
    SignupForm, LoginForm, TalkroomForm, MyPasswordChangeForm,
    EmailChangeForm, UserImageChangeForm, UsernameChangeForm
)
from django.core.exceptions import ObjectDoesNotExist
from .models import User, UserImage, Talk
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import (
    LoginView, PasswordChangeView, PasswordChangeDoneView
)
from django.contrib.auth.decorators import login_required
from django.db.models import Q, OuterRef, Subquery
from django.urls import reverse_lazy


def index(request):
    params = {
        'gotoLogin':'login_view',
        'gotoSignup':'signup_view',
    }
    return render(request, "myapp/index.html", params)

def signup_view(request):
    params = {
        'form' : SignupForm(),
        
    }
    if (request.method == 'POST'):
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            image = form.cleaned_data.get('img')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                user = User.objects.get(username=username)
                user_img = UserImage(user=user,image=image)
                user_img.save()
            return redirect(to='/')
        
    return render(request, "myapp/signup.html", params)




@login_required
def friends(request):
    user = request.user
    newest = Talk.objects.filter(
        Q(sender=user, receiver=OuterRef('pk')) | Q(sender=OuterRef('pk'), receiver=user)
    ).order_by('-date')


    data = User.objects.exclude(id=user.id).annotate(
        newest_sender_id=Subquery(newest.values("pk")[:1]),
        newest_talk_content=Subquery(newest.values("message")[:1]),
        newest_talk_date=Subquery(newest.values("date")[:1]),
    ).order_by('newest_sender_id')

    params = {
        'data': data,
        'gotoFriends': 'friends',
        'gotoSetting': 'setting',
        'gotoTalkroom': 'talk_room/<str:room_name>',
    }
    return render(request, "myapp/friends.html", params)

@login_required
def talk_room(request, room_name):#room_nameを受け取る→htmlを変化
    #room_nameによってデータべスから取得するデータを決める
    # username = request.user.username
    # data = Talk.objects.filter(Q(sender=room_name, receiver=username)|Q(receiver=room_name, sender=username)).order_by('date')
    #↑foreignkey使わないパターン
    user = request.user
    data = user.sender.all().filter(receiver__username=room_name).union(user.receiver.all().filter(sender__username=room_name))
    params = {
        'room_name': room_name,
        'gotoFriends': 'friends',
        'gotoTalkroom': 'talk_room/<str:room_name>',
        'form': TalkroomForm(),
        'data': data,
    }
    if (request.method == 'POST'):
        message = request.POST['talk']
        sender = request.user
        receiver = User.objects.get(username=room_name)
        talk = Talk(sender=sender,receiver=receiver,message=message)
        talk.save()
    
    return render(request, "myapp/talk_room.html", params)

@login_required
def setting(request):
    data = User.objects.all()
    params = {
        'data': data,
        'gotoFriends': 'friends',
        'gotoSetting': 'setting',
        'gotoTalkroom': 'talk_room/<str:room_name>',
        'username_change': 'username_change',
        'email_change': 'email_change',
        'user_img_change': 'user_img_change',
        'password_change': 'password_change',
        'logout': 'logout_view'
    }
    return render(request, "myapp/setting.html", params)




@login_required
def username_change(request):
    user = request.user
    params = {
        'form': UsernameChangeForm(instance=user)
    }
    if (request.method == 'POST'):
        form = UsernameChangeForm(request.POST ,instance=user)
        if form.is_valid():
            form.save()
            return username_change_done(request)
    return render(request, "myapp/username_change.html", params)

@login_required
def username_change_done(request):
    return render(request, "myapp/username_change_done.html")




@login_required
def user_img_change(request):
    user = request.user
    try:
        user_img = UserImage.objects.get(user=user)
    except ObjectDoesNotExist:
        user_img = UserImage.objects.none()
    params = {
        'form': UserImageChangeForm(instance=user_img),
        'user_img': user_img,
    }
    if (request.method == 'POST'):
        form = UserImageChangeForm(request.POST, request.FILES, instance=user_img)
        if form.is_valid():
            #user_img.image = form.cleaned_data.get('image')
            #user_img.save()
            form.save()
            return user_img_change_done(request)
    return render(request, "myapp/user_img_change.html", params)

@login_required
def user_img_change_done(request):
    return render(request, "myapp/user_img_change_done.html")



@login_required
def email_change(request):
    user = request.user
    params = {
        'form': EmailChangeForm(instance=user)
    }
    if (request.method == 'POST'):
        form = EmailChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return email_change_done(request)
    return render(request, "myapp/email_change.html", params)

@login_required
def email_change_done(request):
    return render(request, "myapp/email_change_done.html")



class PasswordChange(PasswordChangeView):
    form_class = MyPasswordChangeForm
    success_url = reverse_lazy('password_change_done')
    template_name = 'myapp/password_change.html'


class PasswordChangeDone(PasswordChangeDoneView):
    template_name = 'myapp/password_change_done.html'
