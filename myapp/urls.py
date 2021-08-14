from django.urls import path
from . import views
#from django.contrib import admin
from django.urls import path
from django.conf import settings 
from django.conf.urls.static import static 

urlpatterns = [
    path('', views.index, name='index'),    
    path('signup', views.signup_view, name='signup_view'),
    path('login', views.login_view, name='login_view'), #★
    #path('accounts/logout/', views.Logout.as_view, name='logout_view'), #★
    path('friends', views.friends, name='friends'),
    path('talk_room/<int:num>', views.talk_room, name='talk_room'),
    path('setting', views.setting, name='setting'),
    path('usernamechange', views.user_name_change, name='user_name_change'),
    path('changecompleted', views.user_change_done, name='user_change_done'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)