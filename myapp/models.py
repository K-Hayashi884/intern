from django.db import models
from django.contrib.auth.models import AbstractUser

# ユーザーアカウントのクラス
class CustomUser(AbstractUser):
    account_image = models.ImageField(upload_to='profile_photos/', blank=True)

# トークメッセージのクラス
class Talk(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE,\
            related_name='talk_owner')
    friend = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField(max_length=1000)
    pub_data = models.DateTimeField(auto_now_add=True)