import os
from os.path import abspath, dirname

from django.core.exceptions import ImproperlyConfigured


def get_env_variable(var_name):
    """Get the environment variable or return exception"""
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the %s env variable" % var_name
        raise ImproperlyConfigured(error_msg)


DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Eric', 'ebrelsford@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': get_env_variable('FARMING_CONCRETE_DB_NAME'),
        'USER': get_env_variable('FARMING_CONCRETE_DB_USER'),
        'PASSWORD': get_env_variable('FARMING_CONCRETE_DB_PASSWORD'),
        'HOST': get_env_variable('FARMING_CONCRETE_DB_HOST'),
        'PORT': get_env_variable('FARMING_CONCRETE_DB_PORT'),
    }
}

EMAIL_SUBJECT_PREFIX = 'Farming Concrete: '
DEFAULT_FROM_EMAIL = 'info@farmingconcrete.org'
SERVER_EMAIL = 'admin@farmingconcrete.org'

TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = True
USE_L10N = True

PROJECT_ROOT = os.path.join(abspath(dirname(__file__)), '..', '..')

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'collected_static')
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/admin/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = get_env_variable('FARMING_CONCRETE_SECRET_KEY')

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.media',
    'django.core.context_processors.request',

    'barn.context_processors.garden_types',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    'middleware.http.Http403Middleware',
)

ROOT_URLCONF = 'barn.urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
)

STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #'compressor.finders.CompressorFinder',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.staticfiles',

    'ajax_select',
    'south',

    'accounts',
    'audit',
    'cropcount',
    'farmingconcrete',
    'harvestcount',
)

AJAX_LOOKUP_CHANNELS = {
    'variety': ('farmingconcrete.lookups', 'VarietyLookup'),
    'garden': ('farmingconcrete.lookups', 'GardenLookup'),
    'uncounted_garden': ('cropcount.lookups', 'UncountedGardenLookup'),
    'gardener': ('harvestcount.lookups', 'GardenerLookup'),
}

AUTH_PROFILE_MODULE = 'accounts.UserProfile'

FARMINGCONCRETE_YEAR = 2013

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'log_file': {
            'level': 'WARN',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(PROJECT_ROOT, 'logs', 'django.log'),
            'maxBytes': '16777216', # 16megabytes
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['log_file', 'mail_admins',],
            'level': 'WARN',
            'propagate': True,
        },
    },
}
