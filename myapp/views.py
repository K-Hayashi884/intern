import json

from django.contrib import messages
from django.contrib.auth import login,logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from django.db.models import Q,Value,Subquery,OuterRef,Count
from django.http import HttpResponse,JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.utils.safestring import mark_safe

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
                return redirect('/friends/')
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
    # print("b")
    me = request.user
    form = FindForm(request.POST or None)
    latest_msg = Message.objects.filter( Q(sender=OuterRef("pk"),receiver=me) | Q(sender=me,receiver=OuterRef("pk")) ).order_by('-pub_date')
    # if request.method == 'POST':
    #     find = request.POST['find']
    #     print("here")
    #     user_qs = User.objects.exclude(id=me.id).annotate(
    #         latest_msg_id=Subquery(
    #             latest_msg.values("pk")[:1]
    #         ),
    #         latest_msg_content=Subquery(
    #             latest_msg.values("content")[:1]
    #         ),
    #         latest_msg_pub_date=Subquery(
    #             latest_msg.values("pub_date")[:1]
    #         ),
    #         q_count = Count("id",filter(username__contains=find))
    #     ).order_by("-q_count","-latest_msg_id")
        # user = User.objects.exclude(username__contains=find).annotate(
        #     latest_msg_id=Subquery(
        #         latest_msg.values("pk")[:1]
        #     ),
        #     latest_msg_content=Subquery(
        #         latest_msg.values("content")[:1]
        #     ),
        #     latest_msg_pub_date=Subquery(
        #         latest_msg.values("pub_date")[:1]
        #     ),
        # ).order_by("-latest_msg_id")
    #     found_user = []
    #     for found in found_qs:
    #         found_user.append(found)
    #     found_user.reverse()
    # else:
    # print("a")
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
    # for user in user_qs:
    #     if len(user["latest_msg_content"]) > 20:
    #         user["latest_msg_content"]=user["latest_msg_content"]+"..."
    page = Paginator(user_qs,30)
        # form = FindForm()
        # msg = Message.objects.order_by("pub_date")
        # user_qs = User.objects.all()
        # user_msg_dict = {}
        # for u in user_qs:
        #     last_msg_date = u.message_sender.all().last().pub_date
        #     user_msg_dict[u] = last_msg_date


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
    params = {
        'form': form,
        'data': page.get_page(num),
        'me': me,
    }
    return render(request, "myapp/friends.html", params)

def search_user(request):
    me=request.user
    print("this")
    q = request.GET.get("q","")
    latest_msg = Message.objects.filter( Q(sender=OuterRef("pk"),receiver=me) | Q(sender=me,receiver=OuterRef("pk")) ).order_by('-pub_date')
    #user_qs = User.objects.filter(username__contains=q)
    user_qs = User.objects.exclude(id=me.id).annotate(
            latest_msg_id=Subquery(
                latest_msg.values("pk")[:1]
            ),
            latest_msg_content=Subquery(
                latest_msg.values("content")[:1]
            ),
            latest_msg_pub_date=Subquery(
                latest_msg.values("pub_date")[:1]
            ),
            q_count = Count("id",filter=(Q(username__contains=q)))
        ).order_by("-q_count","-latest_msg_id")
    print("beforejson")
    user_json = serializers.serialize('json',user_qs)
    #print(user_json)
    print("end")
    return HttpResponse(user_json, content_type='application/json')

@login_required(redirect_field_name='redirect_to')
def talk_room(request, you=1):
    user_me = request.user
    my_name = str(user_me.username)
    user_you = User.objects.get(id=you)
    msg = Message.objects.filter( Q(sender=user_me,receiver=user_you) | Q(sender=user_you,receiver=user_me) ).order_by("pub_date")
    if user_me.id < user_you.id:
        room_name = str(user_me.id) + '_' + str(user_you.id)
    else:
        room_name = str(user_you.id) + '_' + str(user_me.id)
    params = {
        'me': user_me,
        'you': user_you,
        'my_name_json': mark_safe(json.dumps(my_name)),
        'msg': msg,
        'room_name_json': mark_safe(json.dumps(room_name)),
        'form': MessageForm(),
    }
    # if request.method == 'POST':
    #     sender = user_me
    #     receiver = user_you
    #     content = request.POST['content']
    #     message = Message(sender=sender,receiver=receiver,content=content)
    #     message.save()
    return render(request, "myapp/talk_room.html", params)

@login_required(redirect_field_name='redirect_to')
def setting(request):
    obj = request.user
    if request.method == 'POST':
        user = UserForm(request.POST, instance=obj)
        user.save()
        return redirect(to='/friends/')
    params = {
        'form': UserForm(instance=obj),
    }
    return render(request, "myapp/setting.html", params)

@login_required(redirect_field_name='redirect_to')
def logout_view(request):
    logout(request)
    return redirect(to='/')
