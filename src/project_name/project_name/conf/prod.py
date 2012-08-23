# -*- coding: utf-8 -*-

from .base import *

DEBUG = TEMPLATE_DEBUG = False

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.',
#        'NAME': '{{ project_name }}',
#        'USER': '{{ project_name }}',
#        'PASSWORD': '{{ project_name }}',
#        'HOST': 'localhost',
#        'PORT': '',
#        #'OPTIONS': {
#        #    'init_command': 'SET storage_engine=InnoDB',
#        #    'charset' : 'utf8',
#        #    'use_unicode' : True,
#        #},
#        #'TEST_CHARSET': 'utf8',
#        #'TEST_COLLATION': 'utf8_general_ci',
#    }
#}

ADMINS = (
    ('Ivan Perelivskiy', 'livskiy@gmail.com'),
)

MANAGERS = ADMINS

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'var','media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'var', 'static')
STATIC_URL = '/static/'

#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

#EMAIL_HOST = 'smtp.gmail.com'
#EMAIL_PORT = 587
#EMAIL_HOST_USER = 'admin@example.com'
#EMAIL_HOST_PASSWORD = ''
#EMAIL_USE_TLS = True
