from .base import *

# Read .env file if it exists
if os.path.exists(BASE_DIR / "development.env"):
    print("Reading development.env file")
    environ.Env.read_env(BASE_DIR / "development.env")
else:
    print("No development.env file found")

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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'account': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'ai': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# Email Backend (Console for development)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'messenger@promptforgood.org'
