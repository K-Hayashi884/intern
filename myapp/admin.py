from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Image,Message

admin.site.register(User, UserAdmin)
admin.site.register(Image)
admin.site.register(Message)
