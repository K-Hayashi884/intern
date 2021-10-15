from django.db import models
from django.contrib.auth.models import AbstractUser

# ユーザーアカウントのクラス
class CustomUser(AbstractUser):
    account_image = models.ImageField(upload_to='profile_photos/', blank=True)

# トークメッセージのクラス
class Talk(models.Model):
    talk_from = models.ForeignKey(CustomUser, on_delete=models.CASCADE,\
            related_name='talk_from')
    talk_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE,\
            related_name='talk_to')
    content = models.TextField(max_length=1000)
    pub_date = models.DateTimeField(auto_now_add=True)
