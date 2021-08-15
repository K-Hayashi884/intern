#from shoji.django_project3.intern.myapp import admin
from django.shortcuts import redirect, render
from .models import Talk, User
#from myapp.models import User
#↑LogInForm
#ログイン機能
from django.contrib.auth import authenticate, login
#from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.views import(LoginView, LogoutView)
#from .forms import LoginForm
from django.contrib.auth.forms import AuthenticationForm 
#from django.contrib.auth import get_user_model
#User = get_user_model()
from .forms import (
    SignUpForm,
    TalkForm,
    UserNameSettingForm,
    UserEmailSettingForm,
    UserPasswordSettingForm,
    UserImageSettingForm,
)

def index(request):
    params = {
      'title': '¡Hala Madrid!',    
      }
    return render(request, "myapp/index.html", params)

def signup_view(request):
    params = {
        'title':'会員登録',
        'form': SignUpForm(),
        'message':'',
    }
    if (request.method == 'POST'):
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
#            user = User(username=form.cleaned_data["username"]) #★
#            user.set_password(form.cleaned_data["password"]) #★
#            user.save()
            form.save()
#        obj = User()
#        form = SignUpForm(request.POST, request.FILES, instance=obj)
#        
#        if (form.is_valid()):
#            user = User(username=form.cleaned_data["username"]) #★
#            user.set_password(form.cleaned_data["password"]) #★
#            user.save() #★
            return redirect(to='login_view')
            #https://techpr.info/python/django-loginfunction/
            #重複ログイン排除したい。
        else:
            params['message'] = '不備があります。これ今全部小文字じゃないとだめになってるから追って修正する'
   
    return render(request, "myapp/signup.html", params)

@login_required
def friends(request, num=1):
    ##user = request.user #★
    #login_user = request.user #★
    #user = User.objects.get(id=login_user.id)
    #data = Talk.objects.filter(Q(talk_to = user) | Q(talk_from = user))
    ##これ後でトークじゃなくて、Userを参照する形にする。orそのユーザーとのトークの一番上だけを参照する設定にする。
    #params = {
    #    'title': 'Friends',
    #    'form': TalkForm(),
    #    'data': data,
    #    'num': num,
    #}
    #return render(request, "myapp/friends.html", params)

    #ユーザーをdataにあてがうパターン
    login_user = request.user #★
    user = User.objects.get(id=login_user.id)
    data = User.objects.exclude(
            Q(id=login_user.id) |
            Q(id=1)
        ).distinct()
    #ここでlogin_user.idをはじきたいのと、HTMLの修正が必要
    params = {
        'title': 'トーク一覧',
        #'form': TalkForm(),
        'data': data,
        'num': num,
    }
    print(data)
    return render(request, "myapp/friends.html", params)

@login_required
def talk_room(request, num=1):
    login_user = request.user #★
    #ここでviewsのnumとURLのnumをつなぐ式を加えたい。いらない？
    #→繋がってるぽい
    user = User.objects.get(id=login_user.id)
    friend = User.objects.get(id=num) #なんとかここでページ分けしたユーザーを指定したい。
    print(user)
    print(friend)
    data = Talk.objects.filter(
            Q(talk_to = user, talk_from = friend) | 
            Q(talk_to = friend, talk_from = user)
        ).distinct().reverse()
    print(data)
    params = {
        'title': friend.username,
        'form': TalkForm(),
        'data': data,
        'num': num,
    }
    if(request.method == 'POST'):
        obj = Talk()
        talk_from = login_user
        talk_to = friend
        form = TalkForm(request.POST, instance=obj)
        form.save()
    return render(request, "myapp/talk_room.html", params)

    #送信者を設定できるようにしたい。
    
@login_required
def setting(request):
    return render(request, "myapp/setting.html")

@login_required
def user_name_change(request): #ここにnum入れるのは止めてる
    user = request.user
    if request.method == "GET":
        form = UserNameSettingForm(instance=user)
        params = {
            "form":form,
            "title": 'ユーザー名変更',
        }
        return render(request, "myapp/user_name_change.html", params)

    elif request.method == "POST":
        form = UserNameSettingForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return changecompleted(request)
        params = {
            "form":form,
            "title": 'ユーザー名変更',
        }
        #ここなんでわざわざemailなのかわからない
        return render(request, "myapp/changecompleted.html", params)
    

@login_required
def user_email_change(request): #ここにnum入れるのは止めてる
    user = request.user
    if request.method == "GET":
        form = UserEmailSettingForm(instance=user)
        params = {
            "form":form,
            "title": 'メールアドレス変更',
        }
        return render(request, "myapp/user_email_change.html", params)

    elif request.method == "POST":
        form = UserEmailSettingForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return changecompleted(request)
        params = {
            "form":form,
            "title": 'メールアドレス変更',
        }
        #nameの変更と同様にここにどのhtmlを繋ぐのがいいのかわからない
        return render(request, "myapp/changecompleted.html", params)


@login_required
def user_password_change(request): 
    user = request.user
    if request.method == "GET":
        form = UserPasswordSettingForm(instance=user)
        params = {
            "form":form,
            "title": 'パスワード変更',
        }
        return render(request, "myapp/user_password_change.html", params)

    elif request.method == "POST":
        form = UserPasswordSettingForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return changecompleted(request)
        params = {
            "form":form,
            "title": 'パスワード変更',
        }
        #nameの変更と同様にここにどのhtmlを繋ぐのがいいのかわからない
        return render(request, "myapp/changecompleted.html", params)

@login_required
def user_image_change(request): 
    user = request.user
    if request.method == "GET":
        form = UserImageSettingForm(instance=user)
        params = {
            "form":form,
            "title": 'アイコン変更',
        }
        return render(request, "myapp/user_image_change.html", params)

    elif request.method == "POST":
        form = UserImageSettingForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return changecompleted(request)
        params = {
            "form":form,
            "title": 'アイコン変更',
        }
        #nameの変更と同様にここにどのhtmlを繋ぐのがいいのかわからない
        return render(request, "myapp/changecompleted.html", params)


@login_required
def changecompleted(request):
    #ここで一括でプロフィール情報を表示して、変更後のプロフィールは以下の通りです。ってやりたい。
    login_user = request.user #★
    data = User.objects.filter(id=login_user.id)
    params = {
        'title': '変更が完了しました',
        'data':data,
        }
    return render(request, "myapp/changecompleted.html", params)

#ログインの設定

def login_view(request):
    if request.method == 'POST':
       # usernameを指定します。
       # emailを使用したい場合は、Userモデルをカスタマイズする必要があります
       username = request.POST['username']
       password = request.POST['password']
       print(f'username: {username}')
       print(f'password: {password}')
       
       # DBに存在するか確認
       user = authenticate(username=username,password=password)
       print(user)
       if user is not None:
           login(request, user)
           # renderでも可
           return redirect('friends')
       else:
           # 認証失敗時
           print('認証失敗時')
           params = {
            "error": "※名前かパスワードが間違っています",
            }
           return redirect('login_view')
    return render(request, 'myapp/login.html')

#class login_view(LoginView):
 #   form_class = AuthenticationForm
  #  authentication_form = None
   # redirect_field_name = 'myapp/friends'
   # template_name = 'myapp/login.html'
   # redirect_authenticated_user = False
   # extra_context = None