from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView,  LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from .forms import SignupForm,MessageForm,ChangeUsernameForm,ChangeImageForm,ChangeEmailForm,ChangePasswordForm
from .models import Message


User=get_user_model()

def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):

    params={
        'form':SignupForm(),
    }

    if (request.method == 'POST'):
            obj = User()
            form = SignupForm(request.POST, request.FILES, instance=obj)
            if (form.is_valid()):
                form.save()
                return redirect(to='/')
            else:
                params['form'] = form

    return render(request, "myapp/signup.html",params)

class login(LoginView):
    authentication_form = AuthenticationForm
    template_name='myapp/login.html'


@login_required
def friends(request):
    user=request.user
    
    data= User.objects.all()

    message_id= []
    last_contents= {}

    for friend in data:
       
        messager_id= friend.id

        last_message= Message.objects.filter(
        Q(senduser_id=user.id,reseaveuser_id=messager_id)|
        Q(senduser_id=messager_id,reseaveuser_id=user.id)
        ).order_by('pub_date') .last()
        
        # メッセージがあれば、辞書に最後のメッセージと、ログインしていないほうの送信者のidを入れる
        if last_message!=None:
            message_id.append(messager_id)
            id_contents={messager_id:last_message.content}

            last_contents.update(id_contents)
        
        message_friend_data= User.objects.filter(id__in=message_id)

        none_friend_data= User.objects.exclude(id__in=message_id)
    
    params ={
        'title':'friend',
        'header':'友達',
        'message_friend_data':message_friend_data,
        'none_friend_data':none_friend_data,
        'last_contents':last_contents,
        'num':user.id,
    }
    return render(request,'myapp/friends.html',params)


@login_required
def talk_room(request,reseave_user_id):
    user= request.user

    senduser_name= User.objects.get(id=user.id).username

    friend_name= User.objects.get(id=reseave_user_id).username


    data=Message.objects.filter(
        Q(senduser_id=user.id,reseaveuser_id=reseave_user_id)|
        Q(senduser_id=reseave_user_id,reseaveuser_id=user.id)
    ).order_by('pub_date') 

    params={
    'title':'talk_room',
    'header_title':friend_name,
    'form':MessageForm(),
    'send_user_id':user.id,
    'reseave_user_id':reseave_user_id,
    'data':data,
    }
    #   メッセージが送られるとそのメッセージもふくめた新しいトーク画面が表示される
    if(request.method=='POST'):
        content= request.POST['message']
        message= Message(
            senduser_name=senduser_name,
            content=content,
            senduser_id=user.id,
            reseaveuser_id=reseave_user_id
            )

        if message:
            message.save()
            data=Message.objects.filter(
                Q(senduser_id=user.id,reseaveuser_id=reseave_user_id)|
                Q(senduser_id=reseave_user_id,reseaveuser_id=user.id)
            ).order_by('pub_date') 
            params['data']=data

    #   else:
    #     print('There are something wrong!')
        
    return render(request,'myapp/talk_room.html',params)

def setting(request):
    return render(request,'myapp/setting.html')

def change_username(request):
    user=request.user

    obj = User.objects.get(id=user.id)
    if (request.method=='POST'):
        friend = ChangeUsernameForm(request.POST,instance=obj)
        friend.save()
        return redirect(to='/change_username_done')

    params={
        'form':ChangeUsernameForm(),
    }
    return render(request,'myapp/change_username.html',params)

@login_required
def change_username_done(request):
    return render(request,'myapp/change_username_done.html')

@login_required
def change_email(request):
    user = request.user

    obj = User.objects.get(id=user.id)
    if (request.method=='POST'):
        friend = ChangeEmailForm(request.POST,instance=obj)
        friend.save()
        return redirect(to='/change_email_done/')

    params={
        'form':ChangeEmailForm(),
    }

    return render(request,'myapp/change_email.html',params)

@login_required
def change_email_done(request):
    return render(request,'myapp/change_email_done.html')

@login_required
def change_img(request):
    user=request.user

    obj = User.objects.get(id=user.id)
    if (request.method=='POST'):
        friend = ChangeImageForm(request.POST, request.FILES,instance=obj)
        friend.save()
        return redirect(to='/change_img_done')

    params={
        'form':ChangeImageForm(), 
    }

    return render(request,'myapp/change_img.html',params)

@login_required
def change_img_done(request):
    return render(request,'myapp/change_img_done.html')

@login_required
def change_password(request):
    user=request.user

    params={
        'form':ChangePasswordForm(), 
    }
    if (request.method=='POST'):
        obj = User.objects.get(id=user.id)
        friend = ChangePasswordForm(request.POST,instance=obj)
        if(friend.is_valid()):
            friend.save()
            return redirect(to='/change_password_done')

    return render(request,'myapp/change_password.html',params)

@login_required
def change_password_done(request):
    return render(request,'myapp/change_password_done.html')

# @login_required
# def logout_veiws(request):
#     logout(request)
#     return redirect(to='/login')

class logout(LoginRequiredMixin,LogoutView):
    pass
