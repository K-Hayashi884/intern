from django.shortcuts import redirect, render, get_object_or_404
from .models import User, UserImage, Talk
from .forms import SignUpForm, LoginForm, TalkForm, ChangeNameForm, ChangeMailForm, MyPasswordChangeForm, ChangeIconForm
from django.contrib.auth import login, logout 
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
import datetime
from django.db.models import Q
from django.urls import reverse_lazy


def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():

            user = form.save()
            image = form.cleaned_data['img']
            user_image=UserImage(user=user, image=image)
            user_image.save()

            return redirect('/')
        else:
            print('error')

    else:
        form = SignUpForm()




    return render(request, "myapp/signup.html" , {'form':form})

def login_view(request):
    form = LoginForm(request.POST)
    if request.method == 'POST':
        if  form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            #if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('friends')

        form.add_error(None, 'ユーザーID,パスワードが一致しません.')
    
    else:
        form = LoginForm()
    
    return render(request, "myapp/login.html",{'form':form})





@login_required
def friends(request):
    talk_done_data=[]
    talk_not_data=[]
    user = request.user
    user_imgs = UserImage.objects.all()
    friends = User.objects.exclude(username=user)
    for friend in friends:
        data=[]
        data.append(friend)
        for user_img in user_imgs:
            if user_img.user == friend:
                image=user_img.image
                data.append(image)
        talk = Talk.objects.filter(Q(msg_from=user, msg_to=friend)|Q(msg_from=friend, msg_to=user))
        talk = talk.order_by('time').last()
        if talk is None:
            data.append(friend.date_joined)
            talk_not_data.append(data)
        else:
            talk_msg=talk.msg
            talk_time=talk.time
            data.append(talk_msg)
            data.append(talk_time)
            talk_done_data.append(data)

 
    talk_done_data = sorted(talk_done_data, reverse=True, key=lambda x: x[3])
    talk_not_data = sorted(talk_not_data, key=lambda x: x[2])
    print(talk_done_data)
    print(talk_not_data)

    params={
    "talk_done_data":talk_done_data,
    "talk_not_data":talk_not_data,
    }

    return render(request, "myapp/friends.html", params)

@login_required
def talk_room(request, friend_user):
    user = request.user
    try:
        friend = User.objects.get(username=friend_user)
    except ObjectDoesNotExist:
        raise Http404
    talk = Talk.objects.filter(Q(msg_from=user, msg_to=friend)|Q(msg_from=friend, msg_to=user))
    talk = talk.order_by('time')
    

    if request.method == 'POST':
        form = TalkForm(request.POST)
        if form.is_valid():
            msg = form.cleaned_data.get('talk_msg')
            time = datetime.datetime.now()
            create_talk= Talk(msg=msg, msg_from=user, msg_to=friend, time=time)
            create_talk.save()

    
    else:
        form = TalkForm()
    
    params={
        "user":user,
        "friend":friend,
        "talk":talk,
        "form":form,
    }

    return render(request, "myapp/talk_room.html", params)

@login_required
def setting(request):
    user = request.user
    return render(request, "myapp/setting.html", {'user':user})

@login_required
def change_username(request, change_name):
    obj = User.objects.get(username=change_name)
    if request.method == 'POST':
        form = ChangeNameForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            
            return redirect('/setting/done_username')
    form = ChangeNameForm(instance=obj)

    return render(request, "myapp/change_username.html",{'form':form})


class PasswordChange(PasswordChangeView):
    form_class = MyPasswordChangeForm
    success_url = reverse_lazy('done_password')
    template_name = 'myapp/change_password.html'


@login_required
def change_mail(request):
    user = request.user
    if request.method == 'POST':
        form = ChangeMailForm(request.POST, instance=user)
        if form.is_valid():
            form.save()

            return redirect('/setting/done_mail')

    form = ChangeMailForm(instance=user)

    return render(request, "myapp/change_mail.html", {'form':form})

@login_required
def change_icon(request):
    user = request.user
    try:
        user_img = UserImage.objects.get(user=user)
    except ObjectDoesNotExist:
        user_img = UserImage.objects.none()
    if request.method == "GET":
        form = ChangeIconForm(instance=user)
        params = {
            "form":form,
            "user_img":user_img,
        }
        return render(request, "myapp/change_icon.html", params)
    elif request.method == "POST":
        print(request.POST)
        form = ChangeIconForm(request.POST,request.FILES)
        if form.is_valid():
            user_img.image = form.cleaned_data.get('image')
            user_img.save()
            return redirect('/setting/done_icon')
        params = {
            "form":form,
            "user_img":user_img,
        }
        return render(request, "myapp/done_icon.html", params)
    

@login_required
def done_username(request):
    return render(request, "myapp/done_username.html")


class PasswordChangeDone(PasswordChangeDoneView):
    """パスワード変更しました"""
    template_name = 'myapp/done_password.html'

@login_required
def done_mail(request):
    return render(request, "myapp/done_mail.html")

@login_required
def done_icon(request):
    return render(request, "myapp/done_icon.html")