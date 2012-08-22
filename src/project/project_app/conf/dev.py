# -*- coding: utf-8 -*-

import logging

from .base import *


PROJECT_ROOT = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_ROOT, 'var','db.sqlite'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        #'OPTIONS': {
        #    'init_command': 'SET storage_engine=InnoDB',
        #    'charset' : 'utf8',
        #    'use_unicode' : True,
        #},
        #'TEST_CHARSET': 'utf8',
        #'TEST_COLLATION': 'utf8_general_ci',
    }
}

# Uncomment this and set to all slave DBs in use on the site.
# SLAVE_DATABASES = ['slave']

# Recipients of traceback emails and other notifications.
ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Almaty'

# Debugging displays nice error messages, but leaks memory. Set this to False
# on all server instances and True only for development.
DEBUG = TEMPLATE_DEBUG = True

# Make this unique, and don't share it with anybody.  It cannot be blank.
SECRET_KEY = '{{ secret_key }}'

ROOT_URLCONF = '{{ project_name }}.urls_dev'

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'var','media')
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'var', 'static')
MEDIA_URL = '/media/'
STATIC_URL = '/static/'

ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'


# Uncomment these to activate and customize Celery:
# CELERY_ALWAYS_EAGER = False  # required to activate celeryd
# BROKER_HOST = 'localhost'
# BROKER_PORT = 5672
# BROKER_USER = 'django'
# BROKER_PASSWORD = 'django'
# BROKER_VHOST = 'django'
# CELERY_RESULT_BACKEND = 'amqp'

# Common Event Format logging parameters
#CEF_PRODUCT = '{{ project_name }}'
#CEF_VENDOR = 'Your Company'
#CEF_VERSION = '0'
#CEF_DEVICE_VERSION = '0'

INTERNAL_IPS = ('127.0.0.1')

# Enable these options for memcached
#CACHE_BACKEND= "memcached://127.0.0.1:11211/"
#CACHE_MIDDLEWARE_ANONYMOUS_ONLY=True

# Set this to true if you use a proxy that sets X-Forwarded-Host
#USE_X_FORWARDED_HOST = False

SERVER_EMAIL = 'webmaster@example.com'
DEFAULT_FROM_EMAIL = 'webmaster@example.com'
SYSTEM_EMAIL_PREFIX = '[{{ project_name }}]'

#EMAIL_HOST = 'localhost'
#EMAIL_PORT = 25
#EMAIL_HOST_USER = ''
#EMAIL_HOST_PASSWORD = ''
#EMAIL_USE_TLS = False


# LOGGING

LOG_LEVEL = logging.INFO
HAS_SYSLOG = True
SYSLOG_TAG = 'http_app_{{ project_name }}'  # Make this unique to your project.

# Remove this configuration variable to use your custom logging configuration
LOGGING_CONFIG = None
LOGGING = {
    'version': 1,
    'loggers': {
        '{{ project_name }}': {
            'level': "DEBUG"
        }
    }
}

#LOGGING = {
#    'version': 1,
#    'disable_existing_loggers': False,
#    'filters': {
#        'require_debug_false': {
#            '()': 'django.utils.log.RequireDebugFalse'
#        }
#    },
#    'handlers': {
#        'mail_admins': {
#            'level': 'ERROR',
#            'filters': ['require_debug_false'],
#            'class': 'django.utils.log.AdminEmailHandler'
#        }
#    },
#    'loggers': {
#        'django.request': {
#            'handlers': ['mail_admins'],
#            'level': 'ERROR',
#            'propagate': True,
#        },
#    }
#}
