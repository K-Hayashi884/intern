from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup_view, name='signup_view'),
    path('login', auth_views.LoginView.as_view(template_name='myapp/login.html'),
        name='login_view'),
    path('logout', auth_views.LogoutView.as_view(template_name='myapp/logout.html'),
        name='logout_view'),
    path('friends', views.friends, name='friends'),
    path('talk_room/<str:room_name>', views.talk_room, name='talk_room'),
    path('setting', views.setting, name='setting'),
    path('username_change', views.username_change, name='username_change'),
    path('username_change_done', views.username_change, name='username_change_done'),
    path('email_change', views.email_change, name='email_change'),
    path('email_change_done', views.email_change, name='email_change_done'),
    path('user_img_change', views.user_img_change, name='user_img_change'),
    path('user_img_change_done', views.user_img_change, name='user_img_change_done'),
    path('password_change/', views.PasswordChange.as_view(), name='password_change'),
    path('password_change_done/', views.PasswordChangeDone.as_view(), name='password_change_done'),
]