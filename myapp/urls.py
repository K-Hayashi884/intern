from django.urls import path
from . import views
from django.contrib.auth import logout

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup_view, name='signup_view'),
    path('login', views.login_view, name='login_view'),
    path('friends', views.friends, name='friends'),
    
    # トーク画面
    # 誰とのトークかを、URLにて判別
    # ユーザー名に重複が許されていないので、ユーザー名で判別
    path('talk_room/<friend_username>/', views.talk_room, name='talk_room'),
    path('setting', views.setting, name='setting'),
    path('logout', logout, {'template_name': 'index.html'}, name='logout'),
]
