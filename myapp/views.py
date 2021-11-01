from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.db.models import Subquery, OuterRef, Q
from .models import User, Talk
from .forms import SignupForm, LoginForm


def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST, request.FILES, instance=User())
        if form.is_valid():
            form.save()
            return redirect(to='/')
        else:
            return render(request, "myapp/signup.html", {'form': form})
    return render(request, "myapp/signup.html", {'form': SignupForm()})

class login_view(LoginView):
    form_class = LoginForm
    template_name = 'myapp/login.html'    

@login_required
def friends(request):
    user = request.user
    print(user, user.id)
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

def talk_room(request, pk):
    return render(request, "myapp/talk_room.html")

def setting(request):
    return render(request, "myapp/setting.html")
