from django.urls import path
from . import views
from django.conf import settings #追加   
from django.conf.urls.static import static #追加


urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup_view, name='signup_view'),
    path('login', views.Login.as_view(), name='login_view'),
    path('friends', views.friends, name='friends'),
    path('talklist', views.talklist_view, name='talklist'),
    path('talk_room/<partner_name>', views.talk_room, name='talk_room'),
    path('setting', views.setting, name='setting'),
    path('change_name', views.NameChangeView.as_view(), name='change_name'),
    path('change_mail', views.EmailChangeView.as_view(), name='change_mail'),
    path('change_icon', views.IconChangeView.as_view(), name='change_icon'),
    path('change_pass', views.PasswordChange.as_view(), name='change_pass'),
    path('success/<name>', views.change_success, name='change_success'),
    path('logout', views.logout_view, name='logout'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #追加
