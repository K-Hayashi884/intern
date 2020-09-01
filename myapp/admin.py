from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from .models import UserImage,Talk
from django.contrib.auth.models import User

# admin.site.register(User)
admin.site.register(UserImage)
admin.site.register(Talk)
# Register your models here.
