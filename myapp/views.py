from django.shortcuts import redirect, render
from .forms import SignupForm, ImageForm, LoginForm, PostForm, ChangePasswordForm, UserChangeMailForm, UserChangeNameForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from .models import UserImage, Talk
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin

def index(request):
    return render(request, "myapp/index.html")

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        imageform = ImageForm(request.POST, request.FILES)
        print(imageform.is_valid())
        if form.is_valid() and imageform.is_valid():
            user = form.save()
            user.is_active = True
            user.save()
            imageform.instance.username = user
            image = imageform.save()
            return redirect(to = '/')
        else:
           return render(request, 'myapp/signup.html', 
        {'userform': form, 'imageform': imageform}
        )
    else:
        form = SignupForm()
        imageform = ImageForm()
    return render(request, 'myapp/signup.html', 
        {'userform': form, 'imageform': imageform}
        )

class Login(LoginView):
    authentication_form = LoginForm
    template_name = 'myapp/login.html'

class Logout(LogoutView):
    template_name = 'myapp/logout.html'

class PasswordChange(PasswordChangeView):
    form_class = ChangePasswordForm
    success_url = reverse_lazy('passwordchange_done')
    template_name = 'myapp/changepassword.html'

class PasswordChangeDone(PasswordChangeDoneView):
    template_name = 'myapp/passwordchange_done.html'

class UserChangeMailView(LoginRequiredMixin, FormView):
    template_name = 'myapp/changemail.html'
    form_class = UserChangeMailForm
    success_url = reverse_lazy('index')
    
    def form_valid(self, form):
        form.update(user=self.request.user)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'email' : self.request.user.email,
        })
        return kwargs

class UserChangeNameView(LoginRequiredMixin, FormView):
    template_name = 'myapp/changename.html'
    form_class = UserChangeNameForm
    success_url = reverse_lazy('index')
    
    def form_valid(self, form):
        form.update(user=self.request.user)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'username' : self.request.user.username,
        })
        return kwargs

@login_required
def friends(request):
    friends = User.objects.exclude(username = request.user.username)
    images = UserImage.objects.all()
    messages = Talk.objects.all().order_by('-date')
    messages_user = messages.filter(Q(to_talk=request.user)|Q(from_talk=request.user))
    friendusers = []
    latestmessages = []
    for message in messages_user:
        fromuser = message.from_talk
        touser = message.to_talk
        if touser not in friendusers and fromuser == request.user:
            friendusers.append(touser)
            latestmessages.append(message)
        elif fromuser not in friendusers and touser == request.user:
            friendusers.append(fromuser)
            latestmessages.append(message)
    for p in friends:
        if p not in friendusers:
            friendusers.append(p)
    return render(request, "myapp/friends.html", {'user' : request.user, 'friends' : friendusers, 'images' : images, 'messages' : latestmessages})

@login_required
def talk_room(request, name, talkname):
    friend = User.objects.get(username = talkname)
    messages = Talk.objects.all().order_by('date')
    messages = messages.filter(Q(from_talk=friend,to_talk=request.user)|Q(from_talk=request.user,to_talk=friend))
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.instance.from_talk = User.objects.get(username = name)
            form.instance.to_talk = User.objects.get(username = talkname)
            post = form.save()
        form = PostForm()
    else:
        form = PostForm()
    friendimage = None
    useimage = None
    if UserImage.objects.filter(username = friend).exists():
            friendimage = UserImage.objects.get(username = friend)
    if UserImage.objects.filter(username = request.user).exists():
            useimage = UserImage.objects.get(username = request.user)
    params = {
        'imagef' : friendimage,
        'imageu' : useimage,
        'user' : request.user,
        'friend' : friend,
        'messages' : messages,
        'form' : form
    }
    return render(request, "myapp/talk_room.html", params)

def setting(request):
    return render(request, "myapp/setting.html", {'username' : request.user.username})

def deleteMessage(request, num):
    message = Talk.objects.get(id = num)
    if request.method == 'POST':
        message.delete()
        return redirect(to = 'friends')
    else:
        return render(request, "myapp/deleteMessage.html", {'message' : message, 'id' : num})

def editMessage(request, num):
    obj = Talk.objects.get(id = num)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=obj)
        form.save()
        return redirect(to = 'friends')
    params = {
        'message' : obj.message,
        'id' : num,
        'form' : PostForm(instance=obj)
    }
    return render(request, "myapp/editMessage.html", params)

def deleteUser(request, name):
    owner = User.objects.get(username = name)
    if request.method == 'POST':
        owner.delete()
        return redirect(to = 'index')
    else:
        return render(request, "myapp/deleteUser.html", {'name' : request.user.username})

