from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup_view, name='signup_view'),
    path('login', views.login_view, name='login_view'),
    path('friends', views.friends, name='friends'),
    path('talk_room/<int:num>', views.talk_room, name='talk_room'),
    #setting
    path('setting', views.setting, name='setting'),
    path('setting/change_username', views.change_username, name='setting/change_username'),
    path('setting/change_mail', views.change_mail, name='setting/change_mail'),
    path('setting/change_icon', views.change_icon, name='setting/change_icon'),
    path('setting/password_change', views.PasswordChange.as_view(), name='setting/password_change'),
    path('setting/password_change_done', views.PasswordChangeDone.as_view(), name='setting/password_change_done'),
    path('setting/complete', views.complete, name='setting/complete'),
    path('logout',  views.logout_view, name='logout_view'),
]