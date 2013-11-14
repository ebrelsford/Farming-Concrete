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
DEFAULT_FROM_EMAIL = 'Farming Concrete <info@farmingconcrete.org>'
SERVER_EMAIL = 'admin@farmingconcrete.org'

TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'

DATE_INPUT_FORMATS = (
    '%m/%d/%Y', '%Y-%m-%d', '%m/%d/%y',
    '%b %d %Y', '%b %d, %Y',
    '%d %b %Y', '%d %b, %Y',
    '%B %d %Y', '%B %d, %Y',
    '%d %B %Y', '%d %B, %Y',
)
TIME_INPUT_FORMATS = ('%I:%M %p', '%H:%M:%S', '%H:%M')

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
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.debug',
    'django.core.context_processors.static',

    'feedback.context_processors.feedback_form',

    'barn.context_processors.garden_types',
    'metrics.context_processors.metrics',
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

    'compressor.finders.CompressorFinder',
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
    'chosen',
    'compressor',
    'djangojs',
    'feedback',
    'floppyforms',
    'registration',
    'south',
    'widget_tweaks',

    'accounts',
    'audit',
    'estimates',
    'farmingconcrete',
    'harvestmap',
    'imagekit',
    'metrics',
    'metrics.compost',
    'metrics.cropcount',
    'metrics.harvestcount',
    'metrics.landfilldiversion',
    'metrics.lookinggood',
    'metrics.moods',
    'metrics.participation',
    'metrics.reach',
    'metrics.recipes',
    'metrics.skills',
    'metrics.yumyuck',
)

AJAX_LOOKUP_CHANNELS = {
    'variety': ('farmingconcrete.lookups', 'VarietyLookup'),
    'garden': ('farmingconcrete.lookups', 'GardenLookup'),
    'uncounted_garden': ('cropcount.lookups', 'UncountedGardenLookup'),
    'gardener': ('metrics.harvestcount.lookups', 'GardenerLookup'),
}

AUTH_PROFILE_MODULE = 'accounts.UserProfile'
DEFAULT_GROUPS = ('gardeners',)

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

ACCOUNT_ACTIVATION_DAYS = 7

FEEDBACK_CHOICES = (
    ('site bug', 'site bug'),
    ('site enhancement', 'site enhancement'),
    ('general feedback', 'general feedback'),
    ('project feedback', 'project feedback'),
)
