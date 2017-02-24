"""
Django settings for wisesite project.
Generated by 'django-admin startproject' using Django 1.9.
For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/
"""

import os
from django.utils.translation import ugettext_lazy as _


LANGUAGES = (
    ('ru', _('Russin')),
    ('en', _('English')),
)

LANGUAGE_CODE = 'ru'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ACCOUNT_ACTIVATION_DAYS = 2 # кол-во дней для хранения кода активации

# для отправки кода активации
AUTH_USER_EMAIL_UNIQUE = True
# EMAIL_HOST = 'localhost'
# EMAIL_PORT = 1025
# EMAIL_HOST_USER = ''
# EMAIL_HOST_PASSWORD = ''
# EMAIL_USE_TLS = False
# DEFAULT_FROM_EMAIL = 'info@google.ru'

EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "onedeveloptesting@gmail.com"
EMAIL_HOST_PASSWORD = 'jdivkcennbtxrpii'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'onedeveloptesting@gmail.com'
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%t5f-e2lt&*1x1@sx2dkz9n)u+cen^!b1lfml2sin3nq52&h%j'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['photocritic.pythonanywhere.com']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.utils.translation',
    
    #projects app
    'customuseradmin',
    'informer',
    
    #other apps
    'registration',
    'password_reset',
    'compressor',
    #debugg
    #'dbgp',
    'debug_toolbar',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware', 
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'wisesite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['informer/templates/','informer/templates/password_reset/','informer/templates/registration'],
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

WSGI_APPLICATION = 'wisesite.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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

LOGIN_REDIRECT_URL = "index"
LOGOUT_REDIRECT_URL = "index"
REGISTRATION_OPEN = True
RECOVER_ONLY_ACTIVE_USERS = False

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #other finders
    'compressor.finders.CompressorFinder',    
]

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'static','media')
MEDIA_URL = '/media/'
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale/'),
)

COMPRESS_ENABLED = False
COMPRESS_OFFLINE = True
COMPRESS_OUTPUT_DIR = 'cache'

INTERNAL_IPS = '127.0.0.1'