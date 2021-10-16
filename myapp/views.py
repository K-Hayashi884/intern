from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.views import generic
from .models import User
from .forms import UserForm
from django.urls import reverse_lazy
from django.views.generic import CreateView


def index(request):
    return render(request, "myapp/index.html")

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


def login_view(request):
    return render(request, "myapp/login.html")

def friends(request):
    return render(request, "myapp/friends.html")

def talk_room(request):
    return render(request, "myapp/talk_room.html")

def setting(request):
    return render(request, "myapp/setting.html")
