# myproject/settings/local.py

from .base import *

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "financial_management",
        "USER": "postgres",
        "PASSWORD": "vdv1810",
        "HOST": "localhost",
        "PORT": "5432",
    }
}