from django import forms
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.views import generic
from .models import User, Message
from .forms import MessageForm, UserForm
from django.urls import reverse_lazy
from django.views.generic import CreateView


def index(request):
    print(request.user)
    return render(request, "myapp/index.html")

# これは使わない
def signup_view(request):
    params = {
        'form' : UserForm(),
        'message' : '' ,
    }
    if(request.method == 'POST'):
        obj = User()
        user = UserForm(request.POST, instance=obj)
        if(user.is_valid()):
            user.save()
            return redirect(to='/index')
        else:
            params['message'] = 'no good'
            print('no ')
    return render(request, "myapp/signup.html", params)

# これでサインアップする
class ImageView(CreateView):
    model = User
    template_name = 'myapp/signup.html'
    form_class = UserForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        users = form.save(commit=False)
        users.user = self.request.user
        users.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        
        return super().form_invalid(form)


# def login_view(request):
    # return render(request, "myapp/login.html")

def friends(request):
    login_user_id = request.user.id
    friends = User.objects.exclude(id=login_user_id).order_by('id').reverse()
    params = {
        'friends' : friends,
    }
    return render(request, "myapp/friends.html", params)

def talk_room(request, user_id):
    
    friend = User.objects.get(id=user_id)
    path = request.path
    params = {
        'friend' : friend,
        'form' : MessageForm,
        'path' : path,
    }
    
    if request.method == 'POST':
        obj = Message()
        message = MessageForm(request.POST, instance=obj)
        if message.is_valid():
            message.instance.friend = friend
            message.save()
            print('success')
        else: 
            print('why')
    return render(request, "myapp/talk_room.html", params)

def setting(request):
    return render(request, "myapp/setting.html")
