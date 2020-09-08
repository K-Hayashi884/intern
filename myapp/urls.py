from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup_view, name='signup_view'),
    path('login', views.login_view, name='login_view'),
    path('friends', views.friends, name='friends'),
    path('friends/<int:num>', views.friends, name='friends'),
    path('talk_room', views.talk_room, name='talk_room'),
    path('talk_room/<int:me>/<int:you>', views.talk_room, name='talk_room'),
    path('setting', views.setting, name='setting'),
    path('setting/<int:num>', views.setting, name='setting'),
    path('logout/', views.logout_view, name='logout'),
]
