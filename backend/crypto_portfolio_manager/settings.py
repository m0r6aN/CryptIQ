import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'your-secret-key'  # Replace with a secure key or use environment variable

DEBUG = True  # Set to False in production

ALLOWED_HOSTS = ['*']  # Update with your domain or IP

AUTH_USER_MODEL = 'accounts.User'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'crypto_portfolio_manager.apps.accounts',
    'crypto_portfolio_manager.apps.portfolio',
    'crypto_portfolio_manager.apps.trading',
    'rest_framework_simplejwt',
    'channels',
    'ai_assistant',
]

ASGI_APPLICATION = 'crypto_portfolio_manager.asgi.application'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # Other middleware
]

ROOT_URLCONF = 'crypto_portfolio_manager.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Template settings
    },
]

WSGI_APPLICATION = 'crypto_portfolio_manager.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'crypto_db',
        'USER': 'postgres',
        'PASSWORD': 'your-password',
        'HOST': 'db',
        'PORT': 5432,
    },
    'mongo': {
        'ENGINE': '',
        'NAME': 'crypto_mongo_db',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    # Password validators
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

STATIC_URL = '/static/'
