from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    icon = models.ImageField(verbose_name="画像", upload_to="uploads", default="images/noimage.png")
