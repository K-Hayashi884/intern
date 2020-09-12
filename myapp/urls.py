from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup_view, name='signup_view'),
    path('login', views.Login.as_view(), name='login_view'),
    path('friends', views.friends, name='friends'),
    # path('friends', views.find, name='find'),
    path('talk_room/<int:num>', views.talk_room, name='talk_room'),
    path('setting', views.setting, name='setting'),
]
urlpatterns  += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
