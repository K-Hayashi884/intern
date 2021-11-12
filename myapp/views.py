from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.shortcuts import redirect, render
from .forms import EmailChangeForm, ImageChangeForm, MessageForm, SignupForm, LoginForm, PasswordChangeForm, UsernameChangeForm
from .models import Message, User
from django.db.models import Q
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

def index(request):
    parameters = {}
    return render(request, "myapp/index.html", parameters)

def signup(request):
    parameters = {}
    if request.method == 'GET':
        parameters['form'] = SignupForm()
    elif request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid(): # <-これいる？
            form.save()
            return redirect(to="/")
        parameters['form'] = form
    return render(request, "myapp/signup.html", parameters)


class login(LoginView):   
    form_class = LoginForm
    template_name = "myapp/login.html"

class logout(LogoutView, LoginRequiredMixin):
    pass

@login_required
def friends(request):
    parameters = {}
    parameters['friends'] = User.objects.filter(~Q(username=request.user.username))
    return render(request, "myapp/friends.html", parameters)

@login_required
def talk_room(request, partner):
    parameters = {}
    user = request.user.username
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = Message(
                sender=user, \
                receiver=partner, \
                contents=form.cleaned_data['contents']
            )
            message.save()
    parameters['messages'] = Message.objects.filter((Q(sender=partner) & Q(receiver=user)) | (Q(sender=user) & Q(receiver=partner)))
    parameters['form'] = MessageForm()
    parameters['partner'] = partner
    return render(request, "myapp/talk_room.html", parameters)

@login_required
def setting(request):
    return render(request, "myapp/setting.html")

def Form(item):
    if item == 'username':
        return UsernameChangeForm
    elif item == 'image':
        return ImageChangeForm
    elif item == 'email':
        return EmailChangeForm
    else:
        return "invalid"

@login_required
def change(request, item):
    parameters = {}
    user = request.user

    if Form(item) == "invalid":
        return HttpResponse("This URL has not been registered.")

    if request.method == 'GET':
        parameters['form'] = Form(item)(instance=user)
    elif request.method == 'POST':
        if item == 'image':
            form = Form(item)(request.POST, request.FILE, instance=user)
        else:
            form = Form(item)(request.POST, instance=user)
        
        if form.is_valid():
            form.save()
            return redirect("done/"+item)
    
    parameters['item'] = item
    return render(request, "myapp/change.html", parameters)

class password_change(PasswordChangeView, LoginRequiredMixin):
    form_class = PasswordChangeForm
    success_url = reverse_lazy("myapp:change_done", kwargs={'item':'password'})
    template_name = "myapp/password_change.html"

@login_required
def change_done(request, item):
    parameters = {}
    parameters['item'] = item
    return render(request, "myapp/change_done.html", parameters)
