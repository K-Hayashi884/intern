from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.db.models import Q
from .models import User, Talk
from .forms import UserForm, LoginForm, TalkroomForm, ChangeNameForm, ChangeMailForm, ChangeImgForm, ChangeUsernameForm

def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    params =  {
        'error_msg':'',
        'form':UserForm(),
    }
    if (request.method == 'POST'):
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect(to='/')
    else:
        return render(request, 'myapp/signup.html', params)

class login_view(LoginView):
   form_class = LoginForm
   template_name = 'myapp/login.html'

def friends(request):
    user = request.user
    friends = User.objects.exclude(username=user.username)
    params = {
        'friends':friends
    }
    return render(request, "myapp/friends.html", params)

def talk_room(request, recipient_name):
    user = request.user
    self_url = '/talk_room/' + recipient_name
    params = {
        'form':TalkroomForm(),
        'data':Talk.objects.filter(Q(sender=user.username)|Q(recipient=user.username)),
        'recipient':recipient_name,
        'self_url':self_url
    }
    if (request.method == 'POST'):
        form = TalkroomForm(request.POST)
        if (form.is_valid()):
            sender = user.username
            recipient = recipient_name
            content = form.cleaned_data.get('message')
            talk = Talk(sender=sender, recipient=recipient, content=content)
            talk.save()
            return redirect(to=self_url)
        else:
            return render(request, "myapp/talk_room.html", params)
    else:
        return render(request, "myapp/talk_room.html", params)

def setting(request, setting_menu):
#なんでPythonにはswitch文がないんだよ
    if(setting_menu == 'menu'):
        return render(request, "myapp/setting_menu.html")

    elif(setting_menu == 'change_password'):
        params = {
            'msg':'',
            'form':ChangeNameForm()
        }
        user = request.user
        if(request.method == 'POST'):
            if(request.POST['newpassword'] == request.POST['passwordconfirmation'] and user.check_password(request.POST['oldpassword'])):
                user.set_password(request.POST['newpassword'])
                params['msg'] = 'パスワード変更完了'
                return render(request, "myapp/change_password.html", params)
            else:
                params['msg'] = '元のパスワードが間違っているか、新しいパスワードの確認ができません'
                return render(request, "myapp/change_password.html", params)
        else:
            return render(request, "myapp/change_password.html", params)

    elif(setting_menu == 'change_mail'):
        params = {
            'msg':'',
            'form':ChangeMailForm()
        }
        user = request.user
        if(request.method == 'POST'):
            if(user.check_password(request.POST['password'])):
                changed_user = ChangeMailForm(request.POST, instance=user)
                changed_user.save()
                user.set_password(request.POST['password'])
                params['msg'] = 'メールアドレス変更完了'
                return render(request, "myapp/change_mail.html", params)
            else:
                params['msg'] = 'パスワードが間違っています'
                return render(request, "myapp/change_mail.html", params)
        else:
            return render(request, "myapp/change_mail.html", params)

    elif(setting_menu == 'change_img'):
        params = {
            'msg':'',
            'form':ChangeImgForm()
        }
        user = request.user
        if(request.method == 'POST'):
            if(user.check_password(request.POST['password'])):
                changed_user = ChangeImgForm(request.FILES, request.POST, instance=user)
                changed_user.save()
                user.set_password(request.POST['password'])
                params['msg'] = '   アイコン変更完了'
                return render(request, "myapp/change_img.html", params)
            else:
                params['msg'] = 'パスワードが間違っています'
                return render(request, "myapp/change_img.html", params)
        else:
            return render(request, "myapp/change_img.html", params)

    elif(setting_menu == 'change_username'):
        params = {
            'msg':'',
            'form':ChangeUsernameForm()
        }
        user = request.user
        if(request.method == 'POST'):
            if(user.check_password(request.POST['password'])):
                changed_user = ChangeUsernameForm(request.POST, instance=user)
                changed_user.save()
                user.set_password(request.POST['password'])
                params['msg'] = '   ユーザー名変更完了'
                return render(request, "myapp/change_username.html", params)
            else:
                params['msg'] = 'パスワードが間違っています'
                return render(request, "myapp/change_username.html", params)
        else:
            return render(request, "myapp/change_username.html", params)

    elif(setting_menu == 'logout'):
        logout(request)
        return redirect(to='/')