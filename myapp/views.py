from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.db.models import Subquery, OuterRef, Q
from .models import User, Talk
from .forms import SignupForm, LoginForm, TalkForm


def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST, request.FILES, instance=User())
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            return render(request, "myapp/signup.html", {'form': form})
    return render(request, "myapp/signup.html", {'form': SignupForm()})

class login_view(LoginView):
    form_class = LoginForm
    template_name = 'myapp/login.html'    

@login_required
def friends(request):
    user = request.user
    latest_talks = Talk.objects.filter(
        Q(from_user=user, to_user=OuterRef('pk'))
        | Q(from_user=OuterRef('pk'), to_user=user),
    ).order_by('-sent_time')
    #print(latest_talks)
    friend_list = User.objects.exclude(id=user.id).annotate(
        latest_msg=Subquery(latest_talks.values('message')[:1]),
        latest_sent_time=Subquery(latest_talks.values('sent_time')[:1]),
    ).order_by('-latest_sent_time', '-date_joined')
    return render(request, "myapp/friends.html", {'data': friend_list})

@login_required
def talk_room(request, pk):
    user1 = request.user
    user2 = User.objects.get(id=pk)
    message_list = Talk.objects.filter(
        Q(from_user=user1, to_user=user2)
        | Q(from_user=user2, to_user=user1)
    ).order_by('sent_time')

    if request.method == 'POST':
        talk = Talk(from_user=user1, to_user=user2)
        form = TalkForm(request.POST, instance=talk)
        if form.is_valid():
            form.save()
            redirect('talk_room', pk)

    params = {
        'form': TalkForm(),
        'data': message_list,
        'user2_name': user2.username
    }

    return render(request, "myapp/talk_room.html", params)

def setting(request):
    return render(request, "myapp/setting.html")
