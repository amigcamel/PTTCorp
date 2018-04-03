"""
Django settings for PTTCorp project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import glob
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'p&&a0l3o5s#*#^$9g9^boio&$us(6687dvq3sa5^^6o*qldl@*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'pttcorp_comments',
    'pttcorp_admin',
    'django_facebook',
    'misc',
    'rest_framework',
    'api',
    'django_pygments',
    'main',
    'intro',
    'segmentation',
    'sketch',
    'sentiment',
    'registration',
    'captcha',
    'registration_defaults',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'endless_pagination',
    'django_bootstrap_breadcrumbs',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'flashcookie.FlashMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'flashcookie.flash_context',
    'django_facebook.context_processors.facebook',
)

AUTHENTICATION_BACKENDS = (
    'django_facebook.auth_backends.FacebookBackend',
    'django.contrib.auth.backends.ModelBackend',
)

ROOT_URLCONF = 'PTTCorp.urls'

WSGI_APPLICATION = 'PTTCorp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Taipei'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

# STATIC_URL = '/static/'
# STATICFILES_DIRS = (
#     os.path.join(os.path.dirname(os.path.dirname(__file__)),'static'),
# )

STATIC_URL = '/static_pttcorp/'
STATICFILES_DIRS = (
    os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static'),
)
STATIC_ROOT = os.path.join(BASE_DIR, 'static_pttcorp')

UPLOADFILES_DIRS = os.path.join(
    os.path.dirname(
        os.path.dirname(__file__)),
    'user_uploads')


# TEMPLATE PATH
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'registration_defaults/templates/registration'),
)

TEMPLATE_DIRS += tuple(glob.glob(os.path.join(BASE_DIR, 'templates/*')))


ALLOWED_HOSTS = ['lopen.linguistics.ntu.edu.tw', '140.112.147.121']
SITE_ID = 1
ACCOUNT_ACTIVATION_DAYS = 2

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = 'pttcorp.aji@gmail.com'
EMAIL_HOST_PASSWORD = '''sta':K:gt*vL#%(yF{Dzr(@4JRF'W=Q;87S7GPs)?<{&w9z2YcWRn>YsK%8=Pv:ps74>\c+=#'\z(!AUdf3+g6M^wv8,P&p$pa5<'''

LOGIN_REDIRECT_URL = 'index'

ENDLESS_PAGINATION_PER_PAGE = 100

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '20/minute'
    },
}

FACEBOOK_APP_ID = '666382376793585'
FACEBOOK_APP_SECRET = '48144519bcb83dc76aab23a5e1b3c325'

AUTH_PROFILE_MODULE = 'django_facebook.FacebookProfile'
FACEBOOK_LOGIN_DEFAULT_REDIRECT = '/PTT'

LOGGING = {
    'version': 1,
    'formatters': {
        'standard': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'propagate': False,
            'level': 'ERROR',
        },
        'django.db.backends': {
            'handlers': ['null'],  # Quiet by default!
            'propagate': False,
            'level': 'DEBUG',
        },
    },
}
