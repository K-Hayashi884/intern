from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup_view, name='signup_view'),
    path('login', auth_views.LoginView.as_view(template_name='myapp/login.html'),
        name='login_view'),
    path('friends', views.friends, name='friends'),
    path('talk_room', views.talk_room, name='talk_room'),
    path('setting', views.setting, name='setting'),
]
