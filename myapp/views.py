from django.shortcuts import redirect, render
from .models import User
from .forms import SignUpForm, LogInForm
#ログイン機能
from django.contrib.auth import authenticate, login

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
        obj = User()
        form = SignUpForm(request.POST, request.FILES, instance=obj)
        
        if  (form.is_valid()):
            form.save()
            return redirect(to='/accounts/login')
            #https://techpr.info/python/django-loginfunction/
            #重複ログイン排除したい。

        else:
            params['message'] = '不備があります。これ今全部小文字じゃないとだめになってるから追って修正する'
   
    return render(request, "myapp/signup.html", params)

def friends(request):
    return render(request, "myapp/friends.html")

def talk_room(request):
    return render(request, "myapp/talk_room.html")

def setting(request):
    return render(request, "myapp/setting.html")

#ログインの設定
def login_view(request):
    if request.method == 'POST':
        obj = User
        form = LogInForm(request.POST, instance=obj)

        # usernameを指定します。
        # emailを使用したい場合は、Userモデルをカスタマイズする必要があります
        username = request.POST['username']
        print(username)
        password = request.POST['password']
        if form.is_valid():
            # DBに存在するか確認
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('talk_room')
            else:
                # 認証失敗時
                return redirect('login_view')

    return render(request, 'myapp/login.html')