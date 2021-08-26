from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('signup', views.Signup_View.as_view(), name='signup_view'),
    path('login', views.Login_View.as_view(), name='login_view'),
    path('friends', views.friends, name='friends'),
    path('talk_room/<int:id>', views.talk_room, name='talk_room'),
    path('setting', views.setting, name='setting'),
    path('edit_username', views.edit_username, name='edit_username'),
    path('edit_username_done', views.edit_username_done, name='edit_username_done'),
    path('edit_email', views.edit_email, name='edit_email'),
    path('edit_email_done', views.edit_email_done, name='edit_email_done'),
    path('edit_icon', views.edit_icon, name='edit_icon'),
    path('edit_icon_done', views.edit_icon_done, name='edit_icon_done'),
    path('pass_change/', views.PasswordChange.as_view(), name='pass_change'),
    path('pass_change/done', views.PasswordChangeDone.as_view(), name='pass_change_done'),
    path('logout/', views.Logout.as_view(), name='logout')
]
