from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup_view, name='signup_view'),
    path('login', views.login_view.as_view(), name='login_view'),
    path('friends', views.friends, name='friends'),
    path('talk_room/<int:user_id>', views.talk_room, name='talk_room'),
    path('setting', views.setting, name='setting'),
    path('setting/name', views.set_name, name='name'),
    path('setting/mail', views.set_mail, name='mail'),
    path('setting/icon', views.set_icon, name='icon'),
    path('setting/password', views.set_password.as_view(), name='password'),
    path('logout', views.logout_view.as_view(), name='logout_view'),
    path('notification',views.notification,name='notification'),
]
