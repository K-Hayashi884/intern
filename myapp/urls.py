from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup_view, name='signup_view'),
    path('login', views.login_view, name='login_view'),
    path('friends', views.friends, name='friends'),
    path('talk_room', views.talk_room, name='talk_room'),
    path('setting', views.setting, name='setting'),
    path('change_icon', views.change_icon, name='change_icon'),
    path('change_pass', views.change_pass, name='change_pass'),
    path('change_email', views.change_email, name='change_email'),
    path('change_user', views.change_user, name='change_user'),
    path('logout',views.Logout.as_view(), name='logout_view'),
    path('change_pass_done',views.change_pass_done, name='change_pass_done'),
]