from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup_view, name='signup_view'),
    path('login', views.login_view.as_view(), name='login_view'),
    path('friends', views.friends, name='friends'),
    path('talk_room/<int:pk>', views.talk_room, name='talk_room'),
    path('setting', views.setting, name='setting'),
    path('change_username', views.change_username, name='change_username'),
    path('change_email', views.change_email, name='change_email'),
    path('change_icon', views.change_icon, name='change_icon'),
    path('change_password', views.change_password.as_view(), name='change_password'),
    path('change_username_done', views.change_username_done, name='change_username_done'),
    path('change_email_done', views.change_email_done, name='change_email_done'),
    path('change_icon_done', views.change_icon_done, name='change_icon_done'),
    path('change_password_done', views.change_password_done.as_view(), name='change_password_done'),
    path('logout', views.logout_view.as_view(), name='logout_view'),
] + static(settings.IMAGE_URL, document_root=settings.IMAGE_ROOT)