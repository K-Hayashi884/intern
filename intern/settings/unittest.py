from .settings import *
import os
import environ

env = environ.Env()
env.read_env(os.path.join(BASE_DIR, ".env"))
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
