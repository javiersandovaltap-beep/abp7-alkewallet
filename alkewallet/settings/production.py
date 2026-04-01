 
from .base import *
import os
import dj_database_url

DEBUG = False

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost').split(',')

DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600,
        ssl_require=True,
    )
}

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
