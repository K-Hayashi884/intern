from django.urls import path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    re_path('accounts/confirm-email', views.confirm_email, name='confirm-email'),
    path('friends', views.friends, name='friends'),
    path('friends/<int:num>', views.friends, name='friends'),
    path('talk_room/<int:num>', views.talk_room, name='talk_room'),
    path('setting', views.setting, name='setting'),
    path('setting/username', views.change_username, name='change_username'),
    path('setting/username/done', views.change_username_done, name='change_username_done'),
    path('setting/email', views.change_email, name='change_email'),
    path('setting/email/done', views.change_email_done, name='change_email_done'),
    path('setting/icon', views.change_icon, name='change_icon'),
    path('setting/icon/done', views.change_icon_done, name='change_icon_done'),
    path('setting/password', views.PasswordChange.as_view(), name='change_password'),
    path('setting/password/done', views.PasswordChangeDone.as_view(), name='password_change_done'),
]
urlpatterns  += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
