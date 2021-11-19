from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup_view, name='signup_view'),
    path('login', views.login_view, name='login_view'),
    path('friends', views.friends, name='friends'),
    path('talk_room/<username>', views.talk_room, name='talk_room'),
    path('setting', views.setting, name='setting'),
    path('update_username',views.update_username, name='update_username'),
    path('update_username_complete',views.update_username_complete,name="update_username_complete"),
    path('update_email',views.update_email, name='update_email'),
    path('update_email_complete',views.update_email_complete,name="update_email_complete"),
    path('update_image',views.update_image, name='update_image'),
    path('update_image_complete',views.update_image_complete,name="update_image_complete"),
    path('update_password',views.update_password, name='update_password'),
    path('update_password_complete',views.update_password_complete,name="update_password_complete"),
]



