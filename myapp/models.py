from datetime import datetime, timedelta
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    icon = models.ImageField(
        verbose_name="画像", upload_to="uploads", default="images/noimage.png"
    )


# トーク内容を全てdatbaseに保存する形をとる
# ＞１個のトーク内容に紐づける情報は
# ＞〇誰が送ったのか
# ＞〇誰に送ったのか
# ＞〇いつ送ったのか
# という情報
class Talk(models.Model):
    # メッセージ
    talk = models.CharField(max_length=500)
    # 誰から
    talk_from = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="talk_from"
    )
    # 誰に
    talk_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="talk_to")
    # 時間は
    time = models.DateTimeField(auto_now_add=True)

    def get_elapsed_time(self) -> str:
        # メッセージが生成されてから経った時間
        delta = timezone.now() - self.time
        zero_delta, hour_delta, day_delta, week_delta = (
            timedelta(),
            timedelta(hours=1),
            timedelta(days=1),
            timedelta(days=7),
        )
        if zero_delta < delta < hour_delta:
            return f"{int(delta.seconds//60)}分前"

        elif hour_delta <= delta < day_delta:
            return f"{int(delta.seconds//(60*60))}時間前"

        elif day_delta <= delta < week_delta:
            return f"{int(delta.days)}日前"

        elif week_delta <= delta:
            return "1週間以上前"

        else:
            raise ValueError

    def __str__(self):
        return "{}>>{}".format(self.talk_from, self.talk_to)
