from django.contrib import messages
from django.contrib.auth import login,logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Max, Prefetch, Value, Subquery, OuterRef
from django.db.models.functions.comparison import Greatest
from django.db.models.functions import Coalesce
from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.core import serializers

from .forms import UserForm,LoginForm,MessageForm,FindForm
from .models import User, Message

def index(request):
    params = {
        'title': 'DeMiAインターン'
    }
    return render(request, "myapp/index.html", params)

def signup_view(request):
    if request.method == 'POST':
        #print("hello")
        form = UserForm(request.POST)
        if form.is_valid():
            #print("hello2")
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
        else:
            print(form.errors)
    else:
        form = UserForm()
    return render(request, 'myapp/signup.html', {'form': form})
    # if (request.method == 'POST'):
    #     obj = User()
    #     user = UserForm(request.POST, instance=obj)

    #     user.save()
    #     return redirect(to='/')
    # params = {
    #     'form': UserForm(),
    #     'err_msg': '',
    # }
    # return render(request, "myapp/signup.html", params)

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            user = User.objects.get(username=username)
            if user is not None:
                # print("ok")
                login(request, user)
                return redirect('/friends/'+str(user.id))
            else:
                # print("no match")
                params = {
                    'form': form,
                    'err_msg': "ユーザー名またはパスワードが間違っています。"
                }
                return render(request, "myapp/login.html", params)
        else:
            form = LoginForm(request.POST)
            # print("no valid")
            params = {
                'form': form,
                'err_msg': "ユーザー名またはパスワードが間違っています。"
            }
            return render(request, "myapp/login.html", params)
    else:
        form = LoginForm()
        return render(request, "myapp/login.html", {'form': form,})

@login_required(redirect_field_name='redirect_to')
def friends(request):
    me = request.user
    form = FindForm(request.POST or None)
    if request.method == 'POST':
        find = request.POST['find']
        found_qs = User.objects.filter(username__contains=find)
        user = User.objects.exclude(username__contains=find)
        # 続きの処理は書いていください。
    else:
        latest_msg = Message.objects.filter(
                        Q(sender=OuterRef("pk"),receiver=me) | Q(sender=me,receiver=OuterRef("pk"))
                    ).order_by('-pub_date')

        user_qs = (User.objects
            .exclude(id=me.id)
            .annotate(
                latest_msg_id=Subquery(
                    latest_msg.values("pk")[:1]
                ),
                latest_msg_content=Subquery(
                    latest_msg.values("content")[:1]
                ),
                latest_msg_pub_date=Subquery(
                    latest_msg.values("pub_date")[:1]
                ),
            )
            .order_by("-latest_msg_id")
        )

    params = {
        'form': form,
        'user_qs':user_qs,
        'me': me,
    }
    return render(request, "myapp/friends.html", params)

def search_user(request):
    q = request.GET.get("q","")
    user_qs = User.objects.filter(username__contains=q)[:5]
    user_json = serializers.serialize('json',user_qs)
    return HttpResponse(user_json, content_type='application/json')

@login_required(redirect_field_name='redirect_to')
def talk_room(request, you):
    user_me = request.user
    user_you = User.objects.get(id=you)
    msg = Message.objects.filter( Q(sender=user_me,receiver=user_you) | Q(sender=user_you,receiver=user_me) ).order_by("pub_date")
    params = {
        'me': user_me,
        'you': user_you,
        'msg': msg,
        'form': MessageForm(),
    }
    if request.method == 'POST':
        sender = user_me
        receiver = user_you
        content = request.POST['content']
        message = Message(sender=sender,receiver=receiver,content=content)
        message.save()
    return render(request, "myapp/talk_room.html", params)

@login_required(redirect_field_name='redirect_to')
def setting(request, num=1):
    obj = User.objects.get(id=num)
    if request.method == 'POST':
        user = UserForm(request.POST, instance=obj)
        user.save()
        return redirect(to='/friends/'+str(num))
    params = {
        'id': num,
        'form': UserForm(instance=obj),
    }
    return render(request, "myapp/setting.html", params)

@login_required(redirect_field_name='redirect_to')
def logout_view(request):
    logout(request)
    return redirect(to='/')
