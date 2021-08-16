from .base import *

DEBUG = False

ADMINS = (
    ('Ruhel A', 'raktimahmed2019@outlook.com'),
)

ALLOWED_HOSTS = ['www.geek4bangla.com', 'geek4bangla.com']

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.postgresql',
       'NAME': 'geekacademy',
       'USER': 'educa',
       'PASSWORD': 'gkac@2021',
   }
}

SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE = True