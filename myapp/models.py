from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass

class UserImage(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_image")
    image = models.ImageField(upload_to="image/")

    def __str__(self):
        return "{}の写真".format(self.user)


class Talk(models.Model):
    msg = models.CharField(max_length=120)
    msg_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name="msg_form")
    msg_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="msg_to")
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}から{}へのメッセージ".format(self.msg_from,self.msg_to)

    









