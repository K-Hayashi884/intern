from django import forms
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.views import generic
from .models import User, Message
from .forms import MessageForm, UserForm, UsernameChangeForm, EmailChangeForm, ImageChangeForm, MyPasswordChangeForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.db.models import Q
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView


def index(request):
    print(request.user)
    return render(request, "myapp/index.html")

# これは使わない
# def signup_view(request):
#     params = {
#         'form' : UserForm(),
#         'message' : '' ,
#     }
#     if(request.method == 'POST'):
#         obj = User()
#         user = UserForm(request.POST, instance=obj)
#         if(user.is_valid()):
#             user.save()
#             return redirect(to='/index')
#         else:
#             params['message'] = 'no good'
#             print('no ')
#     return render(request, "myapp/signup.html", params)

# これでサインアップする
class ImageView(CreateView):
    model = User
    template_name = 'myapp/signup.html'
    form_class = UserForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        users = form.save(commit=False)
        users.user = self.request.user
        users.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        
        return super().form_invalid(form)


# def login_view(request):
    # return render(request, "myapp/login.html")

def friends(request):
    # ログインしているユーザーを判定
    login_user_id = request.user.id
    # ログインしているユーザーを除いて表示
    friends = User.objects.exclude(id=login_user_id).order_by('id').reverse()
    params = {
        'friends' : friends,
    }
    return render(request, "myapp/friends.html", params)

def talk_room(request, user_id):
    # お相手を定義
    friend = User.objects.get(id=user_id)
    print(friend.image)
    # 自分を定義
    login_user_id = request.user.id
    me = User.objects.get(id=login_user_id)
    print(me.image)
    # 処理
    if request.method == 'POST':
        obj = Message()
        message = MessageForm(request.POST, instance=obj)
        if message.is_valid():
            # messageモデルのインスタンスとユーザーを紐づけ
            message.instance.reciever = friend
            message.instance.sender = me
            # 保存
            message.save()
        else: 
            print('why')
    # メッセージを表示
    # recieverで
    messages = Message.objects.filter(Q(reciever=friend, sender=me)|Q(reciever=me, sender=friend)).order_by('message_date')
    reciever = friend
    sender = me
    params = {
        'form' : MessageForm,
        'messages' : messages,
        'reciever' : reciever,
        'sender' : sender,
        
    }
    
    return render(request, "myapp/talk_room.html", params)

def setting(request):
    params = {
        'login_id' : request.user.id,
    }
    print(request.user.id)
    return render(request, "myapp/setting.html", params)

def username_edit(request, login_id):
    login_id = request.user.id
    current_username = User.objects.get(id=login_id)
    if(request.method == 'POST'):
        username_edit = UsernameChangeForm(request.POST, instance=current_username)
        username_edit.save()
        print(username_edit)
        return redirect(to='/setting')
    params = {
        'current_username' : current_username,
        'form' : UsernameChangeForm(instance=current_username),
    }
    return render(request, "myapp/username_edit.html", params)

def email_edit(request, login_id):
    login_id = request.user.id
    current_email = User.objects.get(id=login_id)
    if(request.method == 'POST'):
        email_edit = EmailChangeForm(request.POST, instance=current_email)
        email_edit.save()
        return redirect(to='/setting')
    params = {
        'current_email' : current_email,
        'form' : EmailChangeForm(instance=current_email),
    }
    return render(request, "myapp/email_edit.html", params)

def image_edit(request, login_id):
    login_id = request.user.id
    current_image = User.objects.get(id=login_id)
    if(request.method == 'POST'):
        image_edit = ImageChangeForm(request.POST, instance=current_image)
        image_edit.save()
        return redirect(to='/setting')
    params = {
        'current_image' : current_image,
        'form' : ImageChangeForm(instance=current_image),
    }
    return render(request, "myapp/image_edit.html", params)

# def password_edit(request, login_id):
#     login_id = request.user.id
#     current_image = User.objects.get(id=login_id)
#     if(request.method == 'POST'):
#         image_edit = PasswordChangeForm(request.POST, instance=current_image)
#         image_edit.save()
#         return redirect(to='/setting')
#     params = {
#         'current_image' : current_image,
#         'form' : PasswordChangeForm(instance=current_image),
#     }
#     return render(request, "myapp/password_edit.html", params)

class PasswordChange(PasswordChangeView):
    """パスワード変更ビュー"""
    form_class = MyPasswordChangeForm
    success_url = reverse_lazy('index')
    template_name = 'myapp/password_edit.html'

