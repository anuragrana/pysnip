"""
Django settings for pysnip project.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os
from django.urls import reverse_lazy

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

import environ

env = environ.Env()
# reading .env file
environ.Env.read_env()
SECRET_KEY = env("SECRET_KEY", default='django-insecure-p(sa&exo^8_c58#d!+n(n79+l+gzm3n!wk8#(&_hyamnxo27&t')

# SECURITY WARNING: don't run with debug turned on in production!
if env('ENVIRONMENT') == "prod":
    DEBUG = False
    ALLOWED_HOSTS = [
        "https://pythonsnippets.dev",
        "https://www.pythonsnippets.dev",
        "pythonsnippets.dev",
        "www.pythonsnippets.dev"
    ]
else:
    DEBUG = True
    ALLOWED_HOSTS = ["*"]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'snip',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pysnip.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'snip.context_processor.site',
            ],
        },
    },
]

WSGI_APPLICATION = 'pysnip.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env("DATABASE_NAME"),
        'USER': env("DATABASE_USER"),
        'PASSWORD': env("DATABASE_PASSWORD"),
        'HOST': env("DATABASE_HOST"),
        'PORT': env("DATABASE_PORT"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

PROJECT_NAME = "PythonSnippets"
PROJECT_NAME_SPACED = "Python Snippets"
SITE_DESC = "Useful Python Snippets. Curated list of Python Snippets. Python Tricks."
SITE_URL = "https://pythonsnippets.dev"
SEO_KEYWORDS = "Python, Django, Python Code, Python Tricks, Python Snippets."

# LOGIN_URL = '/accounts/login/' is used by login_required decorator
LOGIN_URL = reverse_lazy('snip:mylogin')

# logout the user - invalidate the session - when browser is closed
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

GITHUB_SECRET = env("GITHUB_SECRET")
GITHUB_CLIENT_ID = env("GITHUB_CLIENT_ID")

try:
    from .logger_settings import *
except Exception as e:
    print("Unable to load logger settings")
    pass

# these message tags will be used in bootstrap
try:
    from django.contrib.messages import constants as messages

    MESSAGE_TAGS = {
        messages.DEBUG: 'alert-info',
        messages.INFO: 'alert-info',
        messages.SUCCESS: 'alert-success',
        messages.WARNING: 'alert-warning',
        messages.ERROR: 'alert-danger',
    }
except Exception as e:
    pass


