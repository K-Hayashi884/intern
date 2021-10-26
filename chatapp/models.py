from django.db import models
#ユーザー認証
from django.contrib.auth.models import User

#ユーザーアカウントのモデルクラス
class Account(models.Model):
    #ユーザーアカウントのモデルクラス
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #追加フィールド
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    account_image = models.ImageField(upload_to="profile_pics",blank=True, null=True)

    def __str__(self):
        return self.user.username

#messageモデル
class Message(models.Model):
    loggedin_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loggedin_user', null=True, blank=True)
    friend = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='friend')
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=300)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '<Message:id=' + str(self.id) + ', ' + \
        self.title + '(' + str(self.pub_date) + ')>'

    class Meta:
        ordering = ('pub_date',)    