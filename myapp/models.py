from django.db import models

# class Member(models.Model):
    name = models.CharField(max_length=50)
    mail = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    password_conf = models.CharField(max_length=100)
    img = models.ImageField(upload_to='images')
    def __str__(self):
        return 'name:' + self.name + ', mail:' + self.mail
