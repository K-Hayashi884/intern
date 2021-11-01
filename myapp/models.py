from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    img = models.ImageField(upload_to='images', blank=True, null=True)


class Talk(models.Model):
    message = models.CharField(max_length=300)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="from_user")
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="to_user")
    sent_time = models.DateTimeField(auto_now_add=True)
