from .base import *

DEBUG = True

SECRET_KEY = env('SECRET_KEY', default='django-insecure-gjpu_d6@sp%%yx*0hvsaaugfhip2aj&6^e%16nmb&8xixdqu3x')

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Caching (LocMemCache for development)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-know-more',
    }
}

# Email Backend (Console for development)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
