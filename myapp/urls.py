from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup_view, name='signup'),
    path("login", views.Login.as_view(), name="login"),
    path('friends', views.friends, name='friends'),

    # トーク画面
    # 誰とのトークかを、URLにて判別
    # ユーザー名に重複が許されていないので、ユーザー名で判別
    path("talk_room/<int:user_id>/", views.talk_room, name="talk_room"),
    path('setting', views.setting, name='setting'),
    path("logout/", views.Logout.as_view(), name="logout"),
]
