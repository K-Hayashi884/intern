from django.contrib import admin
# Register your models here.
from .models import Talk, User
#from django.contrib.auth.admin import UserAdmin

admin.site.register(Talk)
admin.site.register(User)