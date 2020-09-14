
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE",'intern.settings')

import django
django.setup()

import random
from faker import Faker
from myapp.models import *

fakegen = Faker()
fakegen_ja = Faker(['ja_JP'])

def create_user(N=5):

    for  _ in range(N):

        user = User.objects.get_or_create(
            username=fakegen.user_name(),
            email=fakegen.ascii_company_email(),
        )[0]

        user.save()

    for  _ in range(N):

        sender = User.objects.all().order_by("?").first()
        receiver = User.objects.all().exclude(id=sender.id).order_by("?").first()

        msg = Message.objects.get_or_create(
            sender=sender,
            receiver=receiver,
            content=fakegen.text()
        )[0]

def create_msg(N=5):

    for _ in range(N):

        yusaku = User.objects.get(username="yusaku")
        other = User.objects.exclude(username="yusaku").order_by("?").first()
        sender = random.choice([yusaku,other])
        receiver = other if sender == yusaku else yusaku

        msg = Message.objects.get_or_create(
            sender=sender,
            receiver=receiver,
            content=fakegen.text()
        )[0]

if __name__ == "__main__":
    print("start create student")
    # create_user(50)
    create_msg(50)
    print("end create student")
