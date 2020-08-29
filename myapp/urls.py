from django.urls import path
from . import views
from django.contrib.auth import logout

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('friends', views.friends, name='friends'),
    path('talk_room', views.talk_room, name='talk_room'),
    path('setting', views.setting, name='setting'),
    path('logout', logout, {'template_name': 'index.html'}, name='logout'),
]
