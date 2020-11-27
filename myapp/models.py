from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    pass

class UserImage(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_img")
    image = models.ImageField(verbose_name="画像", upload_to="images", 
        default="images/noimage.png")
 
    def __str__(self):
       return "{}の写真".format(self.user)


class Talk(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")#送信した人
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver") #受信した人
    message = models.CharField(max_length=1000) #メッセージ内容
    date = models.DateTimeField(default=timezone.now) #日時
    


# Create your models here.
