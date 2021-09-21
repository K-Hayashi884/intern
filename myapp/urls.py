from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup_view, name='signup_view'),
    path('login', views.Login.as_view(), name='login_view'),
    path('friends', views.friends, name='friends'),
    path('talk_room/<friend_username>', views.talk_room, name='talk_room'),
    path('setting', views.setting, name='setting'),
    path('logout',views.Logout.as_view(), name='logout_view'),
    path('change_username',views.change_username,name='change_username'),
    path('change_mail',views.change_mail,name='change_mail'),
    path('change_icon',views.change_icon,name='change_icon'),
    path('change_password',views.PasswordChange.as_view(),name='change_password'),
    path('change_username_complete',views.change_username_complete,name='change_username_complete'),
    path('change_icon_complete',views.change_icon_complete,name='change_icon_complete'),
    path('change_mail_complete',views.change_mail_complete,name='change_mail_complete'),
    path('change_password_complete',views.change_password_complete,name='change_password_complete'),
]
