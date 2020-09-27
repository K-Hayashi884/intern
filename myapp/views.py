from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from .forms import SignUpForm
from .forms import LoginForm
from .forms import TalkForm
from .forms import PasswordChangeForm
from .forms import NameChangeForm
from .forms import EmailChangeForm
from .forms import IconChangeForm
from .forms import HeaderChangeForm
from .forms import Prof_msgChangeForm
from django.contrib.auth import authenticate, get_user, login
from .models import User, UserImage, Talk, HeaderImage, prof_msg
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView
import datetime
from django.db.models import Q, Value, Subquery, OuterRef
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, UpdateView
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import logout



def index(request):
    return render(request, "myapp/index.html")

def talklist_view(request):
    user = request.user
    user_imgs = UserImage.objects.exclude(user=user)
    latest_msg = Talk.objects.filter(
        Q(person_from=OuterRef("pk"), person_to=user) | Q(person_from=user, person_to=OuterRef("pk"))
    ).order_by('-time')
    user_qs =(User.objects.exclude(username=user.username).annotate(
        latest_msg_id=Subquery(
            latest_msg.values("pk")[:1]
        ),
        latest_msg_content=Subquery(
                    latest_msg.values("talk")[:1]
        ),
        latest_msg_time=Subquery(
                    latest_msg.values("time")[:1]
        ),
    ).order_by("latest_msg_id")
    )
    params = {
        "user":user,
        "user_imgs":user_imgs,
        "user_qs":user_qs,
    }
    return render(request, "myapp/talklist.html", params)

def signup_view(request):
    if request.method == "GET":
        signup_form = SignUpForm()
    elif request.method == "POST":
        signup_form = SignUpForm(request.POST, request.FILES)
        if signup_form.is_valid():
            signup_form.save()
            username = signup_form.cleaned_data['username']
            email = signup_form.cleaned_data['email']
            password = signup_form.cleaned_data['password1']
            image = signup_form.cleaned_data['image']
            user = authenticate(username=username, password=password)
            login(request, user)
            user = User.objects.get(username=username)
            user_img = UserImage(
               user=user,
               image=image,
            )
            user_img.save()
            #Register prof_msg and HeaderImage with Null in advance
            user_prof_msg = prof_msg(
                user=user,
            )
            user_prof_msg.save()
            user_header_img = HeaderImage(
                user=user,
            )
            user_header_img.save()
            return redirect(to="/")
    params = {
        "form":signup_form
    }
    return render(request, "myapp/signup.html", params)

class Login(LoginView):
    form_class = LoginForm
    template_name= 'myapp/login.html'

#I wanna make a friend-list
def friends(request):
    me = request.user
    #自分と友人は分けて表示したいので、別々に作成
    me_msg = prof_msg.objects.get(user=me)
    me_info = []
    me_info.append([me, me.username, me_msg])
    users = User.objects.exclude(username=me.username)
    prof_msgs = prof_msg.objects.exclude(user=me)
    user_imgs = UserImage.objects.all()
    user_info = []
    for user in users:
        try:
            user_info.append([user, user.username])
        except:
            user_info.append([user, user.username])
    user_info = sorted(user_info, key=lambda x: x[1])
    params = {
        "me_info":me_info,
        "user_imgs":user_imgs,
        "user_info":user_info,
        "prof_msgs":prof_msgs
    }
    return render(request, "myapp/friends.html", params)

def talk_room(request, partner_name):
    myname = request.user.username
    user = User.objects.get(username=myname)
    partner = User.objects.get(username=partner_name)
    form = TalkForm()
    history = Talk.objects.filter(Q(person_from=user, person_to=partner) | Q(person_from=partner, person_to=user))
    history = history.order_by('time')
    params = {
        "user":user,
        "partner":partner,
        "form":form,
        "history":history,
    }

    if request.method == "POST":
        post = TalkForm(request.POST)
        if post.is_valid():
            text = post.cleaned_data['talk']
            date = datetime.datetime.now()
            message = Talk(talk=text, time=date, person_from=user, person_to=partner)
            message.save()

    return render(request, "myapp/talk_room.html", params)

def setting(request):
    return render(request, "myapp/setting.html")


class PasswordChange(PasswordChangeView):
   form_class = PasswordChangeForm
   success_url = 'success/password'
   template_name = 'myapp/change_pass.html'

class PasswordChangeDone(PasswordChangeDoneView):
   template_name = 'myapp/change_success.html'

class NameChangeView(LoginRequiredMixin, FormView):
    template_name = 'myapp/change_name.html'
    form_class = NameChangeForm
    success_url = 'success/username'
    
    def form_valid(self, form):
        #formのupdateメソッドにログインユーザーを渡して更新
        form.name_update(user=self.request.user)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # 更新前のユーザー情報をkwargsとして渡す
        kwargs.update({
            'username' : self.request.user.username,
        })
        return kwargs

class IconChangeView(LoginRequiredMixin, FormView):
    template_name = 'myapp/change_icon.html'
    form_class = IconChangeForm
    success_url = 'success/icon'
    
    def form_valid(self, form):
        #formのupdateメソッドにログインユーザーを渡して更新
        form.icon_update(user=self.request.user)
        return super().form_valid(form)

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     myname = self.request.user.username
    #     user = User.objects.get(username=myname)
    #     user_img = UserImage.objects.get(user=user)
    #     kwargs.update({
    #         'image' : user_img,
    #     })
    #     return kwargs

class HeaderChangeView(LoginRequiredMixin, FormView):
    template_name = 'myapp/change_header.html'
    form_class = HeaderChangeForm
    success_url = 'success/header'
    
    def form_valid(self, form):
        #formのupdateメソッドにログインユーザーを渡して更新
        form.header_update(user=self.request.user)
        return super().form_valid(form)

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     myname = self.request.user.username
    #     user = User.objects.get(username=myname)
    #     user_img = UserImage.objects.get(user=user)
    #     kwargs.update({
    #         'image' : user_img,
    #     })
    #     return kwargs

class EmailChangeView(LoginRequiredMixin, FormView):
    template_name = 'myapp/change_mail.html'
    form_class = EmailChangeForm
    success_url = 'success/email'
    
    def form_valid(self, form):
        #formのupdateメソッドにログインユーザーを渡して更新
        form.email_update(user=self.request.user)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # 更新前のユーザー情報をkwargsとして渡す
        kwargs.update({
            'email' : self.request.user.email,
        })
        return kwargs

class Prof_msgChangeView(LoginRequiredMixin, FormView):
    template_name = 'myapp/change_prof_msg.html'
    form_class = Prof_msgChangeForm
    success_url = 'success/Profile message'
    
    def form_valid(self, form):
        #formのupdateメソッドにログインユーザーを渡して更新
        form.prof_msg_update(user=self.request.user)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        msg = prof_msg.objects.get(user=self.request.user).prof_msg
        if msg:
        # 更新前のユーザー情報をkwargsとして渡す
            kwargs.update({
                'prof_msg' : msg,
            })
        return kwargs
        

def change_success(request, name):
    params = {
        "name":name,
    }
    return render(request, "myapp/change_success.html", params)

def logout_view(request):
    logout(request)
    return render(request,"myapp/index.html")

def profile(request, myname):
    myname = myname
    page_owner = User.objects.get(username=myname)
    icon = UserImage.objects.get(user=page_owner)
    header = HeaderImage.objects.get(user=page_owner)
    params = {
        'myname':myname,
        'icon':icon,
        'header':header,
    }
    return render(request, "myapp/profile.html", params)