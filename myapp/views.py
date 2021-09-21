from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView,LogoutView
from .forms import SignUpForm, ImageForm,LoginForm,MessageForm,ChangeUsernameForm, ChangeMailForm, ChangeImageForm
from .models import Image, User,Message
from django.db.models import Q
from django.contrib.auth.views import PasswordChangeView,PasswordChangeDoneView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

def index(request):
    return render(request, "myapp/index.html")


def signup_view(request):
    params={
        'signupform': SignUpForm(),
        'imageform': ImageForm(),
    }
    if(request.method == 'POST'):
        signup = SignUpForm(request.POST)
        params['signupform']=signup
        if(signup.is_valid()):
            signup.save()
            name = request.POST['username']
            user = User.objects.get(username=name)
            image_obj =Image(
                user=user,
                )
            image = ImageForm(request.POST, request.FILES, instance=image_obj)
            params['imageform']=image
            if(image.is_valid()):
                image.save()
                image_model=Image.objects.get(user=user)
                message=Message(message="no",image=image_model,latest_message=True)
                message.save()
                return redirect(to='/')
    return render(request, "myapp/signup.html", params)


class Login(LoginView):
    form_class = LoginForm
    template_name = 'myapp/login.html'

@login_required()
def friends(request):
    login_user=request.user
    message=Message.objects.filter(Q(user_from=request.user) | Q(user_to=request.user),latest_message=True).order_by('date').reverse()
    all_message=Message.objects.filter(latest_message=True).order_by('date').reverse()
    no_message=all_message.exclude(Q(user_from=request.user) | Q(user_to=request.user))
    for i in no_message:
        for j in message:
            if((i.image.user == j.user_from) or (i.image.user == j.user_to)):
                all_message=all_message.exclude(message="no",image=i.image)
                break
    all_message=all_message.filter(Q(user_from=request.user) | Q(user_to=request.user) | Q(message="no"))
    all_message=all_message.exclude(message="no",image=request.user.img)
    params={
        'message': all_message,
        'login_user': login_user,
    }
    return render(request, "myapp/friends.html",params)

@login_required()
def talk_room(request,friend_username):
    friend_user=User.objects.get(username=friend_username)
    friend_image=friend_user.img
    data=Message.objects.filter(Q(user_from=request.user) | Q(user_from=friend_user),Q(user_to=friend_user) | Q(user_to=request.user)).order_by('date')
    message_before=data.reverse().first()
    params={
        'messageform':MessageForm(),
        'name':friend_username,
        'data':data,
    }
    if(request.method == 'POST'):
        form=MessageForm(request.POST)
        if(form.is_valid()):
            message=request.POST['message']
            message_model=Message(user_from=request.user,user_to=friend_user,message=message,image=friend_image,latest_message=True)
            message_model.save()
            if(message_before != None):
                message_before.latest_message=False
                message_before.save()
    return render(request, "myapp/talk_room.html",params)

@login_required()
def setting(request):
    return render(request, "myapp/setting.html")

class Logout(LogoutView):
    template_name = "myapp/index.html"

@login_required()
def change_username(request):
    params={
        'change_username_form':ChangeUsernameForm(),
    }
    if(request.method == 'POST'):
        form=ChangeUsernameForm(request.POST,instance=request.user)
        params['change_username_form']=form
        if(form.is_valid()):
            form.save()
            return redirect(to='change_username_complete')
    return render(request,"myapp/change_username.html",params)

@login_required()
def change_mail(request):
    params={
        'change_mail_form':ChangeMailForm(),
    }
    if(request.method == 'POST'):
        form=ChangeMailForm(request.POST,instance=request.user)
        params['change_mail_form']=form
        if(form.is_valid()):
            form.save()
            return redirect(to='change_mail_complete')
    return render(request,"myapp/change_mail.html",params)


@login_required()
def change_icon(request):
    params={
        'change_icon_form':ChangeImageForm(),
    }
    if(request.method == 'POST'):
        form=ChangeImageForm(request.POST,request.FILES,instance=request.user.img)
        params['change_icon_form']=form
        if(form.is_valid()):
            form.save()
            return redirect(to='change_icon_complete')
    return render(request,"myapp/change_icon.html",params)

class PasswordChange(LoginRequiredMixin, PasswordChangeView):
    success_url = reverse_lazy('change_password_complete')
    template_name = 'myapp/change_password.html'

@login_required()
def change_username_complete(request):
    return render(request,"myapp/change_username_complete.html")

@login_required()
def change_mail_complete(request):
    return render(request,"myapp/change_mail_complete.html")

@login_required()
def change_icon_complete(request):
    return render(request,"myapp/change_icon_complete.html")

@login_required()
def change_password_complete(request):
    return render(request,"myapp/change_password_complete.html")

class PasswordChangeDone(LoginRequiredMixin,PasswordChangeDoneView):
    template_name = 'change_password_complete.html'
