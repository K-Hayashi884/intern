from django.contrib import admin
#from django.contrib.auth.admin import UserAdmin もし必要なら使ってみる
from .models import User, MyUserManager

admin.site.register(User)
#,UserAdmin
