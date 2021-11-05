from django.contrib import admin

from myapp.models import Message
from .models import CustomUser

admin.site.register(CustomUser)
admin.site.register(Message)