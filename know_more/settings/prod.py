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

# Email Backend (AWS SES for production)
EMAIL_BACKEND = env('EMAIL_BACKEND', default='django_ses.SESBackend')
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID', default='')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY', default='')
AWS_SESSION_PROFILE = env('AWS_SESSION_PROFILE', default='')
AWS_SES_REGION_NAME = env('AWS_SES_REGION_NAME', default='us-west-2')
AWS_SES_REGION_ENDPOINT = env('AWS_SES_REGION_ENDPOINT', default='email.us-west-2.amazonaws.com')

DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='noreply@promptforgood.org')

# Cloudflare
CLOUDFLARE_TURNSTILE_SECRET_KEY = env('CLOUDFLARE_TURNSTILE_SECRET_KEY')

# Security headers
SECURE_SSL_REDIRECT = env('SECURE_SSL_REDIRECT', cast=bool, default=True)
SESSION_COOKIE_SECURE = env('SESSION_COOKIE_SECURE', cast=bool, default=True)
CSRF_COOKIE_SECURE = env('CSRF_COOKIE_SECURE', cast=bool, default=True)
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Static files root for production (where collectstatic will put files)
STATIC_ROOT = BASE_DIR / 'staticfiles'
