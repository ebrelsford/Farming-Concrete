from .base import *


DEBUG = False
TEMPLATE_DEBUG = False

MEDIA_URL = '/barn/media/'
STATIC_URL = '/barn/static/'
ADMIN_MEDIA_PREFIX = '/barn/admin/media/'

EMAIL_HOST = get_env_variable('FARMING_CONCRETE_EMAIL_HOST')
EMAIL_HOST_USER = get_env_variable('FARMING_CONCRETE_EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = get_env_variable('FARMING_CONCRETE_EMAIL_HOST_PASSWORD')

ALLOWED_HOSTS = [
    '.farmingconcrete.org',
]


#
# email
#
INSTALLED_APPS += (
    'mailer',
)
EMAIL_BACKEND = 'mailer.backend.DbBackend'
EMAIL_HOST = get_env_variable('FARMING_CONCRETE_EMAIL_HOST')
EMAIL_HOST_USER = get_env_variable('FARMING_CONCRETE_EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = get_env_variable('FARMING_CONCRETE_EMAIL_HOST_PASSWORD')

# TODO
#  * app to create mailings
#  * associate mailings with users once sent
#  * allow for "faking" mailings
#  * mailings only get sent to users under certain conditions
#  * consider basing on django-drip https://github.com/zapier/django-drip

#
# Caching
#

CACHES = {
    'default' : dict(
        BACKEND = 'django.core.cache.backends.memcached.MemcachedCache',
        LOCATION = ['unix:///tmp/memcached.sock'],
    )
}
