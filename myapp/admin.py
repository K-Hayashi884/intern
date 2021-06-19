from django.contrib import admin
from .models import Post, Photo, Message

# Register your models here.
admin.site.register(Photo)
admin.site.register(Message)