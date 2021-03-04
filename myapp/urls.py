from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup_view, name='signup_view'),
    path('login', views.login_view, name='login_view'),
    path('friends', views.friends, name='friends'),
    path('talk_room/<friend_user>', views.talk_room, name='talk_room'),
    path('setting', views.setting, name='setting'),
    path('logout', auth_views.LogoutView.as_view(), name="logout"),
    path('setting/change_username/<change_name>', views.change_username, name='change_username'),
    path('setting/change_mail', views.change_mail, name='change_mail'),
    path('setting/change_icon', views.change_icon, name='change_icon'),
    path('setting/done_username', views.done_username, name='done_username'),
    path('setting/done_mail', views.done_mail, name='done_mail'),
    path('setting/done_icon', views.done_icon, name='done_icon'),
    path('setting/change_password/', views.PasswordChange.as_view(), name='change_password'),
    path('setting/done_password/', views.PasswordChangeDone.as_view(), name='done_password'),
]


