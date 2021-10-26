from django.urls import path
from . import views

app_name = 'chatapp'
urlpatterns = [
    path('',views.Login,name='login'),
    path("logout",views.Logout,name="Logout"),
    path('register', views.AccountRegistration.as_view(), name='register'),
    path('home', views.home, name='home'),
    path('message/<int:num>', views.message, name='message'),
    path('setting/<int:num>', views.setting, name='setting'),
    path('namechange/<int:num>', views.namechange, name='namechange'),
    path('adresschange/<int:num>', views.adresschange, name='adresschange'),
    path('iconchange/<int:num>', views.iconchange, name='iconchange'),
    path('password/<int:num>', views.password, name='password'),
]