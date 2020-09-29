from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import AbstractUser,UserManager
from django.utils.translation import gettext_lazy as _
from django.core import validators

class User(User):
   pass

class UserImage(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_img")
   image = models.ImageField(
        verbose_name="画像", null=True, blank=True, upload_to="images"
    )
   def __int__(self):
       return "{}の写真".format(self.user)

class Talk(models.Model):
   talk = models.CharField(max_length=10000)
   time = models.DateTimeField()
   person_from = models.ForeignKey(User, related_name="person_from", on_delete=models.CASCADE)
   person_to = models.ForeignKey(User, related_name="person_to", on_delete=models.CASCADE)

class HeaderImage(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="header_img")
   image = models.ImageField(
        verbose_name="画像", null=True, blank=True, upload_to="header"
    )
   def __int__(self):
       return "{}の写真".format(self.user)

class prof_msg(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profile_msg")
   prof_msg = models.CharField(max_length=140, null=True, blank=True)

class Profile(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profile")
   height = models.IntegerField(
      validators=[validators.MinValueValidator(0),
                    validators.MaxValueValidator(300)]
   )
   weight = models.IntegerField(
      validators=[validators.MinValueValidator(0),
                    validators.MaxValueValidator(1000)]
   )