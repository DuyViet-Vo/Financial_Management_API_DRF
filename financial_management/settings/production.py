# myproject/settings/production.py

from .base import *

DEBUG = False

ALLOWED_HOSTS = ["192.168.35.158"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "financial_management",
        "USER": "postgres",
        "PASSWORD": "vdv18102001",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
