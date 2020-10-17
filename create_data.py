
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


if __name__ == "__main__":
    print("start create student")
    create_user(1000)
    print("end create student")
