from .settings import *
import os
import environ

env = environ.Env()
env.read_env(os.path.join(BASE_DIR, ".env"))
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRES_DB"),
        "USER": env("POSTGRES_USER"),
        "PASSWORD": env("POSTGRES_PASSWORD"),
        "HOST": "db",
        "PORT": 5432,
    }
}
