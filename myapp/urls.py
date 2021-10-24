from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('index', views.index, name='index'),
    path('signup', views.ImageView.as_view(), name='signup_view'),
    path('login/', LoginView.as_view(redirect_authenticated_user=True, template_name='myapp/login.html'), name='login_view'),
    path('logout/', LogoutView.as_view(), name='logout_view'),
    path('friends', views.friends, name='friends'),
    path('talk_room/<int:user_id>', views.talk_room, name='talk_room'),
    path('setting', views.setting, name='setting'),
    path('username_edit/<int:login_id>', views.username_edit, name='username_edit'),
    path('email_edit/<int:login_id>', views.email_edit, name='email_edit'),
    path('image_edit/<int:login_id>', views.image_edit, name='image_edit'),
    # path('password_edit/<int:login_id>', views.password_edit, name='password_edit'),
    path('password_edit/<int:login_id>', views.PasswordChange.as_view(), name='password_edit'),
]

