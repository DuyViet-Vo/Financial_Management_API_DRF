# myproject/settings/local.py

from .base import *

DEBUG = True

ALLOWED_HOSTS = ["18.141.201.62"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "financial_management",
        "USER": "postgres",
        "PASSWORD": "vdv18102001",
        "HOST": "db-drf-postgreesql.cfkygo8i0xnp.ap-southeast-1.rds.amazonaws.com",
        "PORT": "5432",
    }
}
