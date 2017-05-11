"""
https://docs.djangoproject.com/en/1.10/topics/settings/
"""

import os
from django.utils.translation import ugettext_lazy as _


LANGUAGES = (
    ('ru', _('Russin')),
    ('en', _('English')),
)

INFORMER_VERSION = '0.1'
PROGRAM_NAME = 'INFORMERS'

LANGUAGE_CODE = 'ru'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ACCOUNT_ACTIVATION_DAYS = 2 # кол-во дней для хранения кода активации

# для отправки кода активации
AUTH_USER_EMAIL_UNIQUE = True

EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "onedeveloptesting@gmail.com"
EMAIL_HOST_PASSWORD = 'jdivkcennbtxrpii'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'onedeveloptesting@gmail.com'
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%t5f-e2lt&*1x1@sx2dkz9n)u+cen^!b1lfml2sin3nq52&h%j'


DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'photocritic.pythonanywhere.com']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.utils.translation',
    'django.contrib.sites',
    
    #other apps
    'registration',
    'password_reset',
    'compressor',
    'wagtail.wagtailforms',
    'wagtail.wagtailredirects',
    'wagtail.wagtailembeds',
    'wagtail.wagtailsites',
    'wagtail.wagtailusers',
    'wagtail.wagtailsnippets',
    'wagtail.wagtaildocs',
    'wagtail.wagtailimages',
    'wagtail.wagtailsearch',
    'wagtail.wagtailadmin',
    'wagtail.wagtailcore',
    'wagtail_modeltranslation',
    'wagtailmedia',
    'django_extensions', #https://github.com/django-extensions/django-extensions
    'django_comments',
    'django_comments_xtd',
    'django_tz', #https://github.com/paluh/django-tz
    'phonenumber_field', #https://github.com/stefanfoulis/django-phonenumber-field
    'geoposition', #https://github.com/philippbosch/django-geoposition
    'ool', #https://github.com/gavinwahl/django-optimistic-lock
    'informer',
    'blog',
    'modelcluster',
    'taggit',
    'meta',
    'subscribe',
    'newsletter',
    #'floppyforms',
    'informer_vcard',
    #'debug_toolbar',
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
    'wagtail.wagtailcore.middleware.SiteMiddleware',
    'wagtail.wagtailredirects.middleware.RedirectMiddleware',
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
]

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]

ROOT_URLCONF = 'wisesite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            'informer/templates/',
            'informer/templates/password_reset/',
            'informer/templates/registration',
            'blog/templates/',
            'blog/templates/blog/',
            'django_comments_xtd/templates/',
            'django_comments_xtd/templates/comments',
            'newsletter/templates/admin',
            'newsletter/templates/newsletter',
            'subscribe/templates/subscribe',
            'informer_vcard/templates/informer_vcard/',
            ],
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

WAGTAIL_SITE_NAME = 'INFORMER'
WAGTAIL_FRONTEND_LOGIN_TEMPLATE = 'informer/login.html'
WAGTAIL_FRONTEND_LOGIN_URL = 'login_user'
WAGTAIL_ALLOW_UNICODE_SLUGS = False

BLOG_PAGINATOR_PER_PAGE = 6
TAGS_PAGINATOR_PER_PAGE = 24
SITE_ID = 1 #for django.contrib.sites
COMMENTS_APP = 'django_comments_xtd' #for django_comments
COMMENTS_XTD_CONFIRM_EMAIL = True
COMMENTS_XTD_MAX_THREAD_LEVEL = 0
COMMENTS_XTD_MAX_THREAD_LEVEL_BY_APP_MODEL = {
    'blog.blogpage': 2,
}
COMMENTS_XTD_FROM_EMAIL = "onedeveloptesting@gmail.com"
COMMENTS_XTD_SEND_HTML_EMAIL = True
COMMENTS_XTD_THREADED_EMAILS = True
COMMENTS_XTD_FORM_CLASS = "django_comments_xtd.forms.XtdCommentForm"

MANAGERS = (
    ('Менеджер блога', 'photocritic72@gmail.com'),
)

#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' # Разрешить отправку email сообщений на консоль
#COMMENTS_XTD_MARKUP_FALLBACK_FILTER = 'markdown'
UNREGISTERED_USER_CAN_COMMENT = False

#SEO
META_SITE_PROTOCOL = 'http'
META_USE_SITES = None
META_SITE_DOMAIN = 'photocritic.pythonanywhere.com'
META_IMAGE_URL = '/media/images/'
GOOGLE_ANALYTICS_TRACKING_ID = ''
#GEO 
GEOPOSITION_GOOGLE_MAPS_API_KEY = 'AIzaSyBmx9uxTpb8VljwAQQqvZQzkuDyKqY8_9o'
GEOPOSITION_MAP_WIDGET_HEIGHT = 280
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

MODELTRANSLATION_DEFAULT_LANGUAGE = 'ru'

# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators
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
RECOVER_ONLY_ACTIVE_USERS = False #Password recovery

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

TIME_ZONE = 'UTC'

USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',    
]


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'static','media')
MEDIA_URL = '/media/'
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale/'),
)
ALLOWED_IMAGE_TYPES = ("jpeg", "jpg", "png", "gif")
COMPRESS_ENABLED = False
COMPRESS_OFFLINE = True
COMPRESS_OUTPUT_DIR = 'cache'

INTERNAL_IPS = ('127.0.0.1', 'photocritic.pythonanywhere.com',)