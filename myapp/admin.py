from django.contrib import admin

# Register your models here.

from .models import Message, User

admin.site.register(User)
admin.site.register(Message)