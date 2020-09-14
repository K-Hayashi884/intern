import json
from django.contrib import messages
from django.contrib.auth import login,logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from django.db.models import Q
from django.http import HttpResponse,JsonResponse
from django.shortcuts import redirect, render, get_object_or_404

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
def friends(request, num=1):
    if request.method == 'POST':
        form = FindForm(request.POST)
        find = request.POST['find']
        found_qs = User.objects.filter(username__contains=find)
        user = User.objects.exclude(username__contains=find)
        found_user = []
        for found in found_qs:
            found_user.append(found)
        found_user.reverse()
    else:
        form = FindForm()
        found_user = []
        user = User.objects.all()
    me = User.objects.get(id=num)
    msg = []
    sorted_user = []
    unsorted_found_msg = []
    unsorted_found_no_msg = []
    unsorted_user_msg = []
    unsorted_user_no_msg = []
    for friend in found_user:
        message = Message.objects.filter( Q(sender=friend,receiver=me) | Q(sender=me,receiver=friend) ).order_by("-pub_date")
        if(len(message)>0):
            msg.append(message[0])
            unsorted_found_msg.append({'user': friend, 'latest': message[0].pub_date})
        else:
            unsorted_found_no_msg.append({'user': friend, 'id': -friend.id})
    for friend in user:
        message = Message.objects.filter( Q(sender=friend,receiver=me) | Q(sender=me,receiver=friend) ).order_by("-pub_date")
        if(len(message)>0):
            msg.append(message[0])
            unsorted_user_msg.append({'user': friend, 'latest': message[0].pub_date})
        else:
            unsorted_user_no_msg.append({'user': friend, 'id': -friend.id})
    unsorted_found_msg.sort(key=lambda x: x['latest'])
    unsorted_found_msg.reverse()
    unsorted_found_no_msg.sort(key=lambda x: x['id'])
    unsorted_user_msg.sort(key=lambda x: x['latest'])
    unsorted_user_msg.reverse()
    unsorted_user_no_msg.sort(key=lambda x: x['id'])
    for ob in unsorted_found_msg:
        sorted_user.append(ob['user'])
    for ob in unsorted_found_no_msg:
        sorted_user.append(ob['user'])
    for ob in unsorted_user_msg:
        sorted_user.append(ob['user'])
    for ob in unsorted_user_no_msg:
        sorted_user.append(ob['user'])
    params = {
        'form': form,
        'id': num,
        'user': sorted_user,
        'msg': msg,
        'me': me,
    }
    return render(request, "myapp/friends.html", params)

def search_user(request):
    # num = request.user.id
    find = request.GET.get('q','')
    user_list = User.objects.filter(username__contains=find)
    # found_qs = User.objects.filter(username__contains=find)
    # user = User.objects.exclude(username__contains=find)
    # found_user = []
    # for found in found_qs:
    #     found_user.append(found)
    # found_user.reverse()
    # me = User.objects.get(id=num)
    # msg = []
    # sorted_user = []
    # unsorted_found_msg = []
    # unsorted_found_no_msg = []
    # unsorted_user_msg = []
    # unsorted_user_no_msg = []
    # for friend in found_user:
    #     message = Message.objects.filter( Q(sender=friend,receiver=me) | Q(sender=me,receiver=friend) ).order_by("-pub_date")
    #     if(len(message)>0):
    #         msg.append(message[0])
    #         unsorted_found_msg.append({'user': friend, 'latest': message[0].pub_date})
    #     else:
    #         unsorted_found_no_msg.append({'user': friend, 'id': -friend.id})
    # for friend in user:
    #     message = Message.objects.filter( Q(sender=friend,receiver=me) | Q(sender=me,receiver=friend) ).order_by("-pub_date")
    #     if(len(message)>0):
    #         msg.append(message[0])
    #         unsorted_user_msg.append({'user': friend, 'latest': message[0].pub_date})
    #     else:
    #         unsorted_user_no_msg.append({'user': friend, 'id': -friend.id})
    # unsorted_found_msg.sort(key=lambda x: x['latest'])
    # unsorted_found_msg.reverse()
    # unsorted_found_no_msg.sort(key=lambda x: x['id'])
    # unsorted_user_msg.sort(key=lambda x: x['latest'])
    # unsorted_user_msg.reverse()
    # unsorted_user_no_msg.sort(key=lambda x: x['id'])
    # for ob in unsorted_found_msg:
    #     sorted_user.append(ob['user'])
    # for ob in unsorted_found_no_msg:
    #     sorted_user.append(ob['user'])
    # for ob in unsorted_user_msg:
    #     sorted_user.append(ob['user'])
    # for ob in unsorted_user_no_msg:
    #     sorted_user.append(ob['user'])
    # for u in sorted_user:
    #     print(u)
    # params = {
    #     'id': num,
    #     'user': sorted_user,
    #     'msg': msg,
    #     'me': me,
    # }
    user_json = serializers.serialize('json',user_list)
    user_data = [
        {
            'id':user.id,
            'name':user.username,
        }
        for user in user_list
    ]
    return JsonResponse({'user_data':user_data})

@login_required(redirect_field_name='redirect_to')
def talk_room(request, me=1, you=2):
    user_me = User.objects.get(id=me)
    user_you = User.objects.get(id=you)
    msg = Message.objects.filter( Q(sender=user_me,receiver=user_you) | Q(sender=user_you,receiver=user_me) ).order_by("pub_date")
    params = {
        'id': me,
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
