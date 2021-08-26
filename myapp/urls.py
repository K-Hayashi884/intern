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
    path('user_name_change', views.user_name_change, name='user_name_change'),
    path('user_email_change', views.user_email_change, name='user_email_change'),
    path('user_password_change', views.user_password_change, name='user_password_change'),
    path('user_image_change', views.user_image_change, name='user_image_change'),
    path('changecompleted', views.changecompleted, name='changecompleted'),
]