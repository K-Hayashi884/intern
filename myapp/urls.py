from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup_view, name='signup_view'),
    # path('login', views.login_view, name='login_view'),
    path('login', views.Login.as_view(), name='login_view'),
    path('friends', views.friends, name='friends'),
    path('talk_room/<partner_name>', views.talk_room, name='talk_room'),
    path('setting', views.setting, name='setting'),
    path('change_name', views.change_name, name='change_name'),
    path('change_mail', views.change_mail, name='change_mail'),
    path('change_icon', views.change_icon, name='change_icon'),
    path('change_pass', views.PasswordChange.as_view(), name='change_pass'),
    path('success/<name>', views.change_success, name='change_success'),
    path('logout', views.logout, name='logout'),
]
