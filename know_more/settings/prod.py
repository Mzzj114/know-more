from .base import *

DEBUG = False

# Required settings for production
SECRET_KEY = env('SECRET_KEY')

ALLOWED_HOSTS = env('ALLOWED_HOSTS', cast=list)

# Database configuration (Defaults to MySQL as per user request)
# Expected DB URL format: mysql://user:password@host:port/dbname
DATABASES = {
    'default': env.db('DATABASE_URL', default='mysql://user:password@localhost:3306/know_more')
}

# Caching (Redis or equivalent is recommended for production, keeping LocMem for now but configurable)
CACHES = {
    'default': env.cache('CACHE_URL', default='locmemcache://unique-know-more')
}

# Email Backend (SMTP for production)
EMAIL_BACKEND = env('EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = env('EMAIL_HOST', default='')
EMAIL_PORT = env('EMAIL_PORT', cast=int, default=587)
EMAIL_USE_TLS = env('EMAIL_USE_TLS', cast=bool, default=True)
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')

# Security headers
SECURE_SSL_REDIRECT = env('SECURE_SSL_REDIRECT', cast=bool, default=True)
SESSION_COOKIE_SECURE = env('SESSION_COOKIE_SECURE', cast=bool, default=True)
CSRF_COOKIE_SECURE = env('CSRF_COOKIE_SECURE', cast=bool, default=True)
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
