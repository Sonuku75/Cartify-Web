"""Django settings for Cartify backend foundation."""
from datetime import timedelta
import os
from pathlib import Path
import sys
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Initialize environment variables handler
env = environ.Env(
    DJANGO_DEBUG=(bool, False),
    DJANGO_SECRET_KEY=(str, 'django-insecure-cartify-dev-baseline-key-change-in-production'),
    DJANGO_ALLOWED_HOSTS=(list, ['localhost', '127.0.0.1', '0.0.0.0', 'testserver']),
    DJANGO_TIME_ZONE=(str, 'UTC'),
    DATABASE_ENGINE=(str, 'django.db.backends.postgresql'),
    DATABASE_NAME=(str, 'cartify_db'),
    DATABASE_USER=(str, 'cartify_user'),
    DATABASE_PASSWORD=(str, ''),
    DATABASE_HOST=(str, 'localhost'),
    DATABASE_PORT=(int, 5432),
    DATABASE_CONN_MAX_AGE=(int, 600),
    REDIS_URL=(str, 'redis://127.0.0.1:6379/1'),
    CELERY_BROKER_URL=(str, 'redis://127.0.0.1:6379/1'),
    CELERY_RESULT_BACKEND=(str, 'redis://127.0.0.1:6379/1'),
    CORS_ALLOWED_ORIGINS=(list, ['http://localhost:3000', 'http://127.0.0.1:3000']),
    CSRF_TRUSTED_ORIGINS=(list, ['http://localhost:3000', 'http://127.0.0.1:3000']),
    JWT_ACCESS_TOKEN_LIFETIME_MINUTES=(int, 60),
    JWT_REFRESH_TOKEN_LIFETIME_DAYS=(int, 7),
)

# Take environment variables from .env file if present
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Core security settings
SECRET_KEY = env('DJANGO_SECRET_KEY')
DEBUG = env('DJANGO_DEBUG')
ALLOWED_HOSTS = env('DJANGO_ALLOWED_HOSTS')

# Fail-fast security validation in production
if not DEBUG and 'test' not in sys.argv:
    if SECRET_KEY == 'django-insecure-cartify-dev-baseline-key-change-in-production':
        from django.core.exceptions import ImproperlyConfigured
        raise ImproperlyConfigured(
            "DJANGO_SECRET_KEY must be configured with a secure production secret key when DEBUG is False."
        )
    if not ALLOWED_HOSTS or '*' in ALLOWED_HOSTS:
        from django.core.exceptions import ImproperlyConfigured
        raise ImproperlyConfigured(
            "DJANGO_ALLOWED_HOSTS must not be empty or contain wildcard '*' when DEBUG is False."
        )

# Application definition
DJANGO_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
]

LOCAL_APPS = [
    'common',
    'apps.users',
    'apps.products',
    'apps.categories',
    'apps.brands',
    'apps.inventory',
    'apps.cart',
    'apps.wishlist',
    'apps.orders',
    'apps.payments',
    'apps.shipping',
    'apps.coupons',
    'apps.reviews',
    'apps.returns',
    'apps.notifications',
    'apps.sellers',
    'apps.cms',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'

# Database configuration: PostgreSQL via Django ORM
DATABASES = {
    'default': {
        'ENGINE': env('DATABASE_ENGINE', default='django.db.backends.postgresql'),
        'NAME': env('DATABASE_NAME', default='cartify_db'),
        'USER': env('DATABASE_USER', default=''),
        'PASSWORD': env('DATABASE_PASSWORD', default=''),
        'HOST': env('DATABASE_HOST', default='localhost'),
        'PORT': env('DATABASE_PORT', default=5432),
        'CONN_MAX_AGE': env('DATABASE_CONN_MAX_AGE', default=600),
        'CONN_HEALTH_CHECKS': True,
        'OPTIONS': {
            'connect_timeout': 5,
        },
    }
}

# Cache configuration: Redis in production/development, LocMemCache in tests
if 'test' in sys.argv:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'cartify-test-cache',
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': env('REDIS_URL'),
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
                'CONNECTION_POOL_KWARGS': {'max_connections': 100},
                'IGNORE_EXCEPTIONS': True,
            },
            'KEY_PREFIX': 'cartify',
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 10},
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = env('DJANGO_TIME_ZONE')
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files (User uploads, product images)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User Model
AUTH_USER_MODEL = 'users.User'

# Django REST Framework Settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PAGINATION_CLASS': 'common.pagination.StandardResultsSetPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': env('THROTTLE_RATE_ANON', default='100/minute'),
        'user': env('THROTTLE_RATE_USER', default='1000/minute'),
        'auth_burst': env('THROTTLE_RATE_AUTH_BURST', default='5/minute'),
        'auth_sustained': env('THROTTLE_RATE_AUTH_SUSTAINED', default='20/hour'),
    },
    'EXCEPTION_HANDLER': 'common.exceptions.custom_exception_handler',
}

if DEBUG:
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] += (
        'rest_framework.renderers.BrowsableAPIRenderer',
    )

# SimpleJWT Settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=env('JWT_ACCESS_TOKEN_LIFETIME_MINUTES')),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=env('JWT_REFRESH_TOKEN_LIFETIME_DAYS')),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
}

# CORS & CSRF Settings
CORS_ALLOWED_ORIGINS = env('CORS_ALLOWED_ORIGINS')
CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = env('CSRF_TRUSTED_ORIGINS')

# Redis & Celery Infrastructure Settings
REDIS_URL = env('REDIS_URL')
CELERY_BROKER_URL = env('CELERY_BROKER_URL', default=REDIS_URL)
CELERY_RESULT_BACKEND = env('CELERY_RESULT_BACKEND', default=REDIS_URL)
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_TRACK_STARTED = True
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_RESULT_EXPIRES = 3600

# Cookie & Session Security
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_HTTPONLY = False
SESSION_COOKIE_AGE = 1209600  # 2 weeks

# Security Headers & Hardening
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Request Body & Upload Constraints
DATA_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024  # 5 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10 MB
DATA_UPLOAD_MAX_NUMBER_FIELDS = 1000
FILE_UPLOAD_PERMISSIONS = 0o644
FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o755
MAX_IMAGE_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

# SSL redirect is controlled by environment variable (enabled in production with HTTPS)
SECURE_SSL_REDIRECT = env.bool('DJANGO_SECURE_SSL_REDIRECT', default=False)

if not DEBUG and SECURE_SSL_REDIRECT:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = env.int('DJANGO_SECURE_HSTS_SECONDS', default=31536000)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# Ensure test runner host is accepted during testing
if 'test' in sys.argv and 'testserver' not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append('testserver')

# Structured Logging Configuration with Sensitive Data Redaction
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'sensitive_data_filter': {
            '()': 'common.logging.SensitiveDataFilter',
        },
    },
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'filters': ['sensitive_data_filter'],
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'apps': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'common': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'celery': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
