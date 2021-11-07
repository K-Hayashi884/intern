from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup_view, name='signup_view'),
    path('login/',views.login.as_view(),name='login_view'),
    path('logout/',views.logout.as_view(),name='logout'),
    path('friends/', views.friends, name='friends'),
    path('talk_room/<int:reseave_user_id>', views.talk_room, name='talk_room'),
    path('setting', views.setting, name='setting'),

    path('setting/username',views.change_username,name='change_username'),
    path('change_username_done/',views.change_username_done,name='change_username_done'),

    path('setting//email',views.change_email,name='change_email'),
    path('change_email_done/',views.change_email_done,name='change_email_done'),

    path('setting//img',views.change_img,name='change_img'),
    path('change_img_done/',views.change_img_done,name='change_img_done'),

    path('setting//password',views.change_password,name='change_password'),
    path('change_password_done',views.change_password_done,name='change_password_done'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
