
import os
#import memcache_toolbar.panels.memcache

PROJECT_ROOT = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')

LANGUAGE_CODE = 'ru'

LANGUAGES = (
    ('ru', 'Russian'),
)

SITE_ID = 1


INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'django.contrib.contenttypes',
    'django.contrib.admin',
    #'django.contrib.sites',
    #'django.contrib.admindocs',
    #'django.contrib.markup',
    #'django.contrib.humanize',
    #'django.contrib.syndication',

    '{{ project_name }}',

    'django_extensions',
    'django_assets',
    'south',
]


# Defines the views served for root URLs.
ROOT_URLCONF = '{{ project_name }}.urls'

# Place bcrypt first in the list, so it will be the default password hashing
# mechanism
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
)


## SESSIONS

# By default, be at least somewhat secure with our session cookies.
SESSION_COOKIE_HTTPONLY = True

# Set this to true if you are using https
SESSION_COOKIE_SECURE = False


## TESTS
#TEST_RUNNER = 'test_utils.runner.RadicalTestSuiteRunner'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django_assets.finders.AssetsFinder',
)


MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


TEMPLATE_CONTEXT_PROCESSORS = [
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.debug',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.i18n',
    'django.core.context_processors.static',
]


TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or
    # "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)


# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)


FIXTURE_DIRS = (
    os.path.join(PROJECT_ROOT, 'fixtures'),
)

# Specify a model to use for user profiles, if desired.
#AUTH_PROFILE_MODULE = '{{ project_name }}.accounts.UserProfile'

FILE_UPLOAD_PERMISSIONS = 0664

# The WSGI Application to use for runserver
WSGI_APPLICATION = '{{ project_name }}.wsgi.application'

# http://south.aeracode.org/ticket/520
SOUTH_TESTS_MIGRATE = False


# THUMBNAILS

THUMBNAIL_BASEDIR = 'thumbs'
THUMBNAIL_PRESERVE_EXTENSIONS = True


# DEBUG TOOLBAR

MIDDLEWARE_CLASSES += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]


INSTALLED_APPS += [
    'debug_toolbar',
    #'debug_toolbar_user_panel',
]


def show_debug_toolbar(request):
    """
    Only show the debug toolbar to users with the superuser flag.
    """
    if 'XDebug' in request.COOKIES:
        return True
    return False


DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'SHOW_TOOLBAR_CALLBACK': show_debug_toolbar,
    'HIDE_DJANGO_SQL': True,
    'TAG': 'body',
    'SHOW_TEMPLATE_CONTEXT': True,
    'ENABLE_STACKTRACES': True,
}


DEBUG_TOOLBAR_PANELS = (
    #'debug_toolbar_user_panel.panels.UserPanel',
    #'memcache_toolbar.panels.memcache.MemcachePanel',
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
)
