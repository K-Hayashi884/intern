from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import AbstractUser,UserManager
from django.utils.translation import gettext_lazy as _

class User(User):
    pass
class UserImage(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_img")
    image = models.ImageField(verbose_name="画像",null=True,blank=True,upload_to="images")
    def __int__(self):
        return "{}の写真".format(self.user)

class Talk(models.Model):
    talk = models.CharField(max_length = 500)
    talk_from = models.CharField(max_length = 20)
    talk_to = models.CharField(max_length = 20)
    def __int__(self):
        return "{}>>{}".format(self.talk_from, self.talk_to)