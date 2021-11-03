from django.shortcuts import redirect, render
from .forms import SignupForm
from .models import User

def index(request):
    parameters = {}
    parameters['signup'] = 'signup_view'
    return render(request, "myapp/index.html", parameters)

def signup_view(request):
    parameters = {}
    if request.method == 'GET':
        parameters['form'] = SignupForm()
        return render(request, "myapp/signup.html", parameters)
    elif request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data #どうしてこれ成功するんだ？？？
            user = User(
                username = cd['username'], \
                email = cd['email'], \
                password = cd['password1'], \
                image = cd['image'],
            )
            user.save()
            return redirect(to="/")
        parameters['form'] = SignupForm(request.POST, request.FILES)
        return render(request, "myapp/signup.html", parameters)


def login_view(request):
    return render(request, "myapp/login.html")

def friends(request):
    return render(request, "myapp/friends.html")

def talk_room(request):
    return render(request, "myapp/talk_room.html")

def setting(request):
    return render(request, "myapp/setting.html")
