from django.urls import path, include
from . import views

urlpatterns = [
    path('index', views.IndexView.as_view(), name='index'),
    path('friends', views.friends, name='friends'),
    path('talk_room/<str:room_path>', views.talk_room, name='talk_room'),
    path('setting', views.SettingView.as_view(), name='setting'),
    path('edit_username', views.edit_username, name='edit_username'),
    path('edit_username_done', views.edit_username_done, name='edit_username_done'),
    path('edit_icon', views.edit_icon, name='edit_icon'),
    path('edit_icon_done', views.edit_icon_done, name='edit_icon_done'),
    path('pass_change/', views.PasswordChange.as_view(), name='pass_change'),
    path('pass_change/done', views.PasswordChangeDone.as_view(), name='pass_change_done'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('accounts/', include('allauth.urls'))
]
