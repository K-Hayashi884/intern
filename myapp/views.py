from django.shortcuts import redirect, render
from .forms import signup,loginform,TalkForm,Change
from django.http import HttpResponse
from django.shortcuts import redirect
# from .models import member,User
from .models import User,Chatroom
from django.contrib.auth.views import LoginView ,LogoutView,PasswordChangeView
from django.contrib.auth import authenticate,get_user,login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import Http404,HttpResponseRedirect
from django.db.models import Q,Subquery,OuterRef
from django.core.exceptions import ObjectDoesNotExist
import datetime
from .forms import (
    SignUpForm,LoginForm,MailSettingForm,ImageSettingForm,PasswordChangeForm,UserNameSettingForm
)


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

@login_required
def friends(request):
    user=request.user
    friends=User.objects.exclude(id=user.id)
    latest_msg=Chatroom.objects.filter(Q(talkfrom=OuterRef("pk"),talkto=user)|Q(talkto=OuterRef("pk"),talkfrom=user)).order_by('-time')
    friends=User.objects.exclude(id=user.id).annotate(
        latest_msg_id=Subquery(latest_msg.values("pk")[:1]),
        latest_msg_content=Subquery(latest_msg.values("chat")[:1]),
        latest_msg_pub_date=Subquery(latest_msg.values("time")[:1]),
    ).order_by("-latest_msg_id")

    params={"people":friends,}
    return render(request, "myapp/friends.html",params)

@login_required
def talk_room(request,friend_username):
    user=request.user
    try:
        friend=User.objects.get(username=friend_username)
    except ObjectDoesNotExist:
        raise Http404

    talk=Chatroom.objects.filter(Q(talkfrom=user,talkto=friend)|Q(talkto=user,talkfrom=friend))
    talk=talk.order_by('time')
    form=TalkForm()

    params={"form": form,
            "user": user,
            "friend":friend,
            "talk":talk,
            "is_talk_toom":True,
    }

    if request.method=="POST":
        form=TalkForm(request.POST)
        if form.is_valid():
            text=form.cleaned_data.get('talk')
            now=datetime.datetime.now()
            new_talk=Chatroom(chat=text,talkfrom=user,talkto=friend,time=now)
            new_talk.save()
            return render(request, "myapp/talk_room.html",params)


    return render(request, "myapp/talk_room.html",params)

@login_required
def setting(request):
    return render(request, "myapp/setting.html")

@login_required
def mail_change(request):
    user=request.user
    if request.method=="GET":
        form=MailSettingForm(instance=user)
        params={
            "form":form,
        }
        return render (request,"myapp/mail_change.html",params)
    elif request.method=="POST":
        form=MailSettingForm(instance=user)
        if form.is_valid():
            form.save()
            return mail_change_done(request)
        params={
            "form":form,
        }
        return render (request,"myapp/mail_change.html",params)

    

