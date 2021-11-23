from django.urls import path
from . import views


app_name = 'myapp'

urlpatterns = [
   path('',views.IndexView.as_view(),name="index"),
   path('friends',views.FriendsView.as_view(),name="friends"),
]
