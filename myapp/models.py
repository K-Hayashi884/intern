from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import AbstractUser,UserManager
from django.utils.translation import gettext_lazy as _
from django.core import validators
from .con import PREFECTURES_CHOICE

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
   def __str__(self):
       return "{}の写真".format(self.user)

class prof_msg(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profile_msg")
   prof_msg = models.CharField(max_length=140, null=True, blank=True)

class Hobby(models.Model):
   name = models.CharField(max_length=100, unique=True)

   def __str__(self):
      return self.name

class Profile(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profile")
   age = models.IntegerField(
      validators=[validators.MinValueValidator(0),
                    validators.MaxValueValidator(130)],
                    null=True,
                    blank=True,
   )
   location = models.CharField(max_length=40, null=True, blank=True, choices=PREFECTURES_CHOICE)
   birthday = models.DateField(null=True,
                    blank=True,)
   hobby = models.ManyToManyField(Hobby)

   def __str__(self):
      return self.user.username + "のプロフィール"