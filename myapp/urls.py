from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup_view, name='signup_view'),
    path('login', views.Login.as_view(), name='login_view'),
    path('friends', views.friends, name='friends'),
    path('talk_room/<str:tousername>', views.talk_room, name='talk_room'),
    path('setting', views.setting, name='setting'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('usernamechange/<str:fromusername>', views.usernamechange, name='usernamechange'),
    path('usernameok', views.usernameok, name='usernameok'),
    path('emailchange/<str:fromusername>', views.emailchange, name='emailchange'),
    path('emailok', views.emailok, name='emailok'),
    path('passwordchange/<str:fromusername>', views.passwordchange, name='passwordchange'),
    path('passwordok', views.passwordok, name='passwordok'),
    path('iconchange/<str:fromusername>', views.iconchange, name='iconchange'),
    path('iconok', views.iconok, name='iconok')
]