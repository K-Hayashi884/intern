from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup_view'),
    path('login', views.Login.as_view(), name='login_view'),
    path('logout', views.Logout.as_view(), name='logout_view'),
    path('changepassword', views.PasswordChange.as_view(), name='changepass'), 
    path('passwordchange_done', views.PasswordChangeDone.as_view(), name='passwordchange_done'), 
    path('friends', views.friends, name='friends'),
    path('setting', views.setting, name='setting'),
    path('talk/<name>/<talkname>', views.talk_room, name='talk_room'),
    path('changemail', views.UserChangeMailView.as_view(), name="changemail"),
    path('changename', views.UserChangeNameView.as_view(), name="changename"),
    path('deleteMessage/<num>', views.deleteMessage, name="deleteMessage"),
    path('editMessage/<num>', views.editMessage, name="editMessage"),
    path('deleteUser/<name>', views.deleteUser, name="deleteUser"),
]
