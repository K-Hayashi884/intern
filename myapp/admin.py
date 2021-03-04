from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserImage, Talk

admin.site.register(User, UserAdmin)
admin.site.register(UserImage)
admin.site.register(Talk)
