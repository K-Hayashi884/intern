from accounts.models import CustomUser

from django.db import models

class Talk(models.Model):


    # メッセージ
    talk = models.CharField(max_length=500)
    # 誰から
    talk_from = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="talk_from"
    )
    # 誰に
    talk_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="talk_to")
    # 時間は
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Talk'

    def __str__(self):
        return "{}>>{}".format(self.talk_from, self.talk_to)