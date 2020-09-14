from django.contrib import admin
from .models import User, UserImage, Talk

admin.site.register(User)
admin.site.register(UserImage)
admin.site.register(Talk)
