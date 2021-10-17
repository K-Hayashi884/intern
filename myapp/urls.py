from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('index', views.index, name='index'),
    path('signup', views.ImageView.as_view(), name='signup_view'),
    path('login/', LoginView.as_view(redirect_authenticated_user=True, template_name='myapp/login.html'), name='login_view'),
    path('friends', views.friends, name='friends'),
    path('talk_room', views.talk_room, name='talk_room'),
    path('setting', views.setting, name='setting'),
]

