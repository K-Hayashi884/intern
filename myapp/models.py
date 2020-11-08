from django.db import models


#下のUsersはミスったやつです。消す予定です。
class Users(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    password = models.CharField(max_length=100)
    img = models.ImageField()

    def __str__(self):
        return '<Users:username=' + self.username + ', ' + \
            'email=' + self.email + ', ' + \
            'password=' + self.password + '>'

# Create your models here.
