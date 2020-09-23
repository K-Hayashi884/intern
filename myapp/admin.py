from django.contrib import admin
from .models import User, UserImage, Talk, HeaderImage, prof_msg

admin.site.register(User)
admin.site.register(UserImage)
admin.site.register(Talk)
admin.site.register(HeaderImage)
admin.site.register(prof_msg)
